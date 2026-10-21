#!/usr/bin/env python3
"""Read-only container header and signature probe; no decryption."""
import argparse,json,hashlib
from pathlib import Path
def main():
    p=argparse.ArgumentParser()
    p.add_argument("file",type=Path)
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    h=hashlib.sha256()
    with a.file.open("rb") as f:
        header=f.read(4096);h.update(header)
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    signatures={"squashfs_le":b"hsqs","elf":b"\x7fELF","gzip":b"\x1f\x8b","zip":b"PK\x03\x04"}
    offsets={k:header.find(v) for k,v in signatures.items() if header.find(v)>=0}
    report={"file":a.file.name,"size":a.file.stat().st_size,"sha256":h.hexdigest(),"header_hex":header[:64].hex(),"known_header_signatures":offsets,"note":"Header heuristics do not validate or extract EPK/PAK containers."}
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
