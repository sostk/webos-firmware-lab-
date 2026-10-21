#!/usr/bin/env python3
"""Read-only ELF metadata inventory. Never executes inspected files."""
import argparse, json, struct
from pathlib import Path

MACHINES={3:"x86",40:"ARM",62:"x86_64",183:"AArch64",8:"MIPS"}
def inspect(path):
    with path.open("rb") as f: h=f.read(64)
    if len(h)<20 or h[:4]!=b"\x7fELF": return None
    bits={1:32,2:64}.get(h[4])
    endian={1:"little",2:"big"}.get(h[5])
    if not bits or not endian: return {"error":"invalid ELF identification"}
    machine=int.from_bytes(h[18:20],endian)
    return {"bits":bits,"endian":endian,"machine":machine,"architecture":MACHINES.get(machine,"unknown"),"type":int.from_bytes(h[16:18],endian)}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("directory",type=Path)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    root=a.directory.resolve(strict=True)
    if not root.is_dir(): p.error("directory required")
    results=[]
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.is_symlink(): continue
        try:
            info=inspect(f)
            if info is not None: results.append({"path":f.relative_to(root).as_posix(),**info})
        except (OSError,ValueError) as e:
            results.append({"path":f.relative_to(root).as_posix(),"error":str(e)})
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps({"schema":1,"root_label":root.name,"elf_files":results},indent=2)+"\n")
    print(f"Found {len(results)} ELF files")
if __name__=="__main__": main()
