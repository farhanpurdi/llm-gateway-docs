# ADR-013 — Pin versi release

Status: **BASELINE + APPROVED_OVERRIDE O-10**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Release memerlukan source/image/dependency versi yang dapat direproduksi dan telah diuji.

## Alasan dan konsekuensi

Jangan pakai latest sebagai release contract. Catat refs/digest/schema compatibility; rollback image+config butuh review.

## Keadaan aktual dan batas bukti

Pin image dan tiga Python lock berhash tersedia. Source main keempat repo sama
dengan candidate yang diuji; review/merge terverifikasi. Pengguna menetapkan versi
**v0.0.1** dan menutup Phase1 dengan catatan pada18Oktober2026, **O-10**.
Nama versi bukan bukti tag sudah dibuat: pemeriksaan remote tidak menemukan tag
v0.0.1, dan pencatatan ini tidak membuat/push tag atau release GitHub.

Risiko kerentanan PostgreSQL/Redis diterima untuk penutupan fase ini. Kandidat evaluasi
masa depan: `dhi.io/postgres:16.15-alpine3.23` dan `dhi.io/redis:7.4.11-debian13`.
Belum ada pemasangan/pengujian kompatibilitas image kandidat. Image/runtime/baseline
tidak diubah. [Refs, batas dan catatan penutupan](../reports/PHASE1_V0_0_1_CLOSEOUT.md).
Config-only rollback teruji lokal tetap bukan server redeploy lintas image/schema.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
