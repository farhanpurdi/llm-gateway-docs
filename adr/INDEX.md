# Indeks ADR — nomor asli dipertahankan

[Register drift/override](README.md) · [Master](../MASTER_CONTEXT.md)

ID berasal dari rancangan awal. Nama file dapat mengikuti topik, tetapi ID/makna tidak boleh diganti.
CONFIRMED/BASELINE/OPEN dibedakan; BASELINE bukan bukti implementasi lengkap. O-04 pada ADR011 berasal dari instruksi user pemindahan docs.

| ID | Judul | Status |
|---|---|---|
| ADR-001 | [LiteLLM sebagai Data Plane](001-use-litellm.md) | CONFIRMED |
| ADR-002 | [OpenAI saja pada Phase1](002-openai-only-phase-1.md) | CONFIRMED |
| ADR-003 | [Mapping company-fast](003-company-fast-model.md) | CONFIRMED |
| ADR-004 | [Mapping company-coding](004-company-coding-model.md) | CONFIRMED |
| ADR-005 | [OpenCode client pertama](005-opencode-first-client.md) | CONFIRMED |
| ADR-006 | [Virtual key dan pemisahan credential](006-virtual-key-authentication.md) | BASELINE |
| ADR-007 | [PostgreSQL sejak Phase1](007-postgresql-persistence.md) | BASELINE |
| ADR-008 | [Redis opsional saat bootstrap](008-redis-bootstrap.md) | BASELINE |
| ADR-009 | [Alias sebagai kontrak client](009-logical-model-contract.md) | BASELINE |
| ADR-010 | [Pisahkan Control Plane](010-control-plane.md) | BASELINE |
| ADR-011 | [Tiga repo komponen dan repo dokumentasi](011-repository-layout.md) | BASELINE + APPROVED_OVERRIDE O-04 |
| ADR-012 | [Satu desired-state writer policy](012-policy-ownership.md) | BASELINE |
| ADR-013 | [Pin versi release](013-release-version-pinning.md) | BASELINE |
| ADR-014 | [Pilihan IdP SSO](014-sso-provider.md) | OPEN |
| ADR-015 | [Hosting dan target release](015-hosting-environment.md) | OPEN; target lokal ditetapkan O-01 |
| ADR-016 | [Budget, rate limits dan peserta pilot](016-pilot-limits.md) | OPEN |
| ADR-017 | [Lisensi dan fitur enterprise](017-licensing.md) | OPEN |
