# Rollback config pada container existing

Baca [deployment](deployment.md) dan [backup](backup.md). Jalankan perintah dari repo infra.
**Scope yang terbukti:** config, container/image/schema yang sama, port4000.
Bukan downgrade image, rollback schema, atau recovery server total.

## Langkah operator

1. Catat gejala, waktu dan operasi release yang gagal. Hentikan release/provisioning
   lain yang dapat mengubah config/data selama diagnosis.
2. Pilih release baseline yang ditangkap sebelum perubahan; jangan menebak nama/digest.
3. Pastikan container/image masih cocok dengan manifest. Script menolak identity berbeda.
4. Jalankan rollback yang diotorisasi dan periksa hasil verifikasinya:

```bash
export PATH="$PWD/../.venv/bin:$PATH"
./scripts/release/release.sh rollback baseline-01
../llm-gateway-e2e/scripts/run-live.sh
```

`baseline-01` contoh ID; gunakan ID nyata. Rollback membuat backup, menulis config pada
inode yang sama, restart, memeriksa mount/readiness/health dan smoke. Live test adalah
langkah operator terpisah dan mengirim request provider berbayar.

## Jika operasi gagal atau proses terputus

Periksa `llm-gateway-infra/releases/operation-*.json`: status operasi, hasil recovery,
path backup dan recovery config. Kegagalan deploy tetap exit gagal walaupun pemulihan
otomatis berhasil; catat incident. Status `in_progress` setelah proses mati perlu
pemeriksaan manual, bukan bukti berhasil.

Ikuti langkah pemulihan byte config dalam [deployment](deployment.md). Pertahankan inode
file bind mount; atomic rename dapat membuat container membaca file lama. Verifikasi
isi mount, health dan tes relevan sebelum menutup incident.

Jangan restore database lama hanya untuk memperbaiki config: transaksi/spend baru dapat
hilang. Perubahan `.env` juga tidak masuk ke environment container hanya melalui restart.
Jika image/schema berbeda, berhenti dan bahas kompatibilitas serta recovery plan dahulu.
