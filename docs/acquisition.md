# Firmware acquisition and provenance

LG regional support pages may present different firmware for related model suffixes. A model match must be independently verified; C5/C6 donor packages are **not** C1 install candidates.

1. Open the support pages listed in `configs/firmware-sources.json`.
2. Confirm the full model suffix, region, release notes, firmware version and direct download link.
3. Record a direct official HTTPS package URL and, where independently available, a known SHA-256.
4. Download **locally**, not via public GitHub Actions:
   ```bash
   python3 scripts/download.py --url 'https://OFFICIAL-DIRECT-PACKAGE-URL' --output downloads/c1.epk
   python3 scripts/probe.py downloads/c1.epk --out reports/c1-package.json
   ```
5. Keep downloaded and extracted proprietary binaries outside Git. Verify file type and extraction tool support before unpacking.

A hash generated after download establishes identity for future comparisons, but **does not** independently authenticate a package. Do not trust filenames, version hints or arbitrary mirror URLs as verification. Do not execute extracted binaries.
