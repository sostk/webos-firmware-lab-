#!/usr/bin/env python3
"""Parse explicit 'linear' extents from readable dpmeta text. No image carving."""
import argparse,json,re
from pathlib import Path
# Example: 0 3292320 linear /dev/block/... 2048
PATTERN=re.compile(r"(?<!\d)(\d+)\s+(\d+)\s+linear\s+(\S+)\s+(\d+)")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("metadata",type=Path,help="Readable dpmeta text or dpmeta.pak bytes")
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    raw=a.metadata.read_bytes().decode("latin-1")
    matches=[]
    for m in PATTERN.finditer(raw):
        logical,length,device,start=m.groups()
        matches.append({"logical_start_sector":int(logical),"sector_count":int(length),"backing_device":device,"physical_start_sector":int(start),"byte_offset_512":int(start)*512,"byte_length_512":int(length)*512})
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps({"schema":1,"sector_size_assumed":512,"extents":matches,"warning":"Unverified heuristic. Verify metadata, block device and sector size before any carving."},indent=2)+"\n")
    print(f"Found {len(matches)} candidate linear extents")
if __name__=="__main__":main()
