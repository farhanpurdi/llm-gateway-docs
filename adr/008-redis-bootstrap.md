# ADR-008 — Redis opsional saat bootstrap

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Pada rancangan awal Redis opsional saat bootstrap; aktivasi ditopang kebutuhan cache/rate limiting terdistribusi.

## Alasan dan konsekuensi

Kebutuhan operasional dan dampak failure harus dibuktikan, bukan sekadar memasukkan komponen ke diagram.

## Keadaan aktual dan batas bukti

Redis existing dan kini wajib bagi readiness/release/Compose. M-02 menunggu rationale/keputusan; jangan menghapus atau menonaktifkannya diam-diam.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Drill17Oktober2026:Redis belum dirujuk sebagai cache dalam runtime YAML existing;
inference/negativeauth/ACL/budget tetap bekerja saat Redis dihentikan. Dependency
health/release tetap membutuhkannya. [Bukti](../reports/phase1-final-evidence/dependency-outage-final.txt).
M-02 tetapOPEN:temuan ini tidak mengotorisasi penghapusan Redis, perubahan readiness,
atau klaim shared/distributed rate limiting. Pertahankan container existing.

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
