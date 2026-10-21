#!/usr/bin/env python3
"""Read-only directory inventory; no firmware unpacking or flashing."""
import argparse, hashlib, json
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    root = a.directory.resolve(strict=True)
    if not root.is_dir():
        p.error("input must be a directory")
    files = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.is_symlink():
            continue
        s = f.stat()
        files.append({"path": f.relative_to(root).as_posix(), "size": s.st_size, "sha256": sha256(f)})
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({"schema": 1, "root_label": root.name, "files": files}, indent=2) + "\n")
    print(f"Inventoried {len(files)} files into {a.out}")

if __name__ == "__main__":
    main()
