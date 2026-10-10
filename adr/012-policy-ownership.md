# ADR-012 — Satu desired-state writer policy

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Gunakan Git untuk desired config Phase1; Phase2 menentukan satu writer per domain dan reconciler eksplisit.

## Alasan dan konsekuensi

Hindari config Git dan Admin UI/API mengubah domain sama tanpa ownership/reconciliation.

## Keadaan aktual dan batas bukti

Policy YAML dibaca script lalu native API; belum ada reconciler. Katalog model tidak otomatis menjadi runtime config.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
