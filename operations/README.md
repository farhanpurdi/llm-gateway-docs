# Panduan operator

[Master](../MASTER_CONTEXT.md) · [status Phase1](../architecture/phase-1.md).

Semua perintah `./scripts/...` pada runbook operasi dijalankan dari
**`company-ai-platform/llm-gateway-infra`**, bukan folder docs. Repo config/e2e harus
berdampingan. Jangan menganggap contoh perintah sebagai izin menjalankan operasi sekarang.

| Kebutuhan | Baca | Dampak |
|---|---|---|
| Capture/release config | [Deployment](deployment.md) | Capture read-only terhadap runtime; deploy backup+restart existing gateway |
| Kembali ke config sebelumnya | [Rollback](rollback.md) | Restart, verifikasi same image/schema; bukan restore transaksi DB |
| Backup/recovery data | [Backup](backup.md) | Drill menghentikan gateway sementara dan menimpa hanya DB restore-test |
| Gangguan kesehatan/akses | [Incident](incident.md) | Diagnosis kemudian tindakan sesuai gejala |
| Onboarding/offboarding | [Lifecycle](lifecycle.md) | Mengubah identitas/key; freeze provisioning saat offboard |
| Keputusan server/pilot | [Checklist Phase1](phase1-checklist.md) | Gate belum otomatis lulus dari hasil lokal |

Environment existing4000, tidak ada staging baru. Simpan secret di `.env` privat atau
mekanisme yang disetujui; jangan menyalin ke docs/log. Backup asli tetap di lokasi
runtime, **tidak dipindahkan ke repo docs**. `reports/` hanya berisi bukti yang telah disanitasi.

Sebelum maintenance: pilih task/target yang diotorisasi, identifikasi baseline dan backup,
hentikan writer lain bila perlu, ketahui langkah recovery, lalu catat hasil aktual
pada [work log](../handover/WORK_LOG.md). Jangan menjalankan E2E secara paralel dengan outage,
restore drill, atau perubahan policy pada user yang sama.
