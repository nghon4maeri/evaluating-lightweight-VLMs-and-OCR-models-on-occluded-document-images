import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(r"D:\User\nghonamjiwoo\Natural Language Processing\Lab")
RESULTS_DIR = BASE_DIR / "colab_results"
OUTPUT_DIR = BASE_DIR / "benchmark_synthesis_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
})
sns.set_theme(style="whitegrid")

SPECS = [
    {
        "model": "PaddleOCR (PP-OCRv4)",
        "type": "OCR Pipeline",
        "params_m": 12.0,
        "path": RESULTS_DIR / "paddleocr_ppocrv4_results" / "per_image_results.csv",
    },
    {
        "model": "EasyOCR",
        "type": "OCR Pipeline",
        "params_m": 25.0,
        "path": RESULTS_DIR / "easyocr_results" / "per_image_results.csv",
    },
    {
        "model": "SmolVLM-Instruct",
        "type": "VLM",
        "params_m": 2200.0,
        "path": RESULTS_DIR / "smolvlm_instruct_results" / "per_image_results.csv",
    },
    {
        "model": "GOT-OCR-2.0",
        "type": "VLM (OCR-spec)",
        "params_m": 580.0,
        "path": RESULTS_DIR / "got_ocr_2_0_results" / "got_ocr_2_0_results" / "per_image_results.csv",
    },
    {
        "model": "Qwen2.5-VL-3B (4-bit)",
        "type": "VLM",
        "params_m": 3000.0,
        "path": RESULTS_DIR / "qwen2_5_vl_3b_results" / "qwen2_5_vl_3b_results" / "per_image_results.csv",
    },
]

frames = []
for s in SPECS:
    if not s["path"].exists():
        print(f"Missing {s['model']} at {s['path']}")
        continue
    df = pd.read_csv(s["path"])
    ok = df[df["status"] == "ok"].copy()
    ok["model"] = s["model"]
    ok["model_type"] = s["type"]
    ok["params_m"] = s["params_m"]
    frames.append(ok)
    print(f"Loaded {s['model']}: {len(ok):,} valid evaluations.")

all_df = pd.concat(frames, ignore_index=True)
print(f"\nTotal combined evaluations: {len(all_df):,}")

# 1. Summary comparison table
summary_df = (
    all_df.groupby(["model", "model_type", "params_m"], as_index=False)
    .agg(
        evaluated_pages=("sample_id", "count"),
        macro_cer=("cer", "mean"),
        macro_wer=("wer", "mean"),
        macro_precision=("token_precision", "mean"),
        macro_recall=("token_recall", "mean"),
        macro_f1=("token_f1", "mean"),
        mean_latency_sec=("latency_sec", "mean"),
    )
    .sort_values("macro_cer", ascending=True)
)
summary_df.to_csv(OUTPUT_DIR / "summary_comparison_table.csv", index=False)
print("\n=== SUMMARY COMPARISON TABLE ===")
print(summary_df.to_string(index=False))

# 2. Text vs Nontext table
cat_df = (
    all_df.groupby(["model", "model_type", "category"], as_index=False)
    .agg(
        n=("sample_id", "count"),
        mean_cer=("cer", "mean"),
        mean_wer=("wer", "mean"),
        mean_f1=("token_f1", "mean"),
        mean_latency=("latency_sec", "mean"),
    )
)
cat_df.to_csv(OUTPUT_DIR / "summary_by_category_all_models.csv", index=False)

# 3. Figure 1: Overall Performance (CER & WER)
fig, ax = plt.subplots(figsize=(9, 4.8))
melted_overall = summary_df.melt(
    id_vars="model", value_vars=["macro_cer", "macro_wer"],
    var_name="Metric", value_name="Error Rate"
)
melted_overall["Metric"] = melted_overall["Metric"].map({"macro_cer": "CER", "macro_wer": "WER"})
sns.barplot(data=melted_overall, x="model", y="Error Rate", hue="Metric", ax=ax, palette="muted")
ax.set_title("Overall OPRB Test Performance: Macro CER & WER (Lower is Better)")
ax.set_xlabel("")
ax.set_ylabel("Error Rate")
ax.tick_params(axis="x", rotation=15)
plt.tight_layout()
fig1_path = OUTPUT_DIR / "fig1_overall_performance.png"
plt.savefig(fig1_path, dpi=300)
plt.close()
print(f"Saved: {fig1_path}")

