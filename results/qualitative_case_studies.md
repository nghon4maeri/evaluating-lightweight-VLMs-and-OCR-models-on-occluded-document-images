# Qualitative Case Studies (OPRB Benchmark)

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

## Sample: `Through_Stamp__110.tar_1804.08268.gz_General_Harmonic_0_ori`
- **Group:** best_transcription | **Category:** text | **Type:** Through_Stamp @ 110.tar_1804.08268.gz_General_Harmonic_0_ori
- **Ground Truth (first 250 chars):** `a) PACS numbers: Keywords: I. INTRODUCTION In recent years the massless Dirac equation in (2 + 1) dimensions has drawn a lot of interest. One of the main reason for this interest is that the dynamics of quasiparticles in materials like graphene is go...`

| Model | CER | WER | Prediction (excerpt) |
| :--- | :---: | :---: | :--- |
| **PaddleOCR (PP-OCRv4)** | 0.096 | 0.370 | PACS numbers: Keywords: I.INTRODUCTION In recent years the massless Dirac equation in (2 + 1) dimensions has drawn a lot of interest.One of the main reason for this interest is tha... |
| **EasyOCR** | 0.090 | 0.326 | PACS numbers; Keywords: INTRODUCTION In recent vears the massless Dirac equation in (2 + 1) dimensions has drawn lot of interest. One of the main reason for this interest is that t... |
| **SmolVLM-Instruct** | 0.121 | 0.196 | In recent years the massless Dirac equation in (2 + 1) dimensions has drawn a lot of interest. One of the main reasons for this interest is that the dynamics of quasiparticles in m... |
| **GOT-OCR-2.0** | 0.015 | 0.044 | a)  PACS numbers:  Keywords:  I. INTRODUCTION  In recent years the massless Dirac equation in (2 + 1) dimensions has drawn a lot of  interest. One of the main reason for this inter... |
| **Qwen2.5-VL-3B (4-bit)** | 0.090 | 0.282 | PACS numbers:  Keywords:  I. INTRODUCTION  In recent years the massless Dirac equation in (2+1) dimensions has drawn a lot of interest. One of the main reason for this interest is ... |

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

## Sample: `Through_Stamp__111.tar_1507.04951.gz_comb_model_arxiv_96_ori`
- **Group:** severe_failure | **Category:** text | **Type:** Through_Stamp @ 111.tar_1507.04951.gz_comb_model_arxiv_96_ori
- **Ground Truth (first 250 chars):** `(cid:90) (cid:88) (cid:88) where we deﬁne (cid:90) A = (cid:88) (cid:88) W ω¯ \ m G L L(D) M (G,[K])∈SRm D∈Dec(G,L) (G,[K])(p) g,k,l ∗ S = W s Φ¯ \ , m G L L(D) M (G,[K])∈SRm D∈Dec(G,L) ∂ (p)(G,[K]) g,k,l and s is nowhere vanishing special canonical....`

| Model | CER | WER | Prediction (excerpt) |
| :--- | :---: | :---: | :--- |
| **PaddleOCR (PP-OCRv4)** | 0.438 | 0.680 | where we define WGWL\L(D) Am = ,DEDe(G,L) M(G[KD(P) (G,[K)ESR,. WGs*LNL(D) Sm= (G,[K)eSR, DeDe(G,L) JaM(P)(G,K) and s is nowhere vanishing special canonical. Wenowclaim Sm=Am+1+Sm+... |
| **EasyOCR** | 0.609 | 0.839 | where we clefine WGCL L(D) Am (G[KTesr  , DeDee(6L) MG[KD(P) Wcs" PLIL(D) . Smn (G khesr" _ De Dee(G,L) ` oM(p)G,n) uowhere vanishing special cahOnica: and Wc How claim Sm A,+l + S... |
| **SmolVLM-Instruct** | 2.707 | 2.931 | where we define where we define where we define where we define where we define where we define where we define where we define where we define where we define where we define wher... |
| **GOT-OCR-2.0** | 0.906 | 0.934 | where we define  Am =  Sm =  and s is nowhere vanishing special canonical.  We now claim  Indeed, consider Sm. Recall that for any G,  ∂M(G,[K]) =  [·]·]·]·]·]·]·]·]·]·]·]·]·]·]·]·... |
| **Qwen2.5-VL-3B (4-bit)** | 1.018 | 0.669 | where we define  \begin{equation} A_m = \sum_{(G,K) \in \mathcal{S}\mathcal{R}^{m}_{g,k,j}} \sum_{D \in \text{Dec}(G,L)} \int_{\mathcal{M}_{(G,K)}(p)} W_G \tilde{\omega}_{L}(D) \en... |

---
