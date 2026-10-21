#!/usr/bin/env python3
"""Download one official LG URL, inspect ZIP metadata, publish JSON only."""
import argparse, hashlib, json, os, urllib.request, zipfile
from pathlib import Path
from urllib.parse import urlparse

MAX_BYTES = 5 * 1024**3
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,default=Path("configs/firmware-sources.json"))
    p.add_argument("--target",choices=["c1","c5","c6"],required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    targets=json.loads(a.manifest.read_text())["targets"]
    target=next(x for x in targets if x["id"]==a.target)
    url=target["download_url"]
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.hostname!="gscs-b2c.lge.com" or parsed.path!="/downloadFile":
        p.error("Expected LG CDN HTTPS downloadFile URL")
    a.out.mkdir(parents=True,exist_ok=True)
    package=a.out/"package.zip"
    digest=hashlib.sha256()
    total=0
    request=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; FirmwareResearch/1.0)"})
    with urllib.request.urlopen(request,timeout=120) as response,package.open("wb") as output:
        final=urlparse(response.geturl())
        if final.scheme!="https" or not (final.hostname=="lge.com" or (final.hostname or "").endswith(".lge.com")):
            raise ValueError("Download redirected outside LG domain")
        while True:
            block=response.read(1024*1024)
            if not block: break
            total+=len(block)
            if total>MAX_BYTES: raise ValueError("Package exceeds 5 GiB safety cap")
            digest.update(block);output.write(block)
    report={"target":a.target,"model_hint":target["model"],"version_hint":target.get("version_hint"),
            "source_url":url,"bytes":total,"sha256":digest.hexdigest(),
            "sha256_independently_verified":False,"zip_entries":[]}
    if not zipfile.is_zipfile(package): raise ValueError("Downloaded response is not a ZIP archive")
    with zipfile.ZipFile(package) as z:
        for e in z.infolist():
            report["zip_entries"].append({"name":e.filename,"size":e.file_size,
                "compressed_size":e.compress_size,"crc32":f"{e.CRC:08x}","encrypted":bool(e.flag_bits & 1)})
    (a.out/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    package.unlink()
    print(f"Inspected {a.target}: {len(report['zip_entries'])} entries; {total} bytes; SHA-256 {digest.hexdigest()}")
if __name__=="__main__": main()
