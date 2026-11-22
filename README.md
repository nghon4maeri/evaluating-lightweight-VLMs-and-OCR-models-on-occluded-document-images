# Evaluating Lightweight Vision-Language and OCR Models on Occluded Document Images

> **Course:** Natural Language Processing (CSC15006)  
> **Benchmark Dataset:** [OPRB – Occluded Pages Restoration Benchmark](https://huggingface.co/datasets/kpurkayastha/OPRB)  
> **Evaluation Mode:** Zero-shot Pretrained Inference (Strictly No Fine-tuning on Test Split)  
> **Total Evaluated Pages:** 22,103 document pages across 5 representative architectures  

---

## Overview & Objective

This repository contains the complete experimental code, evaluation pipelines, quantitative summaries, publication figures, and technical report for benchmarking lightweight **Vision-Language Models (VLMs)** and **Traditional/Pipeline OCR Engines** on heavily occluded document images.

Documents in real-world digitization pipelines often suffer from physical and digital degradations:
- **Text-region occlusions:** Ink marks, stamps, correction fluid (`White_Whitener`), scratches, burns (`White_Burnt`).
- **Non-text-region occlusions:** Dust, border ink spots, margins stamps.

This benchmark evaluates **transcription fidelity** (CER, WER, Bag-of-Words F1) and **computational efficiency** (inference latency, parameter count, memory footprint).

---

## Benchmark Summary Results

Evaluated across **22,103 pages** on NVIDIA GPU hardware:

| Model | Category | Parameters | Evaluated Pages | Macro CER ↓ | Macro WER ↓ | Token Prec. ↑ | Token Rec. ↑ | Token F1 ↑ | Mean Latency ↓ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PaddleOCR (PP-OCRv4)** | OCR Pipeline | **12.0M** | **9,000** (Full Test) | **0.3956** | 0.6174 | 0.7560 | 0.4502 | 0.5487 | **1.14s / page** |
| **Qwen2.5-VL-3B (4-bit)** | Generalist VLM | 3,000.0M | 736 | 0.4729 | **0.5712** | **0.7803** | **0.5590** | **0.6309** | 102.99s / page |
| **EasyOCR** | OCR Pipeline | 25.0M | **9,000** (Full Test) | 0.5822 | 0.8184 | 0.4387 | 0.3014 | 0.3501 | **2.54s / page** |
| **GOT-OCR-2.0** | VLM (OCR-spec) | 580.0M | 2,208 | 0.6788 | 0.8501 | 0.6159 | 0.4332 | 0.4765 | 33.88s / page |
| **SmolVLM-Instruct** | Lightweight VLM | 2,200.0M | 1,159 | 0.8782 | 0.9543 | 0.6212 | 0.1778 | 0.2183 | 10.92s / page |

### Core Findings & Pareto Trade-offs
1. **Speed vs. Reasoning Trade-off:**
   - **PaddleOCR** achieves the lowest CER (0.3956) and is **90x faster** than Qwen (1.14s vs. 103s) because its two-stage DBNet detector crops isolated text lines before recognition.
   - **Qwen2.5-VL-3B** achieves the lowest WER (0.5712) and highest Token F1 (0.6309) by leveraging strong linguistic priors from its 3B LLM backbone to reconstruct occluded words from context.
2. **Failure Modes:**
   - **SmolVLM** can fall into repetitive decoding loops (`"where we define where we define..."`) when occlusions interrupt grammatical flow.
   - **GOT-OCR-2.0** tends to hallucinate LaTeX TikZ plotting environments (`\begin{tikzpicture}`) when formulas are damaged.
   - **Traditional OCR (EasyOCR)** suffers from character fragmentation when occlusions break continuous stroke contours.

---

## Repository Structure

```
bench/
├── README.md                                  # Complete benchmark documentation
├── requirements.txt                           # Python dependencies
├── .gitignore                                 # Git ignore configuration
├── LabOCR.pdf                                 # Official assignment guidelines (local only, git-ignored)
├── OPRB_Qwen2_5_VL_3B_Test_Evaluation.ipynb   # Baseline evaluation reference (unexecuted template)
├── notebooks/                                 # Clean runnable evaluation templates (0 outputs)
│   ├── 01_eval_qwen2_5_vl_3b.ipynb            # Qwen2.5-VL-3B (4-bit NF4) evaluation template
│   ├── 02_eval_got_ocr_2_0.ipynb              # GOT-OCR-2.0 evaluation template
│   ├── 03_eval_smolvlm.ipynb                  # SmolVLM-Instruct evaluation template
│   ├── 04_eval_paddleocr.ipynb                # PaddleOCR PP-OCRv4 evaluation template
│   ├── 05_eval_easyocr.ipynb                  # EasyOCR evaluation template
│   ├── 06_benchmark_synthesis.ipynb           # Cross-model synthesis & figure generation template
│   └── executed/                              # Fully executed notebooks with outputs, tables & charts
│       ├── 01_eval_qwen2_5_vl_3b_executed.ipynb
│       ├── 02_eval_got_ocr_2_0_executed.ipynb
│       ├── 03_eval_smolvlm_executed.ipynb
│       ├── 04_eval_paddleocr_executed.ipynb
│       ├── 05_eval_easyocr_executed.ipynb
│       └── 06_benchmark_synthesis_executed.ipynb
├── scripts/
│   ├── audit_notebooks.py                     # Automated auditor verifying JSON validity & AST syntax
│   ├── standardize_all_notebooks.py           # Formats & synchronizes clean templates and executed logs
│   └── benchmark_synthesis.py                 # Standalone script generating 300 DPI figures
├── results/
│   ├── summary_comparison_table.csv           # Macro performance metrics across 5 models
│   ├── summary_by_category_all_models.csv     # Breakdown by Text vs. Non-Text occlusions
│   ├── qualitative_case_studies.md            # Detailed case studies (Success & Failure modes)
│   ├── qualitative_case_studies.csv           # Raw predictions of qualitative cases
│   └── figures/                               # 300 DPI publication plots
│       ├── fig1_overall_performance.png       # Macro CER and WER comparison
│       ├── fig2_text_vs_nontext.png           # Performance degradation under text vs. non-text
│       ├── fig3_occlusion_robustness.png      # Robustness across densities & occlusion types
│       └── fig4_pareto_tradeoff.png           # Efficiency Pareto frontier (Latency vs. CER)
└── report/                                    # Technical report folder (local only, git-ignored)
    ├── report.tex                             # IEEE-style 2-column LaTeX report (< 4 A4 pages)
    ├── report.pdf                             # Compiled final PDF report (3 A4 pages)
    └── figures/                               # Embedded figures for LaTeX compilation
```

---


## How to Reproduce

### 1. Installation
```bash
git clone <repo-url>
cd bench
pip install -r requirements.txt
```

### 2. Dataset Setup
Download and unpack the OPRB test split from Hugging Face:
```python
from huggingface_hub import hf_hub_download
import tarfile

# Downloads test/text/img.tar.gz and test/text/gt.tar.gz
# Downloads test/nontext/img.tar.gz and test/nontext/gt.tar.gz
```
Store the extracted data under `../Lab/oprb_dataset/` or configure `DATA_ROOT` in the evaluation scripts.

### 3. Run Benchmark Synthesis & Generate Figures
To regenerate all summary tables and 300 DPI figures:
```bash
python scripts/benchmark_synthesis.py
```

### 4. Compile Technical Report (PDF)
Compile the LaTeX document into PDF using MiKTeX or TeX Live:
```bash
cd report
pdflatex -interaction=nonstopmode report.tex
pdflatex -interaction=nonstopmode report.tex
```
Output PDF is generated at `report/report.pdf` (strictly $\le 4$ A4 pages).
