"""Independent continuous statsmodels comparison, NOT a G*Power oracle."""
import argparse
from datetime import datetime, timezone
from itertools import product
import json
import math
from pathlib import Path
import platform
import time

import statsmodels
from statsmodels.stats.power import TTestIndPower
from gpower_clone import analyze


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("oracle/scale/statsmodels_vectors.jsonl"))
    args = parser.parse_args()
    solver = TTestIndPower()
    started = time.perf_counter()
    rows = []
    for index, (d, alpha, power, ratio, tails) in enumerate(product(
            (.1, .2, .3, .5, .8, 1.2), (.01, .05, .1),
            (.6, .7, .8, .9, .95), (.5, 1., 1.7), (1, 2)), 1):
        inp = dict(test="t2-indep", mode="a-priori", tails=tails, d=d,
                   alpha=alpha, power=power, ratio=ratio)
        row = {"id": f"SCALE-{index:04d}", "source": "statsmodels continuous reference, NOT GPower or REA", "input": inp}
        try:
            continuous = float(solver.solve_power(effect_size=d, nobs1=None,
                               alpha=alpha, power=power, ratio=ratio,
                               alternative="larger" if tails == 1 else "two-sided"))
            if not math.isfinite(continuous):
                raise ValueError("Nonfinite continuous solution")
            engine = analyze(inp)
            post = float(solver.power(effect_size=d, nobs1=engine["n1"],
                         alpha=alpha, ratio=engine["n2"]/engine["n1"],
                         alternative="larger" if tails == 1 else "two-sided"))
            rounded_n1 = math.ceil(continuous)
            rounded_n2 = math.ceil(rounded_n1*ratio)
            row.update(statsmodels_n1_continuous=continuous,
                       continuous_ceil_n1=rounded_n1, continuous_ceil_n2=rounded_n2,
                       engine_output=engine,
                       statsmodels_power_at_engine_allocation=post,
                       power_abs_difference=abs(post-engine["actual_power"]),
                       naive_ceil_allocation_matches=(rounded_n1 == engine["n1"] and rounded_n2 == engine["n2"]),
                       status="ok")
        except Exception as exc:
            row.update(status="error", error=f"{type(exc).__name__}: {exc}")
        rows.append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False, allow_nan=False)+"\n" for row in rows), encoding="utf-8")
    good = [row for row in rows if row["status"] == "ok"]
    summary = dict(timestamp=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
                   statsmodels=statsmodels.__version__, total=len(rows), completed=len(good),
                   errors=len(rows)-len(good), seconds=time.perf_counter()-started,
                   max_power_abs_difference=max((row["power_abs_difference"] for row in good), default=None),
                   naive_ceil_differences=sum(not row["naive_ceil_allocation_matches"] for row in good),
                   interpretation="Independent library cross-check; no GPower observation or hidden-score claim")
    args.output.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
