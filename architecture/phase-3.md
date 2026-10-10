# Phase 3 — Enterprise readiness (belum dimulai)

Baca [master](../MASTER_CONTEXT.md). Pertahankan rancangan
[baseline §10](../archive/PROJECT_MASTER_CONTEXT.md#10-roadmap-phase-3--productionenterprise).
**Semua P3 berstatus NOT_STARTED sebagai milestone enterprise.** Beberapa kontrol
minimum sudah ada di Phase1; itu pondasi, bukan bukti HA/DR/SLO enterprise selesai.

## 1. Tujuan dan pemisahan dari Phase1

Naikkan keamanan, keandalan, observability dan skala berdasarkan risiko/beban nyata.
TLS shared access, secret handling, ACL, privacy minimum dan backup awal tetap wajib
Phase1; jangan menundanya dengan alasan Phase3 belum dimulai.

Tidak memilih Kubernetes, WAF, secret manager atau monitoring vendor tanpa kebutuhan
terukur dan ADR. Single-instance local4000 bukan HA. Budget/rate limit lintas replika
memerlukan pembuktian baru. RPO24h/RTO60m dalam runbook lokal adalah usulan, bukan SLA.

## 2. Roadmap asli dan acceptance

| ID | Pekerjaan | Syarat penerimaan |
|---|---|---|
| P3-00 | Threat model/security review | Threats, mitigasi, owner, data handling, risk register |
| P3-01 | API gateway/WAF/network/private endpoints | TLS/IP policy/admin isolation/auth path teruji |
| P3-02 | Secret manager/rotation | Tidak mengandalkan copy key manual; rotation teruji |
| P3-03 | Metrics/log/traces/usage dashboard | SLO latency/error/cost; isi prompt terlindungi |
| P3-04 | HA LiteLLM + PG/Redis strategy | Failover teruji, auth/budget konsisten, batasan dicatat |
| P3-05 | Backup/restore/incident/DR | RPO/RTO disetujui dan diukur; salt/secret lifecycle tercakup |
| P3-06 | Guardrails/classification/redaction | Policy-specific tests, latency dan false positives direview |
| P3-07 | Load/performance/chaos | SLO di bawah beban, provider429/backoff/failure behavior |
| P3-08 | Provider expansion jika disetujui | ADR, adapter/contract/pricing/data governance/tests |
| P3-09 | Production readiness/sign-off | Handover/on-call/SLO/rollback/cost disepakati |

## 3. Pondasi yang boleh digunakan kembali

H4 dependency detection, H5 restore83tabel, H7 scanners, H9 retention, H10 config rollback
adalah bukti lokal terbatas. Jangan mengubah labelnya menjadi failover, cross-region DR,
SLA atau restore lintas versi. Backup di host yang sama bukan offsite recovery.

Observability metadata target dari baseline: request_id, timestamp, user pseudonym,
team_id, key_id/hash, alias, upstream model, provider, input/output tokens, estimated cost,
duration_ms, status/error_type, trace_id. Ketersediaan dan redaksi tiap field harus diuji
pada versi runtime; bukan instruksi menyimpan raw prompt/response/source code/PII.

## 4. Provider expansion tetap berizin

OpenAI-only berlaku sekarang. Anthropic/Google/provider lain adalah opsi masa depan,
bukan backlog yang otomatis diaktifkan. Sebelum P3-08, evaluasi data residency/kontrak,
security, harga/token accounting, tool/stream/context compatibility dan fallback semantics.
Pertahankan alias stabil; perubahan kontrak memerlukan persetujuan. Jika tidak ada
provider cadangan, kembalikan kegagalan dengan jelas; jangan menjanjikan HA/fallback.

## 5. Exit gate

- [ ] Threat/risk/data-handling review dan owner disetujui.
- [ ] SLO, observability, on-call dan biaya dapat dioperasikan.
- [ ] Failover, load, restore/DR dan secret rotation dibuktikan pada target.
- [ ] Change/release/rollback, lisensi, security findings dan exception ditandatangani.
- [ ] Provider tambahan hanya setelah ADR khusus disetujui.

**Next ketika fase ini diizinkan:** P3-00 dan prioritas risiko yang disetujui.
Tidak ada izin dari dokumen ini untuk memperluas infrastruktur sekarang.
