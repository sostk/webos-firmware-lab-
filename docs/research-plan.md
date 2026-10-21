# Firmware port feasibility research

Target: LG OLED65C1PTB. Donor candidates: LG C5 (webOS 25), LG C6 (webOS 26).

## Evidence to collect
- LG support URL, exact model and region, package name, published version, SHA-256
- EPK container structure, signatures and encryption status (without attempting bypass)
- Kernel architecture, config and boot image metadata
- Partition names, filesystem types, A/B slot metadata
- ELF architecture, interpreter, linked shared libraries
- Graphics, video decoder, audio, tuner, HDMI and TEE dependencies
- Signed boot chain and model-specific recovery documentation

## Decision criteria
A donor must match hardware interfaces or have adaptable open drivers; kernel/boot compatibility and recovery must be demonstrated separately. Identical filenames or ELF architecture do not establish compatibility.

## Safety
Never flash experimental images. Never publish proprietary firmware contents or extracted binaries. Do not store firmware URLs containing tokens in CI logs. Prefer local analysis and commit only metadata/reports.