# 4. Figure 2: Text vs Nontext Degradation
fig, ax = plt.subplots(figsize=(9, 4.8))
sns.barplot(data=cat_df, x="model", y="mean_cer", hue="category", ax=ax, palette="Set2")
ax.set_title("Text-Region vs Non-Text-Region Occlusion Impact (Mean CER)")
ax.set_xlabel("")
ax.set_ylabel("Mean CER (Lower is Better)")
ax.tick_params(axis="x", rotation=15)
plt.tight_layout()
fig2_path = OUTPUT_DIR / "fig2_text_vs_nontext.png"
plt.savefig(fig2_path, dpi=300)
plt.close()
print(f"Saved: {fig2_path}")

# 5. Figure 3: Robustness across Occlusion Densities & Types
import re
def extract_clean_meta(stem):
    m_dens = re.search(r"(\d+p\d+|\d+)pct", str(stem))
    dens = f"{m_dens.group(1).replace('p', '.')}%" if m_dens else None
    raw_type = str(stem).split("__")[0]
    type_map = {
        "White_Burnt": "Burnt",
        "White_Whitener": "Fluid",
        "Through_Dust": "Dust",
        "Through_Stamp": "Stamp",
        "Black_Ink": "Ink",
        "Sim": "Sim",
    }
    return type_map.get(raw_type, raw_type), dens

meta_tuples = [extract_clean_meta(s) for s in all_df["sample_id"]]
all_df["clean_type"] = [t[0] for t in meta_tuples]
all_df["clean_density"] = [t[1] for t in meta_tuples]

fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4), dpi=300)
model_palette = {
    "PaddleOCR (PP-OCRv4)": "#1f77b4",
    "Qwen2.5-VL-3B (4-bit)": "#ff7f0e",
    "EasyOCR": "#2ca02c",
    "GOT-OCR-2.0": "#d62728",
    "SmolVLM-Instruct": "#9467bd",
}
model_markers = {
    "PaddleOCR (PP-OCRv4)": "o",
    "Qwen2.5-VL-3B (4-bit)": "s",
    "EasyOCR": "^",
    "GOT-OCR-2.0": "D",
    "SmolVLM-Instruct": "v",
}

# Subplot (a): CER across densities
dens_valid = all_df[all_df["clean_density"].isin(["0.5%", "1.0%", "2.0%"])].copy()
dens_summary = dens_valid.groupby(["model", "clean_density"], as_index=False)["cer"].mean()
dens_summary["dens_num"] = dens_summary["clean_density"].str.replace("%", "").astype(float)
dens_summary = dens_summary.sort_values(["model", "dens_num"])

for model, grp in dens_summary.groupby("model"):
    axes[0].plot(
        grp["clean_density"],
        grp["cer"],
        marker=model_markers.get(model, "o"),
        linewidth=1.8,
        markersize=5.5,
        label=model,
        color=model_palette.get(model, "gray"),
    )

axes[0].set_title("(a) CER vs. Occlusion Density", fontweight="bold", fontsize=9.5, pad=6)
axes[0].set_xlabel("Occlusion Density", fontsize=8.5)
axes[0].set_ylabel("Macro CER (Lower is Better)", fontsize=8.5)
axes[0].set_ylim(0.2, 1.05)
axes[0].tick_params(labelsize=8)
axes[0].grid(True, linestyle="--", alpha=0.5)

# Subplot (b): CER across occlusion types
type_order = ["Burnt", "Fluid", "Dust", "Stamp", "Ink", "Sim"]
type_summary = all_df.groupby(["model", "clean_type"], as_index=False)["cer"].mean()

sns.barplot(
    data=type_summary,
    x="clean_type",
    y="cer",
    hue="model",
    order=type_order,
    palette=model_palette,
    ax=axes[1],
    edgecolor="black",
    linewidth=0.5,
)

axes[1].set_title("(b) CER vs. Occlusion Type", fontweight="bold", fontsize=9.5, pad=6)
axes[1].set_xlabel("Occlusion Modality", fontsize=8.5)
axes[1].set_ylabel("Macro CER (Lower is Better)", fontsize=8.5)
axes[1].set_ylim(0.2, 1.05)
axes[1].tick_params(labelsize=8)
axes[1].grid(True, linestyle="--", alpha=0.5, axis="y")
if axes[1].legend_:
    axes[1].legend_.remove()

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.03),
    ncol=5,
    frameon=True,
    facecolor="white",
    framealpha=0.9,
    edgecolor="#cccccc",
    fontsize=7.5,
)

