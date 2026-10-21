# Official LG firmware listings (checked 2026-10-21)

These are **support-page listings**, not yet independently verified direct ZIP download URLs or checksums.

| Target | Full model | Firmware | LG page | Status |
|---|---|---|---|---|
| C1 baseline | OLED65C1PTB.AAU (Australia) | Not listed on AU page | https://www.lg.com/au/support/product-support/cs-OLED65C1PTB/ | AU page says no software available |
| C1 regional reference | OLED65C1PTB.UTBPLJK (Nepal) | 03.53.45, 2025-10-14 | https://www.lg.com/np/support/product/lg-OLED65C1PTB.UTBPLJK | Official regional listing; verify applicability to AAU before use |
| C5 donor | OLED55C5PUA.AUS (USA) | 33.31.69, 2026-09-08 | https://www.lg.com/us/support/product/lg-OLED55C5PUA.AUS | Official listing |
| C6 donor | OLED65C6PSA.AAU (Australia) | 43.21.79, 2026-10-06 | https://www.lg.com/au/support/product-support/cs-OLED65C6PSA.AAU | Official listing |

## Next steps

1. Resolve actual LG-hosted ZIP download URLs using the support page's download buttons.
2. Check the C1 release's **detailed applicable model list** for OLED65C1PTB and the relevant regional suffix.
3. Download on a workstation, record SHA-256 and inspect ZIP entries without running firmware code.
4. Keep firmware packages and extracted contents out of GitHub.

**Never flash C5/C6 packages to a C1.** These are donor packages for offline analysis only.
