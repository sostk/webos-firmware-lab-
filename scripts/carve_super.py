#!/usr/bin/env python3
"""Read-only, bounds-checked carving from an already extracted super.pak.
Requires explicit JSON extent plan; never guesses offsets or writes to devices.
"""
import argparse, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--super",type=Path,required=True)
    p.add_argument("--plan",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--execute",action="store_true",help="Actually write carved files; default dry-run")
    a=p.parse_args()
    if not a.super.is_file() or a.super.is_symlink(): p.error("super must be a regular file")
    data=json.loads(a.plan.read_text())
    if data.get("sector_size")!=512: p.error("plan must specify sector_size=512")
    entries=data.get("partitions",[])
    if not isinstance(entries,list) or not entries: p.error("nonempty partitions required")
    size=a.super.stat().st_size
    checked=[]; spans=[]
    for e in entries:
        name=e["name"]; start=e["start_sector"]; count=e["sector_count"]
        if not isinstance(name,str) or not name.isascii() or not name.replace("_","").replace("-","").isalnum() or name in (".",".."):
            p.error("invalid partition name")
        if type(start)!=int or type(count)!=int or start<0 or count<=0: p.error("invalid extent")
        offset=start*512; length=count*512
        if offset+length>size: p.error(f"{name}: extent exceeds super file")
        spans.append((offset,offset+length,name))
        checked.append((name,offset,length))
    spans.sort()
    for a1,b1 in zip(spans,spans[1:]):
        if a1[1]>b1[0]: p.error(f"overlapping extents: {a1[2]}, {b1[2]}")
    print(json.dumps({"source":str(a.super),"bytes":size,"dry_run":not a.execute,"partitions":[{"name":n,"offset":o,"length":l} for n,o,l in checked]},indent=2))
    if not a.execute: return
    a.outdir.mkdir(parents=True,exist_ok=True)
    with a.super.open("rb") as source:
        for name,offset,length in checked:
            dest=a.outdir/(name+".img")
            if dest.exists() or dest.is_symlink(): p.error(f"refusing to overwrite {dest}")
            with dest.open("xb") as output:
                source.seek(offset)
                remaining=length
                while remaining:
                    chunk=source.read(min(1024*1024,remaining))
                    if not chunk: raise IOError("unexpected EOF")
                    output.write(chunk);remaining-=len(chunk)
if __name__=="__main__":main()
