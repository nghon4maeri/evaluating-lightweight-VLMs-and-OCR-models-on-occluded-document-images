import ast
import json
import re
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS = sorted(list(BENCH_DIR.rglob("*.ipynb")))

print(f"=================================================================")
print(f" COMPLETE AUDIT OF NOTEBOOKS IN BENCHMARK REPOSITORY ({len(NOTEBOOKS)} files)")
print(f"=================================================================\n")

audit_results = []

for nb_path in NOTEBOOKS:
    rel_path = nb_path.relative_to(BENCH_DIR)
    info = {
        "file": str(rel_path),
        "size_kb": round(nb_path.stat().st_size / 1024, 1),
        "json_valid": False,
        "nbformat": "",
        "total_cells": 0,
        "code_cells": 0,
        "md_cells": 0,
        "executed_cells": 0,
        "syntax_errors": [],
        "has_colab_support": False,
        "has_kaggle_support": False,
        "has_metrics_def": False,
        "has_token_norm": False,
    }

    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
        info["json_valid"] = True
    except Exception as e:
        info["error"] = str(e)
        audit_results.append(info)
        continue

    info["nbformat"] = f"v{nb.get('nbformat', '?')}.{nb.get('nbformat_minor', '?')}"
    cells = nb.get("cells", [])
    info["total_cells"] = len(cells)

    code_cells = [c for c in cells if c.get("cell_type") == "code"]
    md_cells = [c for c in cells if c.get("cell_type") == "markdown"]
    info["code_cells"] = len(code_cells)
    info["md_cells"] = len(md_cells)

    executed = [c for c in code_cells if c.get("outputs") and len(c["outputs"]) > 0]
    info["executed_cells"] = len(executed)

    all_source = ""
    for idx, c in enumerate(code_cells):
        src = "".join(c.get("source", []))
        all_source += "\n" + src
        clean_lines = [
            l if not l.strip().startswith(("%", "!")) else "pass"
            for l in src.splitlines()
        ]
        try:
            ast.parse("\n".join(clean_lines))
        except SyntaxError as se:
            info["syntax_errors"].append((idx + 1, se.msg, se.lineno))

    info["has_colab_support"] = "/content" in all_source or "google.colab" in all_source
    info["has_kaggle_support"] = "/kaggle" in all_source
    info["has_metrics_def"] = "cer(" in all_source and "wer(" in all_source
    info["has_token_norm"] = "NFKC" in all_source or "casefold" in all_source

    audit_results.append(info)

for r in audit_results:
    print(f"File: {r['file']} ({r['size_kb']} KB)")
    print(f"  JSON Valid: {r['json_valid']} | Format: {r['nbformat']}")
    print(f"  Cells: {r['total_cells']} total ({r['code_cells']} code, {r['md_cells']} markdown)")
    print(f"  Execution: {r['executed_cells']} / {r['code_cells']} code cells have outputs")
    print(f"  Syntax: {'[PASS] All valid Python' if not r['syntax_errors'] else f'[FAIL] {r['syntax_errors']}'}")
    print(f"  Features: Colab={r['has_colab_support']} | Kaggle={r['has_kaggle_support']} | MetricsDef={r['has_metrics_def']} | TokenNorm={r['has_token_norm']}")
    print("-" * 65)

# Also check executed notebooks in ../Lab/executed_notebooks
lab_exec_dir = BENCH_DIR.parent / "Lab" / "executed_notebooks"
if lab_exec_dir.exists():
    print(f"\n=================================================================")
    print(f" AUDIT OF EXECUTED LOG NOTEBOOKS IN Lab/executed_notebooks")
    print(f"=================================================================\n")
    for exec_nb in sorted(lab_exec_dir.glob("*.ipynb")):
        with open(exec_nb, "r", encoding="utf-8") as f:
            nb_exec = json.load(f)
        c_code = [c for c in nb_exec["cells"] if c.get("cell_type") == "code"]
        c_out = [c for c in c_code if c.get("outputs") and len(c["outputs"]) > 0]
        print(f"{exec_nb.name} ({round(exec_nb.stat().st_size/1024, 1)} KB):")
        print(f"  Code cells with outputs: {len(c_out)} / {len(c_code)}")
