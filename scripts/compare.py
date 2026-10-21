#!/usr/bin/env python3
"""Compare two file inventories without needing firmware binaries."""
import argparse, json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("baseline", type=Path)
    p.add_argument("donor", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    left = json.loads(a.baseline.read_text())
    right = json.loads(a.donor.read_text())
    if left.get("schema") != 1 or right.get("schema") != 1:
        p.error("unsupported inventory schema")
    x = {f["path"]: f for f in left["files"]}
    y = {f["path"]: f for f in right["files"]}
    result = {
        "baseline": left.get("root_label"),
        "donor": right.get("root_label"),
        "added": sorted(y.keys() - x.keys()),
        "removed": sorted(x.keys() - y.keys()),
        "changed": sorted(k for k in x.keys() & y.keys() if x[k]["sha256"] != y[k]["sha256"]),
        "unchanged": sorted(k for k in x.keys() & y.keys() if x[k]["sha256"] == y[k]["sha256"]),
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2) + "\n")
    print({k: len(v) for k, v in result.items() if isinstance(v, list)})

if __name__ == "__main__":
    main()
