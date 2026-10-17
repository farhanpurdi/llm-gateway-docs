# Release dan rollback config — H10B/H10C

> Jalankan perintah script dari `company-ai-platform/llm-gateway-infra`, bukan dari repo docs.
> Baca [panduan operasional](README.md) dan [status Phase1](../architecture/phase-1.md) sebelum eksekusi.

Prosedur checkpoint ini hanya mengubah config pada **container existing port 4000**.
Tidak menjalankan `compose up`, pull image, recreate container, atau migrasi schema.
`capture` menyimpan config, checksum, ID/digest image dan container, commit serta
checksum file source tiga repository. Status dirty dicatat apa adanya. File runtime
ignored tidak disalin ke manifest source. Folder `releases/` diabaikan Git.

Jalankan dari repository infra dengan Python 3.12 dan dependensi terpasang:

```bash
export PATH="$PWD/../.venv/bin:$PATH"
./scripts/ci/validate.sh
../llm-gateway-config/scripts/ci/validate.sh
../llm-gateway-e2e/scripts/ci/validate.sh
./scripts/health/check-all.sh
./scripts/release/release.sh capture baseline-01
```

Siapkan candidate YAML di file terpisah. Jangan edit config aktif sebelum menangkap
baseline. Pertahankan alias logis dan referensi secret `os.environ/...`.

```bash
./scripts/release/release.sh capture candidate-01 --config /absolute/path/candidate.yaml
./scripts/release/release.sh deploy candidate-01
../llm-gateway-e2e/scripts/run-live.sh
# Jika perlu kembali:
./scripts/release/release.sh rollback baseline-01
../llm-gateway-e2e/scripts/run-live.sh
```

Deploy/rollback otomatis melakukan backup DB + environment, menyimpan config lama,
menulis pada inode config yang sama, restart gateway existing, menunggu readiness,
membandingkan isi mount, health/dependency/catalog check, lalu 5 smoke test. Identitas
container/image harus sama dengan manifest. Tes live dijalankan operator sesudahnya
untuk memeriksa provider dan enforcement, dengan biaya provider kecil.

Mengganti file dengan atomic rename dapat meninggalkan Docker bind mount membaca
inode lama. Karena itu penulisan mempertahankan inode dan dicek dari dalam container.
Satu file lock mencegah dua perintah release bersamaan. Jangan edit config atau
menjalankan script Docker lain secara paralel dengan release.

Jika verifikasi gagal, script berusaha memulihkan byte config sebelum operasi,
restart, dan memverifikasi recovery. Exit tetap gagal agar incident tidak tersamarkan.
`releases/operation-*.json` mencatat status, backup, serta path recovery config.
Kegagalan recovery wajib ditangani operator. Jika proses mati paksa, lihat status
`in_progress`, copy isi recovery config ke **file config existing tanpa rename**,
restart container existing, lalu health/smoke/live. Jangan menganggap rollback
berhasil hanya karena perintah restart berhasil.

## Batas yang harus diketahui

- Rollback yang diuji adalah config, dengan image dan schema yang sama.
- Upgrade/downgrade LiteLLM, PostgreSQL, Redis, schema, atau pindah server memerlukan
  review kompatibilitas dan prosedur tersendiri. Script menolak perubahan ID/image.
- Manifest lokal dapat berasal dari working tree dirty. Sebelum deploy server,
  commit/push semua file dan jalankan merge gate CI; catat SHA release yang disetujui.
- Backup config tidak membatalkan transaksi/spend yang sudah masuk. Jangan restore
  database lama untuk memperbaiki config; itu dapat membuang histori baru.
- Runtime `.env` harus cocok dengan secret yang dipakai container. Mengedit `.env`
  tidak mengubah environment container lewat `docker restart`.

Drill ulang17Oktober2026 PASS:request_timeout180→181→180 lewat capture/deploy/rollback,
backup pada kedua apply,5smoke tiap tahap, healthPASS, inode dan byte asli pulih,
ID/image tetap sama. [Kode drill](../reports/phase1-final-evidence/config-drill.py)
dan [output](../reports/phase1-final-evidence/config-release-rollback.txt).
Manifest tetap workingtree dirty, bukan tag/candidate yang sudah direview.
