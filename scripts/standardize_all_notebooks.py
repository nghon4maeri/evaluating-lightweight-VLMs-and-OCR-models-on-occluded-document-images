import ast
import copy
import json
import os
import shutil
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent.parent
LAB_DIR = BENCH_DIR.parent / "Lab"

NOTEBOOKS_DIR = BENCH_DIR / "notebooks"
EXECUTED_DIR = NOTEBOOKS_DIR / "executed"
EXECUTED_DIR.mkdir(parents=True, exist_ok=True)

def safe_load_notebook(path: Path) -> dict:
    """Load notebook either as JSON or as Python dict repr."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        return json.loads(content)
    except Exception:
        return ast.literal_eval(content)

def clean_notebook(nb: dict) -> dict:
    """Create an unexecuted template copy with empty outputs and reset execution counts."""
    nb_clean = copy.deepcopy(nb)
    for cell in nb_clean.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            # Clean execution metadata if present
            if "metadata" in cell and "execution" in cell["metadata"]:
                del cell["metadata"]["execution"]
    return nb_clean

print("--- 1. Standardizing bench/notebooks/04_eval_paddleocr.ipynb & 05_eval_easyocr.ipynb ---")
# 04 PaddleOCR
nb04_raw = safe_load_notebook(NOTEBOOKS_DIR / "04_eval_paddleocr.ipynb")
nb04_clean = clean_notebook(nb04_raw)
with open(NOTEBOOKS_DIR / "04_eval_paddleocr.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb04_clean, f, indent=1, ensure_ascii=False)
print("  [SAVED] bench/notebooks/04_eval_paddleocr.ipynb (clean template, valid JSON)")

# Save executed 04 in executed/
with open(EXECUTED_DIR / "04_eval_paddleocr_executed.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb04_raw, f, indent=1, ensure_ascii=False)
print("  [SAVED] bench/notebooks/executed/04_eval_paddleocr_executed.ipynb (valid JSON)")

# 05 EasyOCR
nb05_raw = safe_load_notebook(NOTEBOOKS_DIR / "05_eval_easyocr.ipynb")
nb05_clean = clean_notebook(nb05_raw)
with open(NOTEBOOKS_DIR / "05_eval_easyocr.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb05_clean, f, indent=1, ensure_ascii=False)
print("  [SAVED] bench/notebooks/05_eval_easyocr.ipynb (clean template, valid JSON)")

# Save executed 05 in executed/
with open(EXECUTED_DIR / "05_eval_easyocr_executed.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb05_raw, f, indent=1, ensure_ascii=False)
print("  [SAVED] bench/notebooks/executed/05_eval_easyocr_executed.ipynb (valid JSON)")

print("\n--- 2. Syncing & Standardizing Executed Notebooks from Lab ---")
lab_exec = LAB_DIR / "executed_notebooks"

# 01 Qwen2.5-VL
qwen_exec_src = lab_exec / "01_eval_qwen2_5_vl_3b_executed.ipynb"
if qwen_exec_src.exists():
    nb01 = safe_load_notebook(qwen_exec_src)
    with open(EXECUTED_DIR / "01_eval_qwen2_5_vl_3b_executed.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb01, f, indent=1, ensure_ascii=False)
    print("  [SYNCED] 01_eval_qwen2_5_vl_3b_executed.ipynb")

# 02 GOT-OCR 2.0
got_exec_src = lab_exec / "02_eval_got_ocr_2_0_executed.ipynb"
if got_exec_src.exists():
    nb02 = safe_load_notebook(got_exec_src)
    with open(EXECUTED_DIR / "02_eval_got_ocr_2_0_executed.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb02, f, indent=1, ensure_ascii=False)
    print("  [SYNCED] 02_eval_got_ocr_2_0_executed.ipynb")

# 03 SmolVLM
smol_exec_src = lab_exec / "03_eval_smolvlm_executed_checkpoint.ipynb"
if smol_exec_src.exists():
    nb03 = safe_load_notebook(smol_exec_src)
    with open(EXECUTED_DIR / "03_eval_smolvlm_executed.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb03, f, indent=1, ensure_ascii=False)
    # Also fix the one in Lab/executed_notebooks so it's valid JSON
    with open(smol_exec_src, "w", encoding="utf-8") as f:
        json.dump(nb03, f, indent=1, ensure_ascii=False)
    print("  [SYNCED & FIXED] 03_eval_smolvlm_executed.ipynb")

print("\n--- 3. Formatted and Validated Templates ---")
for p in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
    nb = safe_load_notebook(p)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"  [FORMATTED] {p.name}")

# Baseline notebook
base_nb = BENCH_DIR / "OPRB_Qwen2_5_VL_3B_Test_Evaluation.ipynb"
if base_nb.exists():
    nb_base = safe_load_notebook(base_nb)
    with open(base_nb, "w", encoding="utf-8") as f:
        json.dump(nb_base, f, indent=1, ensure_ascii=False)
    print(f"  [FORMATTED] {base_nb.name}")

print("\nDone standardizing notebooks.")
