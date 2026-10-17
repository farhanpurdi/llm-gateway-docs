# ADR-017 — Lisensi dan fitur enterprise

Status: **OPEN**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Review fitur OSS/enterprise dan lisensi versi yang dipakai sebelum bergantung pada commercial capability.

## Alasan dan konsekuensi

Procurement/biaya/lisensi membutuhkan keputusan owner; jangan mengaktifkan fitur berbayar dari asumsi roadmap.

## Keadaan aktual dan batas bukti

[Inventaris komponen/versi dan sumber resmi](../operations/license-inventory.md)
ditambahkan17Oktober2026:LiteLLM community/enterprise dibedakan, PostgreSQL dan
Redis7.4RSALv2/SSPLv1 dicatat. Review distribusi/seluruh dependency dan penerimaan
perusahaan belum ada; ADR tetapOPEN, tidak otomatis ditutup dari inventaris atau tes.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
