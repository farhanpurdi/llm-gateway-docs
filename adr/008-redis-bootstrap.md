# ADR-008 — Redis opsional saat bootstrap

Status: **BASELINE + O-10; implementasi cache/TTL NOT_VERIFIED**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
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

## Keputusan pengguna O-10 — 18 Oktober 2026

Target TTL awal Redis **24 jam (86400 detik)**; belum ada kebijakan pembatasan
pengguna Redis tambahan yang disepakati. Phase1 v0.0.1 ditutup dengan catatan.
Ini target yang harus terbawa ke pekerjaan berikutnya, bukan bukti cache/TTL aktif.

Source runtime YAML belum mempunyai konfigurasi native Redis cache. Compose tetap
memuat Redis di jaringan backend tanpa publish port host; source Compose tidak
menyetel password/ACL Redis tambahan. Ini pemeriksaan source, bukan audit runtime
VM. Developer memakai LiteLLM, tidak perlu diberi akses langsung Redis.

Redis tidak mempunyai satu pengaturan global TTL yang otomatis berlaku ke semua
key existing. Scope key/data dan cara mengaktifkan TTL perlu ditentukan sebelum
implementasi. Jangan menerapkan expiry24jam pada lock/auth/rate-limit/spend data
secara massal. TTL ini bukan retensi PostgreSQL, expiry virtual key atau reset budget.
[Keputusan dan tindak lanjut](../reports/PHASE1_V0_0_1_CLOSEOUT.md).

## Aturan perubahan

Drill17Oktober2026:Redis belum dirujuk sebagai cache dalam runtime YAML existing;
inference/negativeauth/ACL/budget tetap bekerja saat Redis dihentikan. Dependency
health/release tetap membutuhkannya. [Bukti](../reports/phase1-final-evidence/dependency-outage-final.txt).
M-02 tetapOPEN:temuan ini tidak mengotorisasi penghapusan Redis, perubahan readiness,
atau klaim shared/distributed rate limiting. Pertahankan container existing.

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
