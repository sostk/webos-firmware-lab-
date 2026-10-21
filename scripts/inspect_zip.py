#!/usr/bin/env python3
"""Inspect LG firmware ZIP locally without extracting or executing its contents."""
import argparse,hashlib,json,zipfile
from pathlib import Path
def main():
 p=argparse.ArgumentParser()
 p.add_argument("package",type=Path)
 p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 h=hashlib.sha256()
 with a.package.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
 with zipfile.ZipFile(a.package) as z:
  files=[{"name":x.filename,"uncompressed_bytes":x.file_size,"compressed_bytes":x.compress_size,"crc32":f"{x.CRC:08x}","encrypted":bool(x.flag_bits&1)} for x in z.infolist()]
 result={"filename":a.package.name,"bytes":a.package.stat().st_size,"sha256":h.hexdigest(),"entries":files,"note":"ZIP central directory inspection only. CRC is not cryptographic authentication."}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+"\n")
 print(f"Inspected {len(files)} entries; SHA-256: {h.hexdigest()}")
if __name__=="__main__":main()
