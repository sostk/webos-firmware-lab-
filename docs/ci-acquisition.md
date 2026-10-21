# GitHub Actions: official firmware acquisition

All three direct LG CDN links are recorded in `configs/firmware-sources.json` as supplied by the repository owner. **Package model/version and regional applicability are not verified until inspection.** SHA-256 is initially unknown.

## Run
1. Open [Actions](https://github.com/sostk/webos-firmware-lab-/actions).
2. Select **Inspect official LG firmware packages**.
3. Select **Run workflow**, choose `c1`, then repeat for `c5` and `c6`.
4. Download each job's `firmware-<target>-metadata` artifact. The artifact contains JSON only.

The workflow downloads a maximum 5 GiB ZIP to an ephemeral runner, computes SHA-256, reads ZIP central-directory entries and **deletes the ZIP before upload**. It does not extract EPK, execute binaries, flash devices or publish proprietary files.

## Limits and verification
- Jobs are manually triggered, serialized, and limited to 90 minutes each.
- The official CDN may reject automated requests or redirect unexpectedly. Failures require investigation; no fallback mirrors.
- SHA-256 of a downloaded ZIP is a reproducibility fingerprint, not independent authenticity verification.
- ZIP entries and filenames alone do not prove model/firmware compatibility.
- Reports should be reviewed before proceeding to extraction.
- LG's distribution terms and CI bandwidth usage should be considered before repeated runs.
