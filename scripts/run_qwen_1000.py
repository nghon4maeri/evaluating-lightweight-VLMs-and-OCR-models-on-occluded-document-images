import csv
import random
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from jiwer import cer, wer
from transformers import AutoProcessor, BitsAndBytesConfig, Qwen2_5_VLForConditionalGeneration

DATA_ROOT = Path(r"D:\User\nghonamjiwoo\Natural Language Processing\Lab\oprb_dataset")
RESULTS_CSV = Path(r"D:\User\nghonamjiwoo\Natural Language Processing\Lab\colab_results\qwen2_5_vl_3b_results\qwen2_5_vl_3b_results\per_image_results.csv")
TARGET_TOTAL = 1000

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"
RANDOM_SEED = 42
NORMALIZE_CASE = True
MAX_IMAGE_PIXELS = 768 * 28 * 28
MAX_NEW_TOKENS = 1024

def parse_occlusion_metadata(stem: str) -> dict:
    parts = stem.split("__", 2)
    return {
        "occlusion_type": parts[0] if len(parts) > 0 and parts[0] else "unknown",
        "occlusion_density": parts[1] if len(parts) > 1 and parts[1] else "unknown",
        "batch_id": parts[2] if len(parts) > 2 and parts[2] else "unknown",
    }

def collect_test_pairs() -> list[dict]:
    pairs = []
    for category in ["text", "nontext"]:
        image_dir = DATA_ROOT / category / "img"
        gt_dir = DATA_ROOT / category / "gt"
        images = {p.stem: p for p in image_dir.glob("*.jpg")}
        gts = {p.stem: p for p in gt_dir.glob("*.txt")}
        common = sorted(images.keys() & gts.keys())
        for stem in common:
            pairs.append({
                "category": category,
                "sample_id": stem,
                "image_path": str(images[stem]),
                "gt_path": str(gts[stem]),
                **parse_occlusion_metadata(stem),
            })
    random.Random(RANDOM_SEED).shuffle(pairs)
    return pairs

