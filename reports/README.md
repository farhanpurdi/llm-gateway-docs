# Laporan dan bukti

[Master aktif](../MASTER_CONTEXT.md) menentukan aturan; [Phase1](../architecture/phase-1.md)
menentukan status acceptance terbaru. Laporan menyimpan hasil bertanggal, **bukan izin
menjalankan langkah berikutnya atau jaminan server siap**.

| Dokumen/folder | Isi dan cara membaca |
|---|---|
| [PHASE1_H1_H10_REPORT.md](PHASE1_H1_H10_REPORT.md) | Penjelasan perubahan/test per-H1–H10D pada sesi implementasi |
| [PHASE1_CODE_APPENDIX.md](PHASE1_CODE_APPENDIX.md) | 50 file source snapshot sesi tersebut; baca hanya bagian yang relevan |
| [CONTEXT_ALIGNMENT_REVIEW.md](CONTEXT_ALIGNMENT_REVIEW.md) | Evaluasi rancangan awal vs H10D; gate Phase1 belum lengkap |
| [phase1-evidence](phase1-evidence/README.md) | Output eksekusi tes/security/drill sebelumnya |
| [context-review](context-review/README.md) | Reproduksi gap validator dan provenance dokumen sebelum migrasi |
| [docs-migration](docs-migration/README.md) | Manifest pemindahan, integritas evidence dan hasil validasi navigasi |

Output `.txt`/`.json` historis dipindahkan **tanpa mengubah byte**. Path yang tercetak di
log/JSON atau kode snapshot adalah path saat eksekusi, bukan error yang harus "diperbaiki"
dengan mengedit evidence. Tautan Markdown navigasi diperbarui sesuai lokasi baru.
Jangan membuka semua bukti sekaligus; gunakan tautan pada baris acceptance/task aktif.
