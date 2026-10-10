> **Laporan historis:** hasil dan potongan source mengikuti sesi yang tercantum, bukan status current setelah migrasi.
> Baca [master aktif](../MASTER_CONTEXT.md) dan [Phase1](../architecture/phase-1.md); path pada blok kode/log bisa merupakan path lama.
> Tautan navigasi disesuaikan saat migrasi; hasil tes dan isi blok kode tidak diubah.

# Evaluasi rancangan awal vs pekerjaan aktual

2026-10-10 · Sesi dokumentasi/evaluasi, tanpa perubahan aplikasi atau Docker.

**Kesimpulan:** arah utama sesuai. Tetap LiteLLM, OpenAI-only, dua alias yang sama,
virtual keys, PostgreSQL, OpenCode dan tiga repo. Belum ada custom UI/Control Plane,
HA, atau provider lain yang melenceng dari fase.

**Koreksi penting:** H10D selesai lokal tidak sama dengan Phase1 P1-00…P1-18 selesai.
Hasil pengujian sebelumnya tetap sah, tetapi sebagian acceptance awal belum dibuktikan.

## Yang ditemukan

| Jenis | Temuan | Arti untuk kelanjutan |
|---|---|---|
| Gap terbukti baru | Validator menerima upstream tak disetujui dan alias tambahan pada salinan sementara | Perlu memperketat kontrak Phase1; config aktif tidak berubah dan tetap sesuai |
| Gap acceptance | Full coding agent OpenCode, token/pricing reconciliation, TPM/member-team budget dan provider errors | Tes yang sudah lulus belum menguji seluruh persyaratan awal |
| Scope operasional | Redis kini dependency wajib, gateway publish semua interface | Perlu alasan/keputusan, jangan menganggapnya otomatis rancangan final |
| Scope release | Rollback config pada image/schema sama | Tidak setara deployment/rollback compatible image+config lintas server |
| Override yang sah | User membatalkan staging dan memilih Docker existing4000 | Jangan membuat staging lagi; tentukan alternatif verifikasi release bila diperlukan |
| Governance | Source dirty, root docs di luar Git, pilot/tag/sign-off belum ada bukti | Phase1 exit gate tetap terbuka |
| Data/security | Scan PASS dengan CVE tersisa; log-minimization/TLS/admin isolation belum lengkap | Review security/privacy sebelum shared service |
| Context drift | Master lama PLANNING, handoff COMPLETE lokal dan detail usang tercampur | Master ringkas + fase + register drift sekarang memisahkan target dari fakta |

Bukti baru: [validator-contract-check.json](context-review/validator-contract-check.json).
Status per-task dan bukti terdahulu: [Phase1](../architecture/phase-1.md).

## Dokumen hasil konsolidasi

- [PROJECT_CONTEXT_MASTER.md](../MASTER_CONTEXT.md): pintu masuk chat baru dan batas roadmap.
- [PHASE_1.md](../architecture/phase-1.md): seluruh P1-00…18 dipetakan ke H1–H10D, bukti dan gap.
- [PHASE_2.md](../architecture/phase-2.md): roadmap Control Plane tetap NOT_STARTED.
- [PHASE_3.md](../architecture/phase-3.md): enterprise roadmap tetap NOT_STARTED.
- [DECISIONS_AND_DRIFT.md](../adr/README.md): ADR001–017, override user, F-01…12 dan M-01…05.
- [WORK_LOG.md](../handover/WORK_LOG.md): handoff aktif, provenance, aturan update, next task.

Dua dokumen awal hanya ditambah banner navigasi. Tubuh aslinya dipertahankan identik;
checksum sumber tercatat di [source-provenance.json](context-review/source-provenance.json).
Seluruh source ketiga repo tidak diubah oleh sesi ini. Tidak ada pengujian live baru,
commit/push, server deployment, perubahan workflow, atau keputusan arsitektur baru.

## Penyesuaian besar: belum dilaksanakan

1. **M-01 — release/server/CI target tanpa staging:** tentukan jaringan/TLS, compatible refs,
   runner reachability dan prosedur maintenance yang sesuai izin environment.
2. **M-02 — Redis:** sahkan alasan menjadi dependency wajib, atau bahas kembali sifat opsional
   beserta dampaknya. Container existing tetap dipertahankan.
3. **M-03 — Git untuk root context:** putuskan versioning parent/submodule atau publikasi
   docs terkontrol. Jangan otomatis mengubah tiga repo menjadi monorepo.
4. **M-04 — image/CVE:** pilih remediation yang kompatibel atau risk acceptance yang sah;
   tidak ada upgrade/downgrade atau kenaikan baseline pada sesi ini.
5. **M-05 — data/budget/licensing pilot:** tetapkan pemilik, batas biaya, log/retention,
   fitur berlisensi dan peserta. Angka config existing bukan keputusan corporate otomatis.

Tidak ada kebutuhan rewrite arsitektur yang terbukti saat ini. Usulan pekerjaan teknis
kecil pertama adalah **P1-06/F-01**, memperketat validator sesuai kontrak awal; belum
mulai dikerjakan. Keputusan major di atas harus dibicarakan dengan user sebelum implementasi.
