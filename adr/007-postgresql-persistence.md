# ADR-007 — PostgreSQL sejak Phase1

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Simpan identitas/key/spend secara persisten melalui native LiteLLM dan PostgreSQL.

## Alasan dan konsekuensi

Backup/salt/recovery perlu dikelola; jangan menulis schema internal LiteLLM dari Control Plane secara langsung.

## Keadaan aktual dan batas bukti

PG16.15 existing; restore83tabel identik. Bukan bukti boot aplikasi terhadap DB restore atau fail-closed saat outage.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
