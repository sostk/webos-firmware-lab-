#!/usr/bin/env python3
"""Read-only EPK metadata probe; never saves or uploads firmware payloads."""
import argparse, hashlib, json, re, urllib.request, zipfile
from pathlib import Path
from urllib.parse import urlparse

MAX_DOWNLOAD = 5 * 1024**3
MAX_EPK = 5 * 1024**3
def trusted(url):
    u=urlparse(url)
    return u.scheme=="https" and (u.hostname=="lge.com" or (u.hostname or "").endswith(".lge.com"))
class LgRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not trusted(newurl):
            raise ValueError("Redirect outside LG HTTPS domains")
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def run(manifest, target_id, out):
    target=next(t for t in json.loads(manifest.read_text())["targets"] if t["id"]==target_id)
    url=target["download_url"]
    u=urlparse(url)
    if not trusted(url) or u.hostname!="gscs-b2c.lge.com" or u.path!="/downloadFile":
        raise ValueError("Not an approved LG firmware source")
    out.mkdir(parents=True,exist_ok=True)
    temp=out/"firmware.tmp.zip"
    result={"target":target_id,"model_hint":target["model"],"version_hint":target.get("version_hint"),
            "source_url":url,"status":"not_probed","entries":[]}
    try:
        h=hashlib.sha256(); size=0
        opener=urllib.request.build_opener(LgRedirect())
        with opener.open(urllib.request.Request(url,headers={"User-Agent":"FirmwareLab/1.0"}),timeout=120) as response, temp.open("wb") as f:
            if not trusted(response.geturl()): raise ValueError("Untrusted final URL")
            while block:=response.read(1024*1024):
                size+=len(block)
                if size>MAX_DOWNLOAD: raise ValueError("Download exceeds 5 GiB")
                h.update(block);f.write(block)
        result.update(zip_bytes=size,zip_sha256=h.hexdigest(),zip_sha256_independently_verified=False)
        if not zipfile.is_zipfile(temp): raise ValueError("Not a ZIP")
        with zipfile.ZipFile(temp) as z:
            for entry in z.infolist():
                if entry.is_dir(): continue
                if not entry.filename.lower().endswith(".epk"): continue
                if entry.file_size>MAX_EPK: raise ValueError("EPK exceeds 5 GiB")
                if entry.flag_bits & 1: raise ValueError("ZIP member encrypted")
                # Inspect only a small prefix; no extracted EPK is written to disk.
                with z.open(entry) as f: header=f.read(4096)
                strings=[m.group().decode("ascii") for m in re.finditer(rb"[ -~]{6,}",header)]
                result["entries"].append({"name":entry.filename,"epk_bytes":entry.file_size,
                    "zip_crc32":f"{entry.CRC:08x}","header_hex_first_128":header[:128].hex(),
                    "header_ascii_strings":strings[:40],
                    "header_sha256_first_4096":hashlib.sha256(header).hexdigest(),
                    "header_bytes_read":len(header),
                    "extraction_attempted":False,
                    "extraction_status":"not_attempted: secured EPK payload requires validated tooling and authorization"})
        result["status"]="header_probed"
    except Exception as exc:
        result["status"]="error";result["error"]=f"{type(exc).__name__}: {exc}"
        raise
    finally:
        temp.unlink(missing_ok=True)
        (out/"epk-probe.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"target":target_id,"status":result["status"],"epk_count":len(result["entries"])},indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,default=Path("configs/firmware-sources.json"))
    p.add_argument("--target",choices=["c1","c5","c6"],required=True)
    p.add_argument("--out",type=Path,default=Path("epk-output"))
    a=p.parse_args()
    run(a.manifest,a.target,a.out)
