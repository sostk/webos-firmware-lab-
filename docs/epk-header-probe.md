# Secured EPK header probe

The manual workflow [Probe secured EPK headers](../.github/workflows/epk-header-probe.yml) downloads one official LG ZIP at a time and inspects up to 4096 bytes of each EPK member. It produces JSON metadata only and removes the temporary ZIP.

Run the workflow separately for `c1`, `c5`, and `c6`. Download the `epk-header-<target>` artifact and compare its `header_hex_first_128` and `header_ascii_strings` fields.

**Scope:** This is a container-header inspection stage, not EPK decryption or filesystem extraction. The `extraction_status` field explicitly records that extraction was not attempted. Before adding an EPK extractor, verify supported format versions, license, upstream source revision, and required keys. Never upload firmware, keys, or extracted proprietary binaries as artifacts. No flashing or TV modifications.
