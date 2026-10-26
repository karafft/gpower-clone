"""One-command local setup/checks. Never writes to GitHub or calls an LLM.

python tools/check_all.py --install
"""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Create local .venv and install project dependencies from package registry")
    parser.add_argument("--scale", action="store_true", help="Also regenerate independent statsmodels comparison")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    venv = root / ".venv"
    executable = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if args.install:
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        subprocess.run([str(executable), "-m", "pip", "install", ".[mcp,scale]"], cwd=root, check=True)
    if not executable.exists():
        parser.error("Local .venv missing; use --install, or run documented tests in your existing environment")
    commands = [
        ["-m", "gpower_clone", "--version"],
        ["-m", "unittest", "discover", "-s", "tests", "-v"],
        ["tests/test_differential.py", "public_vectors.jsonl", "--report", "tests/reports/local_public.json"],
        ["tests/test_differential.py", "oracle/sude_contract_compatible_vectors.jsonl", "--require-evidence", "--report", "tests/reports/local_sude58.json"],
    ]
    if args.scale:
        commands.append(["tools/generate_scale.py", "--output", "oracle/scale/local_statsmodels.jsonl"])
    for command in commands:
        subprocess.run([str(executable), *command], cwd=root, check=True)
    print("Local checks completed. Live LLM, GUI screenshots, and fresh external validation are separate.")


if __name__ == "__main__":
    main()
