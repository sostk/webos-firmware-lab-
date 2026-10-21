# EPK extractor compatibility — 2026-10-21

Source: [GitHub Actions run 39534078677](https://github.com/sostk/webos-firmware-lab-/actions/runs/39534078677). All three matrix jobs succeeded and published JSON metadata. Extractor: [openlgtv/epk2extract](https://github.com/openlgtv/epk2extract), pinned commit `2b6af078b56dbedb89efc0f4943036150f1ecae9`.

| Target | Job | Extractor exit | Missing AES key flag | Unsupported format flag | Extracted files |
|---|---|---:|---|---|---:|
| C1 | success | 0 | true | false | 0 |
| C5 | success | 0 | true | false | 0 |
| C6 | success | 0 | true | false | 0 |

The JSON also reports `epk_v3_detected: false` for all targets. This is a log-pattern flag, **not evidence that EPK v3 was absent**: the filenames indicate V3 secured, and the diagnostic pattern may not match the extractor's output. No decryption keys were supplied, and no proprietary firmware files were uploaded.

**Conclusion:** The tested extractor invocation did not produce any files for any target. The zero exit codes must not be interpreted as successful extraction. Missing AES keys were indicated in the captured diagnostics; no definitive conclusion about compatibility or port feasibility follows.

## Recommended next work

1. Tighten CI status semantics: `exit_code == 0` and zero extracted files must be labeled `no_payload_extracted`, not `completed_without_keys`.
2. Add unit tests for diagnostic parsing using synthetic fixtures; avoid repeated multi-GB downloads.
3. Investigate legitimately available developer documentation, public kernel source, webOS OSE components, and hardware specifications for cross-generation comparison without decrypting proprietary firmware.
4. Keep extraction and flashing outside the workflow unless legal access, key handling and model compatibility are established.
