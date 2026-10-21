# Observed C1 and C6 firmware packages — 2026-10-21

These results were extracted from GitHub Actions **metadata artifacts**, not from proprietary firmware files. Both acquisition jobs completed successfully.

| Field | C1 | C6 |
|---|---|---|
| Run | [39524158551](https://github.com/sostk/webos-firmware-lab-/actions/runs/39524158551) | [39524221182](https://github.com/sostk/webos-firmware-lab-/actions/runs/39524221182) |
| Model hint | OLED65C1PTB | OLED65C6PSA |
| Version hint | 03.53.45 | 43.21.79 |
| ZIP bytes | 1456634872 | 2203707985 |
| ZIP SHA-256 | `7d8745b692901f10d752c61b20b0670522f880efc650130f13a0473387c2c6a5` | `e18681230c091c85a2a343752023cdd6da3d06a73e7958b5667e8edea909e8bf` |
| ZIP entries | 1 | 1 |
| EPK filename | `lib32-starfish-global-secured-o20n-koli-47-03.53.45_prodkey_usb_V3_SECURED.epk` | `lib32-starfish-global-secured-o26-qilian-3512-43.21.79_prodkey_usb_V3_SECURED.epk` |
| EPK uncompressed bytes | 1463701733 | 2222621505 |
| EPK compressed bytes | 1456634618 | 2203707653 |
| ZIP entry encrypted | false | false |

**Interpretation:** Both ZIPs contain one EPK whose name indicates secured V3 packaging. ZIP-level encryption is absent, but that does not mean the EPK payload is unencrypted or extractable. Platform strings `o20n` and `o26` differ; they are not sufficient to establish exact chipsets or port feasibility. The source model/version remains a hint until package headers and applicable-model metadata are inspected. Hashes were computed during download, not verified against an independent LG checksum.

## Next
1. Run C5 acquisition and inspect its metadata.
2. Add CI extraction-probe mode that extracts only the ZIP's EPK and inspects its header (no full EPK decryption).
3. Determine which EPK extraction features work for each target and record any key/format blockers.
4. Compare actual boot/kernel/partition data only after validated extraction.
