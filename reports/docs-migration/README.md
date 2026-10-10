# Migrasi dokumentasi ke llm-gateway-docs

Atas permintaan user: seluruh docs/report dan context utama dipusatkan pada repository
docs existing. [Manifest](migration-manifest.json) mencatat source→tujuan, hash sebelum
pemindahan dan hash setelah penyesuaian. Bukti mentah dipertahankan identik.

Perubahan source non-dokumentasi hanya dua daftar prasyarat validator config:
`docs/model-catalog.md` diganti `README.md`, karena katalog kini dimiliki repo docs.
Pemeriksaan model/policy/runtime tidak dilonggarkan atau diperbaiki pada sesi ini;
F-01/F-02 tetap OPEN. Validasi tautan/katalog dokumentasi dilakukan oleh validator docs.

Tidak ada Docker/provider operation, deployment, repo/remote baru, commit atau push.
File context lama di root menjadi penunjuk saja. Folder docs/reports asal dikosongkan
melalui pemindahan, bukan menyisakan salinan isi yang bisa drift.

## Hasil pemeriksaan migrasi

- [Validator docs](docs-validation.txt): struktur, tautan/anchor, ID roadmap dan ADR, serta hash evidence.
- [Validator CI config](config-ci-validation.txt) dan [validator config dasar](config-validation.txt): PASS.
- [Scope source](scope-verification.json): hanya dua prasyarat lokasi docs berubah; source komponen lain tetap.
- [Scan secret final](secret-scan.txt): dijalankan pada repo docs. Dua kecocokan awal ternyata
  kalimat deskriptif, bukan credential; kalimat diperjelas tanpa mematikan rule scanner.
  [Catatan pemeriksaan](secret-scan-review.json) dan [hasil awal](secret-scan-initial.txt) dipertahankan.