plt.tight_layout(rect=[0, 0, 1, 0.94])
fig3_path = OUTPUT_DIR / "fig3_occlusion_robustness.png"
plt.savefig(fig3_path, dpi=300, bbox_inches="tight")
plt.savefig(BASE_DIR.parent / "bench" / "results" / "figures" / "fig3_occlusion_robustness.png", dpi=300, bbox_inches="tight")
plt.savefig(BASE_DIR.parent / "bench" / "report" / "figures" / "fig3_occlusion_robustness.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved: {fig3_path}")

# 6. Figure 4: Pareto Trade-off Frontier (Latency vs CER)
fig, ax = plt.subplots(figsize=(9, 5.2))
colors = {"OCR Pipeline": "#1f77b4", "VLM": "#ff7f0e", "VLM (OCR-spec)": "#2ca02c"}
for mtype, group in summary_df.groupby("model_type"):
    ax.scatter(
        group["mean_latency_sec"],
        group["macro_cer"],
        s=group["params_m"].clip(lower=20) * 0.35,
        alpha=0.75,
        edgecolors="black",
        linewidths=1.2,
        label=mtype,
        color=colors.get(mtype, "gray")
    )
for _, row in summary_df.iterrows():
    ax.annotate(
        f"{row['model']} ({row['params_m']:.0f}M)",
        (row["mean_latency_sec"], row["macro_cer"]),
        textcoords="offset points",
        xytext=(8, 4),
        fontsize=9,
        fontweight="bold"
    )
ax.set_title("Efficiency Pareto Frontier: Inference Latency vs Macro CER")
ax.set_xlabel("Mean Inference Latency (seconds / document page)")
ax.set_ylabel("Macro CER (Lower is Better)")
ax.legend(title="Model Category")
plt.tight_layout()
fig4_path = OUTPUT_DIR / "fig4_pareto_tradeoff.png"
plt.savefig(fig4_path, dpi=300)
plt.close()
print(f"Saved: {fig4_path}")

# 7. Qualitative Case Studies Extraction
pivot_cer = all_df.pivot_table(index="sample_id", columns="model", values="cer", aggfunc="mean")
meta_cols = (
    all_df[["sample_id", "category", "occlusion_type", "occlusion_density", "ground_truth"]]
    .drop_duplicates("sample_id")
    .set_index("sample_id")
)
case_pool = meta_cols.join(pivot_cer).dropna()
case_pool["avg_cer"] = case_pool[summary_df["model"].tolist()].mean(axis=1)

best_ids = case_pool.nsmallest(2, "avg_cer").index.tolist()
worst_ids = case_pool[case_pool["category"] == "text"].nlargest(2, "avg_cer").index.tolist()
selected_ids = best_ids + worst_ids

cases_df = all_df[all_df["sample_id"].isin(selected_ids)].copy()
cases_df["case_group"] = np.where(cases_df["sample_id"].isin(best_ids), "best_transcription", "severe_failure")
cases_df.to_csv(OUTPUT_DIR / "qualitative_case_studies.csv", index=False)

md_lines = ["# Qualitative Case Studies (OPRB Benchmark)\n"]
for sid in selected_ids:
    sub = cases_df[cases_df["sample_id"] == sid]
    first = sub.iloc[0]
    md_lines.append(f"## Sample: `{sid}`")
    md_lines.append(f"- **Group:** {first['case_group']} | **Category:** {first['category']} | **Type:** {first['occlusion_type']} @ {first['occlusion_density']}")
    md_lines.append(f"- **Ground Truth (first 250 chars):** `{str(first['ground_truth'])[:250]}...`\n")
    md_lines.append("| Model | CER | WER | Prediction (excerpt) |")
    md_lines.append("| :--- | :---: | :---: | :--- |")
    for _, r in sub.iterrows():
        pred_clean = str(r["prediction"]).replace("\n", " ").strip()[:180]
        md_lines.append(f"| **{r['model']}** | {r['cer']:.3f} | {r['wer']:.3f} | {pred_clean}... |")
    md_lines.append("\n---\n")

case_md_path = OUTPUT_DIR / "qualitative_case_studies.md"
case_md_path.write_text("\n".join(md_lines), encoding="utf-8")
print(f"Saved: {case_md_path}")
print("\nALL SYNTHESIS ARTIFACTS SUCCESSFULLY GENERATED!")
