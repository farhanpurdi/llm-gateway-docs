# Gate release lokal tanpa staging

Target verifikasi disetujui pengguna **O-08,17 Oktober2026**:
GitHub menjalankan CI offline; full live dijalankan manual pada Docker existing4000.
Workflow live staging lama dihapus. Ini tidak mengubah kontrak model, required
validate/security checks, image/container atau gate keamanan server.

## Langkah operator dan reviewer

1. Pilih candidate empat repo, koordinasikan maintenance dan hentikan perubahan
   source/provisioning bersamaan. Simpan status dirty, SHA commit dan hash file yang
   benar-benar akan diuji. Release final perlu candidate commit/review; working tree
   dirty masih bisa menghasilkan bukti lokal, tetapi bukan release yang sudah disetujui.
2. Dari repo infra, gunakan `release.sh capture <id-unik>` untuk mencatat config,
   hash source tiga komponen, container dan imageID. Catat SHA docs dan image
   RepoDigests/platform juga. Capture tidak menjalankan deploy atau membuat container.
3. Jalankan validator ketiga komponen dan docs. GitHub validate/security harus
   hijau pada **SHA candidate**, bukan hanya pada HEAD lama yang berbeda isinya.
4. Dari repo E2E, gunakan Python existing dan jalankan secara serial:

```bash
source ../.venv/bin/activate
./scripts/run-all.sh --include-outage
```

   Pipeline menjalankan unit→smoke→native→live→outage. Outage menghentikan PG/Redis
   existing sebentar dan memulihkannya; OpenCode/sibling repos harus tersedia.
   Simpan stdout/stderr tersensor, waktu dan exitcode. Kegagalan/teardown gagal tidak
   boleh diubah menjadiPASS dari collection atau keberhasilan tahap sebelumnya.
5. Periksa key/team fixture sudahblocked, spend/history tetap ada, layanan sehat,
   ID/image tidak berubah, log/spend tidak menyimpan isi sensitif pada scope audit.
   Dump, `.env`, salt dan raw key tetap di lokasi privat; jangan upload sebagai bukti.
6. Bandingkan hash source sebelum/sesudah. Jika kode/config perilaku berubah,
   ulangi acceptance yang terdampak; untuk perubahan luas ulang full suite. Perubahan
   dokumentasi/metadataCI saja dapat direview dan divalidasi offline tanpa mengirim
   ulang provider request, dengan perbedaan tersebut dicatat secara eksplisit.
7. Simpan laporan, manifest dan hash output di `llm-gateway-docs/reports/`; tautkan
   pada PR/release. Reviewer mencocokkan candidateSHA/filehash/image/platform dengan
   bukti yang dieksekusi dan mencatat review/sign-off. Upload bukti saja bukan livePASS.

## Bukti sesi17Oktober

[Full run](../reports/phase1-final-evidence/full-regression-final.txt):97unit,
5smoke,13native,30live biasa dan2outage PASS, exit0. [Source saat tes](../reports/phase1-final-evidence/source-under-test.json)
serta manifest penutupan pada indeks evidence menunjukkan workingtree yang diuji.
README dan penghapusan workflow staging diselaraskan setelah fullrun; perubahan
non-runtime tersebut dicatat dan E2E validator diulang setelahO-08.

Tidak ada staging, runner self-hosted, secret GitHub baru, deploy/tag/push dari
keputusan ini. TLS/domain/admin boundary, backup luarhost, CVE, penerimaan lisensi/
billing dan sign-off server tetap gate masing-masing. Pilot nyata/peserta/PIC
ditundaO-07, bukan penggunaan/feedback yang sudah terverifikasi.
