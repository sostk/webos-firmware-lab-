#!/usr/bin/env python3
"""Explicit-URL firmware download. Does not infer model compatibility."""
import argparse, hashlib, json, urllib.request
from pathlib import Path
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--url",required=True,help="Direct, manually verified official firmware URL")
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--expected-sha256",help="Known independent checksum, if available")
    a=p.parse_args()
    if not a.url.startswith("https://"):
        p.error("HTTPS URL required")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    tmp=a.output.with_name(a.output.name+".partial")
    h=hashlib.sha256()
    try:
        req=urllib.request.Request(a.url,headers={"User-Agent":"webos-firmware-lab/0.1"})
        with urllib.request.urlopen(req,timeout=90) as response, tmp.open("wb") as out:
            final=response.geturl()
            if not final.startswith("https://"):
                raise ValueError("Redirected to non-HTTPS URL")
            for block in iter(lambda:response.read(1024*1024),b""):
                h.update(block);out.write(block)
        digest=h.hexdigest()
        if a.expected_sha256 and digest.lower()!=a.expected_sha256.lower():
            raise ValueError("SHA-256 mismatch")
        tmp.replace(a.output)
        metadata={"source_url":a.url,"sha256":digest,"bytes":a.output.stat().st_size,"file":a.output.name}
        a.output.with_suffix(a.output.suffix+".metadata.json").write_text(json.dumps(metadata,indent=2)+"\n")
        print(json.dumps(metadata,indent=2))
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
if __name__=="__main__":
    main()
