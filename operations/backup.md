# Backup dan restore — H5/H10C

**Keputusan18Oktober2026, O-10:** backup akan dibahas dengan manager; snapshot VM
GCP menjadi opsi awal yang paling mudah. Jadwal/retensi, cakupan disk dan restore
snapshot belum diverifikasi. Usulan backup harian di bawah belum menjadi jadwal aktif.
Phase1 v0.0.1 ditutup dengan catatan; [closeout](../reports/PHASE1_V0_0_1_CLOSEOUT.md).
Pemulihan snapshot harus mempertahankan data PostgreSQL dan konfigurasi/salt yang
sesuai. Permission700/600 pada file lokal bukan enkripsi file.

> Jalankan perintah script dari `company-ai-platform/llm-gateway-infra`, bukan dari repo docs.
> Baca [panduan operasional](README.md) dan [status Phase1](../architecture/phase-1.md) sebelum eksekusi.

```bash
export PATH="$PWD/../.venv/bin:$PATH"
BACKUP_FILE="$(./scripts/backup/backup-postgres.sh)"
./scripts/backup/verify-backup.sh "$BACKUP_FILE"
./scripts/backup/restore-postgres-test.sh "$BACKUP_FILE"
./scripts/backup/check-restore.sh
```

Satu backup baru menghasilkan tiga file dalam `backups/`:

1. arsip database format custom PostgreSQL (nama acak, tanpa keharusan ekstensi);
2. file `.json` berisi identitas database, waktu UTC, SHA256 dump/environment;
3. file `.env` untuk memulihkan salt/encryption key dan kredensial.

Folder berizin 700 dan file 600. Backup gagal dibersihkan agar tidak disalahartikan
sebagai backup lengkap. Verifier menolak checksum salah atau file pasangan hilang.
Backup lama tanpa metadata tidak dapat dipakai oleh verifier baru: buat backup baru,
atau validasi/migrasikan arsip lama secara terkontrol; jangan mengarang checksum
untuk menyatakan arsip yang belum diverifikasi aman.

Restore test hanya boleh menuju `<POSTGRES_DB>_restore_test` pada PostgreSQL existing.
Database test tersebut akan dihapus/dibuat ulang, jadi jangan gunakan untuk data lain.
Target database utama atau nama lain ditolak sebelum perintah Docker. Wrapper
`restore-postgres.sh` juga memakai pengaman yang sama. Tidak ada restore otomatis
ke database aplikasi utama.

## Drill yang membuktikan isi data

```bash
./scripts/backup/drill.sh --quiesce
./scripts/health/check-all.sh
../llm-gateway-e2e/scripts/run-all.sh
```

Drill mematikan gateway existing sementara agar tidak ada penulisan aplikasi selama
backup/perbandingan. Jangan menjalankan provisioning, SQL writer, atau E2E bersamaan.
Kemudian restore test, periksa tabel, bandingkan jumlah dan fingerprint isi setiap
tabel public. Trap berusaha menyalakan gateway kembali jika drill gagal. Jika mesin
mati/proses terbunuh paksa, operator wajib memeriksa gateway dan menyalakannya kembali.
Fingerprint untuk dataset pilot kecil; bukan validator skala warehouse atau bukti
bahwa schema/image downgrade kompatibel. Health dan E2E setelah drill memeriksa
aplikasi aktif; restore DB diuji integritasnya, belum digunakan boot gateway terpisah.

## Recovery server

Simpan ketiga file bersama di storage **terenkripsi di luar host**, akses terbatas.
SHA256 memeriksa kerusakan file, bukan tanda tangan terhadap penyerang. Jangan kirim
backup `.env` ke chat/log/Git. Pertahankan `LITELLM_SALT_KEY`; kehilangan salt dapat
membuat data terenkripsi tidak bisa dibaca. Redis bukan sumber histori billing.

Usulan pilot: backup harian + sebelum release, retensi harian 7 dan mingguan 4,
restore drill mingguan; operator perlu mengaktifkan jadwal dan menguji restore dari
storage luar host. RPO target 24 jam dan RTO target 60 menit belum merupakan SLA
terukur. Restore database utama saat bencana harus dilakukan operator dalam jendela
maintenance, sesudah menyimpan kondisi terkini dan menilai kehilangan transaksi.
