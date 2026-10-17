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
| [P1_06_MODEL_CONTRACT_REPORT.md](P1_06_MODEL_CONTRACT_REPORT.md) | Implementasi F-01/F-02, penjelasan sederhana, kode dan hasil tes offline 12 Oktober |
| [P1_06_CODE_APPENDIX.md](P1_06_CODE_APPENDIX.md) | Sepuluh file source snapshot P1-06; baca bagian yang terkait |
| [p1-06-evidence](p1-06-evidence/README.md) | Output validator/matrix/scope sesi P1-06; bukan tes live baru |
| [P1_09_P1_10_LIMITS_COST_REPORT.md](P1_09_P1_10_LIMITS_COST_REPORT.md) | Per-milestone: bug reset anggota, shared limits, token/biaya kedua alias, hasil dan batas bukti |
| [P1_09_P1_10_CODE_APPENDIX.md](P1_09_P1_10_CODE_APPENDIX.md) | Sebelas file source lengkap dengan SHA-256; baca hanya bagian terkait |
| [p1-09-10-evidence](p1-09-10-evidence/README.md) | Output aktual offline/smoke/live, before-after bug, cleanup/accounting dan scope |
| [P1_11_P1_12_OPENCODE_REPORT.md](P1_11_P1_12_OPENCODE_REPORT.md) | Per-milestone: onboarding asli, agent kedua alias sampai hasil tool digunakan, streaming, hasil dan batas |
| [P1_11_P1_12_CODE_APPENDIX.md](P1_11_P1_12_CODE_APPENDIX.md) | Delapan file source lengkap dan SHA-256 |
| [p1-11-12-evidence](p1-11-12-evidence/README.md) | Output unit/smoke/live aktual, cleanup, health, runtime dan scope17Oktober |
| [PHASE1_FINAL_CROSSCHECK_REPORT.md](PHASE1_FINAL_CROSSCHECK_REPORT.md) |Laporan aktif penutupan menyeluruh; IN_PROGRESS sampai seluruh gate yang relevan terbukti |
| [PHASE1_FINAL_CODE_APPENDIX.md](PHASE1_FINAL_CODE_APPENDIX.md) |32file kode penuh dan hash; buka bagian terkait setelah membaca laporan |
| [PHASE1_RELEASE_DECISIONS.md](PHASE1_RELEASE_DECISIONS.md) |O-08targetCI disetujui/dijalankan; proposalCVE/server masihOPEN |
| [PHASE1_MAIN_PROMOTION_PROPOSAL.md](PHASE1_MAIN_PROMOTION_PROPOSAL.md) |Usulan non-force untuk main yang historynya terpisah; belum merge/promosi |
| [phase1-final-evidence](phase1-final-evidence/README.md) |Full regression baru, native errors/retry, CI/locks/security, privacy dan maintenance |

Output `.txt`/`.json` historis dipindahkan **tanpa mengubah byte**. Path yang tercetak di
log/JSON atau kode snapshot adalah path saat eksekusi, bukan error yang harus "diperbaiki"
dengan mengedit evidence. Tautan Markdown navigasi diperbarui sesuai lokasi baru.
Jangan membuka semua bukti sekaligus; gunakan tautan pada baris acceptance/task aktif.
