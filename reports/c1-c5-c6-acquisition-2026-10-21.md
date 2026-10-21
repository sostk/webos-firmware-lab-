# Firmware acquisition: C1 / C5 / C6 — 2026-10-21

All three GitHub Actions acquisition jobs completed successfully. Findings come from ZIP metadata artifacts, **not** extracted EPK contents. Download SHA-256 values have not been checked against independently published LG hashes.

| Target | Run | ZIP bytes | ZIP SHA-256 | ZIP EPK filename |
|---|---|---:|---|---|
| C1 | [39524158551](https://github.com/sostk/webos-firmware-lab-/actions/runs/39524158551) | 1456634872 | `7d8745b692901f10d752c61b20b0670522f880efc650130f13a0473387c2c6a5` | `lib32-starfish-global-secured-o20n-koli-47-03.53.45_prodkey_usb_V3_SECURED.epk` |
| C5 | [39525691038](https://github.com/sostk/webos-firmware-lab-/actions/runs/39525691038) | 1821390376 | `3783089869307a05b2a3e6181bd8a5a02a72008bd00f474164d3fa76140e0650` | `lib32-starfish-global-secured-o22n3-papikonda-3006-33.31.68_prodkey_usb_V3_SECURED.epk` |
| C6 | [39524221182](https://github.com/sostk/webos-firmware-lab-/actions/runs/39524221182) | 2203707985 | `e18681230c091c85a2a343752023cdd6da3d06a73e7958b5667e8edea909e8bf` | `lib32-starfish-global-secured-o26-qilian-3512-43.21.79_prodkey_usb_V3_SECURED.epk` |

## C5 entry details

- EPK uncompressed size: **1838871496 bytes**
- EPK compressed size: **1821390034 bytes**
- ZIP entry CRC32: `e6ab9da2`
- ZIP entry encrypted flag: false (does **not** establish that EPK payload is unencrypted)
- **Discrepancy:** Manifest version hint was `33.31.69`, but actual EPK filename contains `33.31.68`. Treat the filename as observed evidence, not a definitive verified internal firmware version.

## Next gate

Build a manual workflow to stream each ZIP's EPK to ephemeral storage, inspect container header and attempt a supported metadata-only extraction using pinned upstream tools. Publish JSON/text diagnostics only. Do not publish proprietary payloads, infer keys, or flash devices.
