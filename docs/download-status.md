# Official LG download resolution status — 2026-10-21

| ID | LG support page | Version | Direct ZIP URL | Downloaded | SHA-256 |
|---|---|---|---|---|---|
| C1 | https://www.lg.com/np/support/product/lg-OLED65C1PTB.UTBPLJK | 03.53.45 | Not yet verified | No | Unknown |
| C5 | https://www.lg.com/us/support/product/lg-OLED55C5PUA.AUS | 33.31.69 | Not yet verified | No | Unknown |
| C6 | https://www.lg.com/au/support/product-support/cs-OLED65C6PSA.AAU | 43.21.79 | Not yet verified | No | Unknown |

The pages publicly list these packages, but their download buttons may rely on dynamic page data. Do not guess CDN URLs. For C1, the Nepal page's displayed applicable-model list is incomplete for the exact Australian suffix; confirm compatibility before treating it as an Australian recovery package. Donor packages are for offline analysis only.

## Local acquisition
Use LG's **Download** button on the relevant support page and save the ZIP to `downloads/`. Then:

```bash
python3 scripts/inspect_zip.py downloads/Software_File\(Version_03.53.45\).zip --out reports/c1-zip.json
```

Repeat for C5 and C6 with the corresponding filenames. Do not commit ZIPs or extracted firmware. The resulting JSON metadata can be reviewed without distributing proprietary binaries.

## Direct URL discovery
In a desktop browser, open Developer Tools > Network, click the LG download button, and inspect the resulting request or redirect. Verify it belongs to LG's official distribution infrastructure and corresponds to the selected model/version before adding it to the source manifest. Avoid copying URLs containing private tokens.
