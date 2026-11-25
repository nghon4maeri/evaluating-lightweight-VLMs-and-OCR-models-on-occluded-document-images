# Qualitative Case Studies (OPRB Benchmark)

## Sample: `Through_Dust__1p0pct__107.tar_1507.03120.gz_arxiv_23_ori`
- **Group:** best_transcription | **Category:** text | **Type:** Through_Dust @ 1p0pct
- **Ground Truth (first 250 chars):** `[42] Cordourier-Maruri, G., Gupta, V., and de Coss, R.: Recurrence in resonant trans- mission of the one-dimensional array of delta potetials, Mod. Phys. Lett. B, 28, 1450016 (2014) 24...`

| Model | CER | WER | Prediction (excerpt) |
| :--- | :---: | :---: | :--- |
| **PaddleOCR (PP-OCRv4)** | 0.000 | 0.000 | [42] Cordourier-Maruri, G., Gupta, V., and de Coss, R.: Recurrence in resonant trans- mission of the one-dimensional array of delta potetials, Mod. Phys. Lett. B, 28, 1450016 (2014... |
| **EasyOCR** | 0.130 | 0.483 | [42] Cordourier-Maruri. G  Gupta; V and de Coss, R:: Recurrence in resonant trans- mission of thcone-dlimeusional ATTAY of delta potetials Mod, Fhvs Lett. BS 228 1450016 (2014)... |
| **SmolVLM-Instruct** | 0.060 | 0.207 | Cordourier-Marui, G., Gupta, V., and de Coss, R.: Recurence in resonant trans- mission of the one-dimensional array of delta potentials, Mod. Phys. Lett. B, 28, 1450016 (2014).... |
| **GOT-OCR-2.0** | 0.005 | 0.034 | [42] Cordourier-Maruri, G., Gupta, V., and de Coss, R.: Recurrence in resonant trans- mission of the one-dimensional array of delta potentials, Mod. Phys. Lett. B, 28, 1450016 (201... |
| **Qwen2.5-VL-3B (4-bit)** | 0.033 | 0.138 | [42] Cordourier-Maruri, G., Gupta, V., and de Coss, R.: Recurrence in resonant transmission of the one-dimensional array of delta potentials, Mod. Phys. Lett. B, 28, 1450016 (2014)... |

---

## Sample: `White_Whitener__1p0pct__104.tar_1804.05908.gz_evg_pol_v3_23_ori`
- **Group:** best_transcription | **Category:** text | **Type:** White_Whitener @ 1p0pct
- **Ground Truth (first 250 chars):** `[BO99] C. M. Bender and S. A. Orszag. Advanced mathematical methods for scientists and engineers: I: Asymptotic methods and perturbation theory. Springer, 1999. [BP32] A. Bloch and G. Po´lya. On the Roots of Certain Algebraic Equations. Proc. London ...`

| Model | CER | WER | Prediction (excerpt) |
| :--- | :---: | :---: | :--- |
| **PaddleOCR (PP-OCRv4)** | 0.064 | 0.431 | [BO99] C.M.Bender and S.A.Orszag.Aduanced mathematical methods for scientists and engineers: I: Asymptotic methods and perturbation theory. Springer, 1999. [BP32] A.Bloch and G.Pol... |
| **EasyOCR** | 0.140 | 0.553 | [BO99] C.M; Beuder aud $ A. Orszag- Advanced mathematical methods for scientists and engincers: [: Asymptotic methods and perturbation thcory: Springer, 1999. [BP32] Bloch and G Po... |
| **SmolVLM-Instruct** | 0.074 | 0.159 | BO99 C. M. Bender and S. A. Orszag. Advanced mathematical methods for scientists and engineers: Asymptotic methods and perturbation theory. Springer, 1999. BP32 A. Bloch and G. P´o... |
| **GOT-OCR-2.0** | 0.021 | 0.084 | [BO99]  C. M. Bender and S. A. Orszag. Advanced mathematical methods for scientists  and engineers: I: Asymptotic methods and perturbation theory. Springer, 1999.  [BP32]  A. Bloch... |
| **Qwen2.5-VL-3B (4-bit)** | 0.019 | 0.169 | [BO99] C.M. Bender and S.A. Orszag. Advanced mathematical methods for scientists and engineers: I. Asymptotic methods and perturbation theory. Springer, 1999.  [BP32] A. Bloch and ... |

---

## Sample: `White_Burnt__1p0pct__102.tar_1408.2843.gz_D_asymmetry_8_ori`
- **Group:** severe_failure | **Category:** text | **Type:** White_Burnt @ 1p0pct
- **Ground Truth (first 250 chars):** `ex]]. 9...`

| Model | CER | WER | Prediction (excerpt) |
| :--- | :---: | :---: | :--- |
| **PaddleOCR (PP-OCRv4)** | 0.429 | 1.000 | exl].... |
| **EasyOCR** | 0.714 | 1.000 | exll:... |
| **SmolVLM-Instruct** | 0.857 | 1.000 | wall.... |
| **GOT-OCR-2.0** | 134.000 | 32.000 | \begin{tikzpicture} \draw[line width=1.04pt,color=brown,opacity=0.3] (-2.56,0.79) -- (0.85,0.79);     \draw[line width=1.04pt,color=brown,opacity=0.3] (-2.56,0.79) -- (-0.99,4.58);... |
| **Qwen2.5-VL-3B (4-bit)** | 0.429 | 1.000 | ex].... |

---

## Sample: `Through_Dust__1p0pct__107.tar_1408.5358.gz_generalized_cox_rings_43_ori`
- **Group:** severe_failure | **Category:** text | **Type:** Through_Dust @ 1p0pct
- **Ground Truth (first 250 chars):** `44 ULRICH DERENTHAL AND MARTA PIEROPAN...`

| Model | CER | WER | Prediction (excerpt) |
| :--- | :---: | :---: | :--- |
| **PaddleOCR (PP-OCRv4)** | 0.079 | 0.167 | ULRICH DERENTHAL AND MARTA PIEROPAN... |
| **EasyOCR** | 0.211 | 0.667 | ULRICT DERENTHAL At MAFETA PIEROPAN... |
| **SmolVLM-Instruct** | 26.842 | 0.833 | 44 111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111... |
| **GOT-OCR-2.0** | 0.026 | 0.167 | 44  UlRICH DlRENTHAL AND MARTA PIEROPAN... |
| **Qwen2.5-VL-3B (4-bit)** | 0.026 | 0.167 | 44 ULRICH DERNENTHAL AND MARTA PIEROPAN... |

---
