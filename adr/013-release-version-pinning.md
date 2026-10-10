# ADR-013 — Pin versi release

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Release memerlukan source/image/dependency versi yang dapat direproduksi dan telah diuji.

## Alasan dan konsekuensi

Jangan pakai latest sebagai release contract. Catat refs/digest/schema compatibility; rollback image+config butuh review.

## Keadaan aktual dan batas bukti

Tag image spesifik dan snapshot manifest lokal ada. Python masih ranges, source dirty, tag/sign-off belum; config-only rollback tidak membuktikan server redeploy.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
