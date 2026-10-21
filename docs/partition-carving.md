# Offline super.pak extent extraction

The [epk2extract super.pak PR #143](https://github.com/openlgtv/epk2extract/pull/143) documents an example on a particular C5 model. It does **not** establish universal offsets for all C5, C6 or C1 packages.

This project requires **manual verification** of each partition extent before carving. Create a local plan JSON file:

```json
{
  "sector_size": 512,
  "partitions": [
    {"name": "rootfs", "start_sector": 2048, "sector_count": 100}
  ]
}
```

Values above are **illustrative, not actual LG partition data**.

First dry-run:

```bash
python3 scripts/carve_super.py --super extracted/c5/super.pak --plan local-plan.json --outdir extracted/c5/partitions
```

Then, only after validating the extents against the exact image:

```bash
python3 scripts/carve_super.py --super extracted/c5/super.pak --plan local-plan.json --outdir extracted/c5/partitions --execute
```

The script refuses out-of-bounds and overlapping extents and existing outputs. It never writes to a block device. Extracted binaries remain excluded from version control.
