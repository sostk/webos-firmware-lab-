# Evidence: webOS 25 extraction and partitioning

## Upstream tools
- [openlgtv/epk2extract](https://github.com/openlgtv/epk2extract) documents EPK v1/v2/v3 and warns that EPK v2/v3 require suitable AES/RSA keys. Do not assume every LG firmware is extractable.
- [openlgtv/epk2extract PR #143](https://github.com/openlgtv/epk2extract/pull/143) (open at time of research) proposes a second-stage `super.pak` carving workflow for OLED55C56LB.AEK firmware 33.31.68.01, using `dpmeta.pak` layout information. This is an example from a specific donor, not verified for C1 or C6.

## Hypothesis to test
Modern donor packages may contain multiple logical filesystem partitions within `super.pak`, whereas the C1 may use a different layout. Compare actual partition tables and metadata; do not transplant offsets across models.

## Analysis procedure
1. Acquire package from model-matched official support page, retain SHA-256 and provenance.
2. Attempt supported offline EPK extraction, recording errors and required prerequisites.
3. If `dpmeta.pak` and `super.pak` exist, inventory metadata and verify extent boundaries before carving.
4. Inventory extracted files, then run `scripts/elf_inventory.py` to identify binary ABI differences.
5. Separate verified evidence from assumptions in feasibility assessment.

No firmware files have yet been extracted in this repository.
