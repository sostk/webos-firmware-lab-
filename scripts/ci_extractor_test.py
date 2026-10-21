#!/usr/bin/env python3
"""Ephemeral no-key extractor compatibility test; emits metadata only."""
import argparse, hashlib, json, os, re, shutil, subprocess, tempfile, urllib.request, zipfile
from pathlib import Path
from urllib.parse import urlparse

MAX=5*1024**3
def check_url(url):
    p=urlparse(url)
    return p.scheme=="https" and (p.hostname=="lge.com" or (p.hostname or "").endswith(".lge.com"))
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not check_url(newurl): raise ValueError("Untrusted redirect")
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target",required=True,choices=["c1","c5","c6"])
    p.add_argument("--manifest",type=Path,default=Path("configs/firmware-sources.json"))
    p.add_argument("--extractor",type=Path,required=True)
    p.add_argument("--revision",required=True)
    p.add_argument("--out",type=Path,default=Path("extractor-report"))
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    target=next(t for t in json.loads(a.manifest.read_text())["targets"] if t["id"]==a.target)
    url=target["download_url"]
    if not check_url(url) or urlparse(url).hostname!="gscs-b2c.lge.com": p.error("Untrusted source")
    report={"target":a.target,"extractor":"openlgtv/epk2extract","extractor_revision":a.revision,
            "keys_supplied":False,"payload_uploaded":False,"result":"not_started"}
    try:
        with tempfile.TemporaryDirectory(prefix="firmware-lab-") as tmp:
            root=Path(tmp); archive=root/"firmware.zip"
            size=0;h=hashlib.sha256()
            opener=urllib.request.build_opener(Redirect())
            with opener.open(url,timeout=120) as response,archive.open("wb") as dest:
                if not check_url(response.geturl()): raise ValueError("Untrusted final URL")
                while chunk:=response.read(1024*1024):
                    size+=len(chunk)
                    if size>MAX: raise ValueError("ZIP over 5 GiB")
                    h.update(chunk);dest.write(chunk)
            report.update(zip_bytes=size,zip_sha256=h.hexdigest())
            with zipfile.ZipFile(archive) as z:
                epks=[e for e in z.infolist() if e.filename.lower().endswith(".epk") and not e.is_dir()]
                if len(epks)!=1: raise ValueError("Expected exactly one EPK")
                entry=epks[0]
                if entry.file_size>MAX or entry.flag_bits&1: raise ValueError("Unsupported EPK member")
                epk=root/"input.epk"
                with z.open(entry) as src,epk.open("wb") as dst:
                    copied=0
                    while block:=src.read(1024*1024):
                        copied+=len(block)
                        if copied>MAX: raise ValueError("EPK too large")
                        dst.write(block)
                report.update(epk_filename=entry.filename,epk_bytes=copied)
            archive.unlink()
            # Run without keys in isolated temp directory. Never upload extracted content.
            run_dir=root/"run";run_dir.mkdir()
            binary=a.extractor.resolve()
            try:
                proc=subprocess.run([str(binary),str(epk)],cwd=run_dir,
                                    stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                    timeout=180,check=False)
                output=proc.stdout[-100000:].decode("utf-8",errors="replace").lower()
                report["extractor_exit_code"]=proc.returncode
                report["result"]="completed_without_keys" if proc.returncode==0 else "nonzero_exit"
                report["diagnostics"]={
                    "missing_aes_key":bool(re.search(r"proper aes key is missing|cannot decrypt epk|trying known aes keys",output)),
                    "signature_warning":bool(re.search(r"cannot verify digital signature|proper pem file",output)),
                    "epk_v3_detected":"epk v3 detected" in output,
                    "unsupported_format":"unsupported input file format" in output,
                }
            except subprocess.TimeoutExpired:
                report["result"]="timeout_180_seconds"
            report["extracted_file_count"]=sum(1 for f in run_dir.rglob("*") if f.is_file())
            report["note"]="No output files retained or uploaded. A zero exit code alone does not prove successful extraction."
    except Exception as exc:
        report["result"]="error";report["error_type"]=type(exc).__name__
        raise
    finally:
        (a.out/"compatibility.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
