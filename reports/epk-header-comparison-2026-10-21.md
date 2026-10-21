# Secured EPK header comparison — 2026-10-21

Source: [GitHub Actions run 39530177031](https://github.com/sostk/webos-firmware-lab-/actions/runs/39530177031), three successful matrix jobs. These are **metadata-only observations** from the first 4096 bytes of each EPK member. No EPK extraction or decryption was attempted.

| Target | Artifact ID | EPK bytes | Header SHA-256 (first 4096 bytes) | Readable version-like strings |
|---|---:|---:|---|---|
| C1 | 12314264898 | 1463701733 | `c54438da6c2645cf7f6b78634c7200e38a44e7f938b6feef2a58f74fd9d4c17e` | none reliably identified |
| C5 | 12315303439 | 1838871496 | `5f0232efa19233d9753e5161aee3abe9ea6729aa27c34bd4bc18230a9774a6e3` | `10.3.1` (twice) |
| C6 | 12315109664 | 2222621505 | `458f994e88f82c4780c4a3ef347ade7fd1e2fb38d311964ef0584eada257dfe5` | `11.2.0` (twice) |

EPK filenames:
- C1: `lib32-starfish-global-secured-o20n-koli-47-03.53.45_prodkey_usb_V3_SECURED.epk`
- C5: `lib32-starfish-global-secured-o22n3-papikonda-3006-33.31.68_prodkey_usb_V3_SECURED.epk`
- C6: `lib32-starfish-global-secured-o26-qilian-3512-43.21.79_prodkey_usb_V3_SECURED.epk`

The version-like strings are **not yet identified** as kernel, OpenSSL, firmware, or other component versions. The secured V3 suffix is filename evidence only. The headers appear opaque to this simple signature probe, but entropy or cryptographic state was not measured. ZIP entry encryption flags were false, which does not imply that EPK contents are unencrypted.

## Next validation gate
Review the current upstream `openlgtv/epk2extract` implementation, build from a pinned commit in CI, run a bounded, metadata-focused compatibility test with clearly reported errors, and publish logs/JSON only. Do not upload EPKs, keys, extracted payloads, or device firmware. No flashing or firmware transplantation.
