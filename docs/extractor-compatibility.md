# No-key EPK extractor compatibility test

Manual workflow: [Test EPK extractor compatibility (all models)](../.github/workflows/epk-extractor-compatibility.yml).

Builds `openlgtv/epk2extract` at pinned commit `2b6af078b56dbedb89efc0f4943036150f1ecae9` and runs it separately on each EPK **without supplying keys**. A failed extraction due to unavailable keys is an expected diagnostic, not proof the format is unsupported. Upstream explicitly states EPK v2/v3 extraction needs appropriate AES and RSA keys.

The test runs in an ephemeral runner, with a 5 GiB input limit and a 180-second extractor timeout. It deletes temporary firmware and any generated payloads; artifacts contain JSON metadata only. Raw extractor stdout is not uploaded because it could expose proprietary data. Results report only predefined diagnostic flags, process status and generated-file count. This is an unprivileged compatibility experiment, **not** a validated secure sandbox. No TV interaction, flashing or firmware repacking.

Possible issue: upstream has reported modern-system build failures and EPK3 crashes; CI may need toolchain compatibility adjustments. A successful process exit alone does not prove successful extraction.