def read_gt_tokens(gt_path: str) -> list[str]:
    tokens = []
    with open(gt_path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            fields = line.rstrip("\r\n").split("\t")
            if fields and fields[0].strip():
                tokens.append(fields[0].strip())
    return tokens

def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text.casefold() if NORMALIZE_CASE else text

def bag_of_words_prf(reference: str, prediction: str) -> tuple[float, float, float]:
    ref = Counter(reference.split())
    hyp = Counter(prediction.split())
    matched = sum((ref & hyp).values())
    ref_n, hyp_n = sum(ref.values()), sum(hyp.values())
    precision = matched / hyp_n if hyp_n else (1.0 if ref_n == 0 else 0.0)
    recall = matched / ref_n if ref_n else (1.0 if hyp_n == 0 else 0.0)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return float(precision), float(recall), float(f1)

def compute_metrics(ground_truth: str, prediction: str) -> dict:
    ref = clean_text(ground_truth)
    hyp = clean_text(prediction)
    p, r, f1 = bag_of_words_prf(ref, hyp)
    return {
        "cer": float(cer(ref, hyp)),
        "wer": float(wer(ref, hyp)),
        "token_precision": p,
        "token_recall": r,
        "token_f1": f1,
        "gt_words": len(ref.split()),
        "pred_words": len(hyp.split()),
    }

def main():
    pairs = collect_test_pairs()
    prev_df = pd.read_csv(RESULTS_CSV)
    completed = set(prev_df.loc[prev_df["status"] == "ok", "sample_id"].astype(str).tolist())
    print(f"Already completed: {len(completed)} / {TARGET_TOTAL}")
    
    needed = TARGET_TOTAL - len(completed)
    if needed <= 0:
        print("Target 1000 already reached!")
        return

    pending = [s for s in pairs if s["sample_id"] not in completed][:needed]
    print(f"Queued {len(pending)} samples to reach {TARGET_TOTAL}.")

    print("Loading processor and 4-bit Qwen2.5-VL-3B-Instruct...")
    processor = AutoProcessor.from_pretrained(
        MODEL_ID,
        min_pixels=256 * 28 * 28,
        max_pixels=MAX_IMAGE_PIXELS,
    )
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        quantization_config=quant_config,
        torch_dtype=torch.float16,
        device_map={"": "cuda:0"},
        attn_implementation="sdpa",
    )
    model.eval()
    print("Model loaded on RTX 4060!")

    OCR_PROMPT = (
        "Transcribe all text visible on this document page in natural reading order. "
        "Return only the transcription without introductory text or explanations. "
        "Do not describe the page, and do not invent or hallucinate occluded characters that you cannot read."
    )

    FIELDNAMES = [
        "category", "sample_id", "occlusion_type", "occlusion_density", "batch_id",
        "model_id", "status", "error", "prediction", "ground_truth",
        "latency_sec", "generated_tokens", "possibly_truncated",
        "cer", "wer", "token_precision", "token_recall", "token_f1",
        "gt_words", "pred_words",
    ]

    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        for idx, sample in enumerate(pending, 1):
            t0 = time.perf_counter()
            row = {
                "category": sample["category"],
                "sample_id": sample["sample_id"],
                "occlusion_type": sample["occlusion_type"],
                "occlusion_density": sample["occlusion_density"],
                "batch_id": sample["batch_id"],
                "model_id": MODEL_ID,
                "status": "error",
                "error": "",
                "prediction": "",
                "ground_truth": "",
                "latency_sec": np.nan,
                "generated_tokens": 0,
                "possibly_truncated": False,
                "cer": np.nan,
                "wer": np.nan,
                "token_precision": np.nan,
                "token_recall": np.nan,
                "token_f1": np.nan,
                "gt_words": 0,
                "pred_words": 0,
            }
            try:
                with torch.inference_mode():
                    with Image.open(sample["image_path"]) as im:
                        image = im.convert("RGB")
                    messages = [{
                        "role": "user",
                        "content": [{"type": "image"}, {"type": "text", "text": OCR_PROMPT}],
                    }]
                    prompt_text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                    inputs = processor(text=[prompt_text], images=[image], padding=True, return_tensors="pt").to("cuda:0")
                    output_ids = model.generate(
                        **inputs,
                        max_new_tokens=MAX_NEW_TOKENS,
                        do_sample=False,
                        repetition_penalty=1.05,
                    )
                    new_tokens = output_ids[0, inputs["input_ids"].shape[-1]:]
                    prediction = processor.decode(new_tokens, skip_special_tokens=True, clean_up_tokenization_spaces=False).strip()
                    torch.cuda.synchronize("cuda:0")
                    elapsed = time.perf_counter() - t0
                    n_tokens = int(new_tokens.numel())
                    truncated = n_tokens >= MAX_NEW_TOKENS
                    del inputs, output_ids, new_tokens

                ground_truth = " ".join(read_gt_tokens(sample["gt_path"]))
                metrics = compute_metrics(ground_truth, prediction)
                row.update({
                    "status": "ok",
                    "prediction": prediction,
                    "ground_truth": ground_truth,
                    "latency_sec": elapsed,
                    "generated_tokens": n_tokens,
                    "possibly_truncated": truncated,
                    **metrics,
                })
                print(f"[{idx}/{len(pending)}] {sample['category']} | {elapsed:.1f}s | CER={metrics['cer']:.3f} | tok={n_tokens}")
            except Exception as e:
                row["error"] = repr(e)
                print(f"[{idx}/{len(pending)}] ERROR: {e!r}")

            writer.writerow(row)
            csv_file.flush()
            if idx % 10 == 0:
                torch.cuda.empty_cache()

    print("Finished reaching 1,000 pages for Qwen2.5-VL-3B!")

if __name__ == "__main__":
    main()
