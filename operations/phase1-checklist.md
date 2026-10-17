# Checklist keputusan deploy Phase 1

> Jalankan perintah script dari `company-ai-platform/llm-gateway-infra`, bukan dari repo docs.
> Baca [panduan operasional](README.md) dan [status Phase1](../architecture/phase-1.md) sebelum eksekusi.

Pengujian lokal port 4000 adalah bukti untuk konfigurasi dan image saat diuji.
Bukan bukti jaringan/TLS/storage/CI server tujuan sudah siap.

## Wajib lulus pada candidate final

- [ ] Commit/push perubahan ketiga repo, semua file baru ikut Git, required merge gate lulus.
- [ ] Catat SHA source dan image digest yang disetujui; tidak ada tag latest.
- [ ] Validator infra/config/E2E, unit, smoke, live dan OpenCode lulus.
- [ ] Gitleaks history + working tree, audit Python, dan baseline Trivy lulus.
- [ ] Backup diverifikasi, restore drill dan rollback config lulus.
- [ ] Review temuan keamanan aktual, jangan menaikkan baseline agar scan terlihat hijau.

## Wajib disiapkan pada server oleh operator

- [ ] Secret server disimpan privat; master/provider key tidak diberikan ke developer.
- [ ] `.env` berizin 600, salt tersimpan bersama backup terenkripsi di luar host.
- [ ] TLS/domain, firewall, dan akses administrator dikonfigurasi dan diuji dari luar host.
- [ ] PostgreSQL/Redis tidak terbuka ke jaringan pengguna; gateway port 4000 dibatasi.
- [ ] Kapasitas disk dan jadwal backup/retensi aktif; alarm kegagalan dan PIC incident jelas.
- [ ] Kompatibilitas migrasi diperiksa jika versi image/database berubah.
- [ ] Aturan freeze provisioning/offboarding dipahami seluruh operator.
- [x] Policy pengerjaan/tes final pilot disetujui user 2026-10-13: pilot.yaml (kedua alias, team US$10, anggota US$2, RPM30/TPM100000); detail [ADR-016](../adr/016-pilot-limits.md).
- [ ] Penerapan policy pada target pilot, kelompok peserta, pemilik layanan dan RPO/RTO disetujui/diverifikasi dan dicatat.
- [ ] Anggota lama yang akan dipakai pilot diperiksa: script sebelumnya tidak mengirim durasi reset. Perbaikan script tidak memigrasikan record lama; lihat [laporan P1-09](../reports/P1_09_P1_10_LIMITS_COST_REPORT.md).
- [ ] Ulangi health, smoke/live, TLS/access check dan restore di target setelah deploy.

Kotak yang masih kosong disengaja: tidak ditandai lulus hanya karena tes lokal berhasil.
Laporan lintas milestone dan bukti eksekusi ada di folder `llm-gateway-docs/reports/`.
