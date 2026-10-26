"""External oracle runner; never generates its own expected values.

python tests/test_differential.py public_vectors.jsonl --report tests/reports/public.json
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time


def compare(actual, expected):
    differences = []
    for key, value in expected.items():
        if key not in actual:
            differences.append({"field": key, "expected": value, "reason": "missing"})
            continue
        got = actual[key]
        if isinstance(value, bool):
            equal = type(got) is bool and got == value
        elif isinstance(value, int):
            equal = type(got) is int and got == value
        elif isinstance(value, float):
            equal = (type(got) in (int, float) and math.isfinite(got)
                     and math.isclose(got, value, abs_tol=1e-6, rel_tol=1e-6))
        else:
            equal = got == value
        if not equal:
            differences.append({"field": key, "expected": value, "actual": got})
    return differences


def load_vectors(path):
    raw = path.read_text(encoding="utf-8-sig")
    if raw.lstrip().startswith("["):
        rows = json.loads(raw)
    else:
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if not isinstance(rows, list) or not rows:
        raise ValueError("Vector file must be a nonempty JSON array or JSONL")
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("input"), dict) or not isinstance(row.get("expected"), dict) or not row["expected"]:
            raise ValueError("Each vector requires input and nonempty expected objects")
    return rows


def source_digest(root):
    digest = hashlib.sha256()
    paths = sorted((root / "src").rglob("*.py")) + [root / "pyproject.toml"]
    for path in paths:
        if path.exists():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run(vectors, timeout=2.0, require_evidence=False):
    results = []
    for i, vector in enumerate(vectors):
        inp, expected = vector["input"], vector["expected"]
        result = {"id": vector.get("id", str(i)), "input": inp,
                  "expected": expected, "evidence": vector.get("evidence")}
        if inp.get("test") != "t2-indep":
            result.update(status="skipped", reason="Other family; excluded from numerical score")
            results.append(result)
            continue
        if require_evidence and not vector.get("evidence"):
            result.update(status="failed", reason="External evidence identifier required")
            results.append(result)
            continue
        command = [sys.executable, "-m", "gpower_clone"]
        for key, value in inp.items():
            command.extend(["--" + key, str(value)])
        started = time.perf_counter()
        try:
            proc = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
            result.update(seconds=time.perf_counter()-started, exit_code=proc.returncode,
                          stderr=proc.stderr)
            lines = proc.stdout.splitlines()
            if len(lines) != 1:
                raise ValueError("stdout must have exactly one JSON line")
            actual = json.loads(lines[0])
            if not isinstance(actual, dict):
                raise ValueError("stdout must be a JSON object")
            result["actual"] = actual
            errors_expected = "error" in expected
            differences = compare(actual, {k: v for k, v in expected.items() if k != "error"})
            valid_exit = proc.returncode != 0 if errors_expected else proc.returncode == 0
            if not valid_exit or (errors_expected and "error" not in actual):
                differences.append({"field": "exit/error", "reason": "Unexpected success/error state"})
            if proc.stderr:
                result["stderr_note"] = "Diagnostics present; review manually"
            result.update(status="passed" if not differences else "failed", differences=differences)
            n_fields = [key for key in ("n1", "n2", "n_total") if key in expected]
            if inp.get("mode") == "a-priori" and not errors_expected and n_fields:
                result["n_exact"] = (proc.returncode == 0 and all(
                    type(actual.get(key)) is int and actual[key] == expected[key] for key in n_fields))
        except (subprocess.TimeoutExpired, ValueError, OSError) as exc:
            result.update(status="failed", reason=str(exc), seconds=time.perf_counter()-started)
            if inp.get("mode") == "a-priori" and "error" not in expected and any(k in expected for k in ("n1", "n2", "n_total")):
                result["n_exact"] = False
        results.append(result)
    n_results = [item["n_exact"] for item in results if "n_exact" in item]
    return {"timestamp": datetime.now(timezone.utc).isoformat(),
            "scope": "Only supplied external expected values; not a hidden competition score or REA proof",
            "total": len(results), "passed": sum(r["status"] == "passed" for r in results),
            "failed": sum(r["status"] == "failed" for r in results),
            "skipped": sum(r["status"] == "skipped" for r in results),
            "a_priori_n_cases": len(n_results),
            "a_priori_n_exact_rate": sum(n_results)/len(n_results) if n_results else None,
            "timeout_seconds": timeout, "results": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vectors", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--require-evidence", action="store_true")
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and positive")
    report = run(load_vectors(args.vectors), args.timeout, args.require_evidence)
    report["vectors_sha256"] = hashlib.sha256(args.vectors.read_bytes()).hexdigest()
    report["source_sha256"] = source_digest(Path(__file__).resolve().parents[1])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}))
    return 1 if report["failed"] or not report["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
