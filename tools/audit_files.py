"""Check tracked delivery files, source syntax, JSON, and evidence hashes."""
import ast
import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
from urllib.parse import unquote


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args=parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
    paths = [root / name for name in paths if name]
    counts = {"files": len(paths), "python": 0, "json": 0, "jsonl": 0, "evidence_images": 0}
    for path in paths:
        if not path.is_file():
            raise ValueError(f"Missing tracked file: {path.relative_to(root)}")
        if path.suffix.lower() in {".exe", ".dll", ".pyd", ".zip", ".whl"}:
            raise ValueError(f"Forbidden delivery artifact: {path.name}")
        if path.suffix == ".py":
            text = path.read_text(encoding="utf-8-sig")
            ast.parse(text, filename=str(path))
            if path.relative_to(root).parts[0] == "src" and any(mark in text for mark in ("TÃ¼rk", "yanÄ±t", "araÅŸ")):
                raise ValueError(f"Broken Turkish encoding: {path.name}")
            counts["python"] += 1
        elif path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8-sig")); counts["json"] += 1
        elif path.suffix == ".jsonl":
            for line in path.read_text(encoding="utf-8-sig").splitlines():
                if line.strip(): json.loads(line)
            counts["jsonl"] += 1
        elif path.suffix.lower() in {".jpg", ".png"}:
            signature = b"\xff\xd8\xff" if path.suffix == ".jpg" else b"\x89PNG\r\n\x1a\n"
            if not path.read_bytes().startswith(signature): raise ValueError(path.name)
            counts["evidence_images"] += 1
        elif path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)",path.read_text(encoding="utf-8-sig")):
                local=target.strip("<>").split("#")[0]
                if not local or "://" in local or local.startswith(("mailto:","C:","/")):
                    continue
                if not (path.parent/unquote(local)).exists():
                    raise ValueError(f"Broken local link in {path.relative_to(root)}: {target}")
    hashes = json.loads((root / "SHA256SUMS.json").read_text(encoding="utf-8"))
    for name, expected in hashes.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"File hash mismatch: {name}")
    manifest=json.loads((root/"oracle/sude_screenshots/manifest.json").read_text(encoding="utf-8"))
    for record in manifest["records"]:
        if hashlib.sha256((root/record["file"]).read_bytes()).hexdigest()!=record["sha256"]:
            raise ValueError(record["id"])
    for line in (root/"oracle/new_validation/vectors.jsonl").read_text(encoding="utf-8").splitlines():
        record=json.loads(line); evidence=record["evidence"]
        if hashlib.sha256((root/evidence["screenshot"]).read_bytes()).hexdigest()!=evidence["screenshot_sha256"]:
            raise ValueError(record["id"])
    result={"status":"passed", **counts, "file_hashes_checked":len(hashes)}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
