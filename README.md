# webOS Firmware Lab

Read-only research into porting webOS 25/26 to LG OLED65C1PTB (webOS 6), comparing LG C1, C5 and C6 firmware.

## Current status
The initial inventory and comparison tools are committed. **No firmware has been downloaded, extracted or compared yet.** No claim of port feasibility is established.

## Quick start
Supply directories of already extracted firmware files (do not commit proprietary firmware):

```bash
python3 scripts/inventory.py firmware/c1 --out reports/c1.json
python3 scripts/inventory.py firmware/c5 --out reports/c5.json
python3 scripts/compare.py reports/c1.json reports/c5.json --out reports/c1-vs-c5.json
```

For EPK research, see [openlgtv/epk2extract](https://github.com/openlgtv/epk2extract). Extraction depends on format and access to legitimately available tooling/keys. This repository does not flash TVs, bypass signatures or modify boot partitions.

## Next milestones
1. Verify official model-specific firmware downloads and hashes.
2. Add controlled extraction and ELF/kernel/partition analysis.
3. Generate evidence-backed C1 vs C5 vs C6 compatibility matrices.
4. Assess boot feasibility and recovery independently.

See [research plan](docs/research-plan.md).
