# Rencana penutupan Phase 1

Disusun 2026-10-12, Asia/Jakarta, dari [master](../MASTER_CONTEXT.md),
[acceptance Phase 1](phase-1.md), [register keputusan](../adr/README.md), dan source/Git aktual.
Dokumen ini mengurutkan pekerjaan tersisa; status acceptance tetap dimiliki `phase-1.md`.
Nomor urutan di bawah adalah paket pengerjaan, bukan milestone atau phase baru.

**Checkpoint aktif17Oktober2026:** user meminta lanjut sampai akhir dan full
cross-check/test. P1-06/P1-09…P1-13 memiliki bukti lokal; lock, auditprivasi, restore,
rotasi key dan configrollback diperluas padaP1-FINAL. CI lokal config63/infra31/
E2E97unitPASS; fullrun97unit/5smoke/30live/2outage+13nativePASS,exit0. O-08 menetapkan
hosted offline + live manual4000; enam CI candidate PASS dan docs #1 tersedia.
O-09 menyetujui penyiapan tiga draft PR promosi ke main dengan kedua history
dipertahankan dan tree identik candidate. Review/merge masih terbuka.
Pilot nyata/peserta/PIC ditunda
O-07. Lanjut dari [laporan aktif](../reports/PHASE1_FINAL_CROSSCHECK_REPORT.md),
bukan dari posisi awal12Oktober di bawah. Target live CI telah disetujui O-08;
CVE/server tetap memerlukan
[keputusan konkret](../reports/PHASE1_RELEASE_DECISIONS.md); Phase2 belum dimulai.

## Posisi awal yang sudah diperiksa

- H1–H10D memiliki bukti lokal tanggal 2026-10-10. Tes live tidak diulang pada sesi perencanaan ini.
- Config aktif tetap dua alias OpenAI sesuai kontrak. Source validator masih belum menolak
  exact upstream yang salah atau alias tambahan; konsistensi seluruh katalog belum dijaga.
- Repo docs berada pada commit `1d07d02` dan bersih sebelum pembaruan rencana ini.
  Commit lokal terverifikasi; push/review remote belum diperiksa.
- Source komponen belum tersimpan seluruhnya pada HEAD: config `b2cf9b0` (9 path berubah),
  infra `05f7749` (27), E2E `6151e07` (16). Hitungan mencakup modified/deleted/untracked.
- Tiga Markdown root sudah tidak ada. Context aktif di repo docs; sumber awal di `archive/`.
- P1-17 pilot dan P1-18 release/sign-off belum mempunyai bukti selesai.

## Batas pengerjaan yang tetap berlaku

Gunakan Docker existing port 4000; jangan membuat staging, environment atau container baru.
Pertahankan OpenAI-only, mapping `company-fast` ke `openai/gpt-5.6-terra` dan
`company-coding` ke `openai/gpt-5.6-sol`, satu HTTP client E2E, dan histori audit.
Pemilihan Sol 6.1 sebagai assistant pengembangan tidak mengubah mapping gateway ini.
Custom UI, SSO, Control Plane dan HA tetap berada pada phase berikutnya.

## Urutan pekerjaan dan bukti selesai

| Urutan | ID roadmap / gap | Pekerjaan dalam bahasa sederhana | Bukti yang harus tersedia |
|---|---|---|---|
| 1 | P1-06 / F-01, F-02 | Kunci konfigurasi agar hanya dua alias, provider dan model yang disepakati dapat lolos. Cocokkan katalog, provider YAML dan runtime; periksa jalur release juga. | Config benar PASS; alias tambahan/hilang/duplikat, upstream/provider salah, serta katalog berbeda harus FAIL. Format filename sebagai identitas model tetap dipertahankan. |
| 2 | P1-09, P1-10 / F-05 | Buktikan batas request/token dan budget pada key, user/member dan team sesuai dukungan versi terpasang. Cocokkan usage, token dan biaya tiap alias dengan data provider. | Pengerjaan/tes final pilot memakai pilot.yaml sesuai O-06/ADR-016. Pengujian batas tercapai dan ditolak, interaksi/reset limit terdokumentasi, token/biaya diperiksa, serta keterlambatan/selisih rekonsiliasi dijelaskan. Skenario tes dibatasi sesuai policy; cap/alert provider tetap perlu ditetapkan; kemampuan yang tidak tersedia tidak diasumsikan ada. |
| 3 | P1-11, P1-12 / F-06 | Jalankan OpenCode memakai virtual key developer untuk kedua alias, streaming, tool call sampai hasil tool diterima, dan tugas coding kecil dari awal sampai selesai. | Onboarding dapat diulang, kedua alias terbukti, perubahan kode contoh dan verifikasinya tercatat. API forced tool call saja belum menutup acceptance agent. |
| 4 | P1-02, P1-13 / F-07 | Periksa provider 429/5xx/timeout, retry dan respons error. Buktikan akses dan budget berperilaku benar saat dependency terganggu. | Kasus provider dengan simulasi terkontrol dibedakan dari tes integrasi; bukti invalid/blocked/denied/budget dan key valid saat outage, recovery dan konsistensi data. Jangan sengaja membanjiri provider. Drill outage existing dijadwalkan agar layanan pengguna tidak terganggu tanpa koordinasi. |
| 5 | P1-00, P1-02, P1-03, P1-15 / F-03, F-04, F-10 | Tutup persyaratan akses bersama: TLS, batas jaringan/admin, kerahasiaan log dan spend storage, rotasi secret, owner/billing/lisensi dan keputusan CVE. Catat alasan Redis dipertahankan. | Bukti akses yang dibolehkan/ditolak pada target yang disetujui, pemeriksaan data/log tersanitasi, hasil scan aktual dan keputusan pemilik atas temuan. Mengganti image/jaringan/retensi mengikuti keputusan major dahulu. |
| 6 | P1-01, P1-14, P1-16 / F-08, F-09 | Siapkan candidate yang dapat direproduksi: dependency lock, SHA tiap repo dan image digest, perbaiki target live CI yang masih menyebut staging, lengkapi deploy/rollback/rotasi/backup luar host. | Perubahan tercakup commit/review, required CI candidate hijau, operator lain dapat mengikuti runbook, kompatibilitas config/image/schema dan jalur rollback jelas. Backup terenkripsi di lokasi yang disetujui; source checkout bersih saat capture candidate. |
| 7 | P1-03–P1-16 | Jalankan pemeriksaan akhir terhadap candidate yang sama sebelum diserahkan untuk deploy. Sesudah deploy oleh operator, verifikasi kondisi server tujuan. | Static/lint/validator, unit, smoke/live, OpenCode, security scan, persistence, backup/restore dan rollback yang relevan PASS atau pengecualian eksplisit disetujui. Evidence lokal dan server dibedakan. Bug diperbaiki lalu tes terkait diulang; perubahan candidate membatalkan hasil yang terdampak. |
| 8 | P1-17 | Pilot dengan 2–5 developer nyata: akses model, onboarding, biaya, batas pemakaian dan feedback. | Peserta/owner/budget disetujui, bukti penggunaan tersanitasi, issue log dan hasil tindak lanjut. Fixture tes bukan peserta pilot. |
| 9 | P1-18 | Review exit gate bersama owner dan tetapkan versi rilis Phase 1. | Seluruh P1-00…P1-18 ditutup dengan evidence atau pengecualian yang disetujui, refs/tag tiap repo dan manifest lintas repo, hasil CI, serta sign-off tercatat. |

Paket 2–4 dapat disiapkan setelah kontrak paket 1 stabil. Keputusan paket 5–6 perlu
dibahas lebih awal karena menjadi prasyarat target bersama, CI live dan pilot.
Paket 7 adalah verifikasi candidate akhir, bukan pengulangan semua tes setiap kali file docs berubah.
Deploy ke server terjadi setelah pemeriksaan sebelum deploy pada paket 7 dan otorisasi target;
Phase 1 baru ditutup setelah verifikasi server/pilot/sign-off bila target rilis adalah server tersebut.

## Keputusan yang masih memerlukan pemilik project

| ID | Keputusan | Persiapan yang dapat dilakukan dahulu |
|---|---|---|
| M-01 / ADR-015 | Server/domain, akses pengguna/admin, cara CI menjangkau target tanpa staging, dan jadwal maintenance | Audit workflow/runbook; siapkan pilihan dengan dampak jaringan/downtime dan rencana rollback. Jangan membuka akses atau mengubah target remote sebelum keputusan. |
| M-02 / ADR-008 | Alasan dan peran Redis pada instalasi existing | Periksa konfigurasi/cache/rate limit dan dokumentasikan penggunaan aktual. Pertahankan Redis saat analisis. |
| M-04 / ADR-013 | Patch/upgrade image atau penerimaan risiko CVE oleh owner | Siapkan hasil scan dan analisis kompatibilitas/migrasi/rollback. Upgrade/recreate dan perubahan baseline memerlukan keputusan. |
| M-05 / ADR-016, ADR-017 | Policy pengerjaan/tes final pilot disetujui O-06; PIC layanan/security/billing/reviewer, akun/billing OpenAI, cap provider, lisensi, peserta dan aturan data/retensi masih OPEN | Pakai pilot.yaml dan batasi skenario tes; inventarisasi kebutuhan dan fitur yang dipakai. Jangan menebak approval bagian lain, kemampuan berlisensi atau membuang histori. |

M-03 penempatan dokumentasi selesai. Commit docs lokal sudah ada; publikasi remote tetap
perlu diperiksa. Bukti direct API/akun perusahaan pada P1-00 diperiksa lewat akses aman yang
disetujui; keberhasilan inference melalui gateway tidak membuktikan kepemilikan billing.

## Progres paket pertama

**P1-06 / F-01–F-02**, memperkuat kontrak yang sudah disepakati. Source utama:

- [Runtime validator](../../llm-gateway-config/scripts/ci/validate-runtime-config.py).
- [Catalog validator](../../llm-gateway-config/scripts/ci/validate-model-catalog.py).
- [Runtime config](../../llm-gateway-config/config/litellm_config.yaml),
  [provider catalog](../../llm-gateway-config/providers/openai.yaml),
  [fast catalog](../../llm-gateway-config/models/company-fast.yaml),
  [coding catalog](../../llm-gateway-config/models/company-coding.yaml).
- [Release manager](../../llm-gateway-infra/scripts/release/manage.py).
- [Model E2E assertions](../../llm-gateway-e2e/tests/test_models.py).

Setelah sesi rencana, user meminta paket pertama dikerjakan. P1-06/F-01/F-02 kini
**LOCAL_VERIFIED static/offline**: 63 tes config, 22 infra dan 29 unit E2E PASS;
lihat [laporan/kode](../reports/P1_06_MODEL_CONTRACT_REPORT.md). Gate commit/review/CI remote
dan live assertion terbaru tetap terbuka. Tidak ada deployment/provider/outage.
**Paket 2: P1-09/P1-10 — keputusan sebelum implementasi**. Pada 2026-10-13, user mengoreksi acuan pengerjaan/tes
final pilot ke [pilot.yaml](../../llm-gateway-config/policies/teams/pilot.yaml):
kedua alias, team US$10, anggota US$2, RPM30/TPM100000; script existing memakai durasi
team `30d`. Detail di [ADR-016](../adr/016-pilot-limits.md). Berikutnya audit jalur
policy→API→nilai tersimpan, reset budget dan tes dikerjakan pada sesi P1-09/P1-10
yang dicatat berikutnya.

## Progres paket kedua

P1-09/P1-10 kini **LOCAL_VERIFIED 2026-10-13**: bug durasi anggota null diperbaiki
menjadi30d, policy asli tersimpan, shared RPM/TPM/recovery dan budget key/member/team
PASS. Reset otomatis fixture mengikuti scheduler existing dan cumulative spend tetap
ada. Dua alias mempunyai token, biaya dan atribusi yang cocok dengan respons provider
serta harga standar resmi. Hasil final147 offline,4 smoke,11 live PASS;
[laporan sederhana, kode dan evidence](../reports/P1_09_P1_10_LIMITS_COST_REPORT.md).

`30d` pada instalasi ini memakai awal bulan berikutnya UTC; scheduler597–605detik.
Anggota lama tidak dimigrasikan, invoice billing/workload lain tidak direkonsiliasi,
cap provider/peserta/PIC dan commit/review/candidate masih perlu ditutup. Sembilan asset
aktif tetap identik dan tidak ada restart/container baru atau deployment.
Paket3 dilaksanakan setelah user meminta melanjutkan pada17Oktober; hasilnya di bawah.

## Progres paket ketiga

P1-11/P1-12 **LOCAL_VERIFIED 2026-10-17**: script onboarding asli dengan policy pilot,
key developer, kedua agent OpenCode2.0.18 menjalankan read→edit→shell verifier lalu
memakai receipt acak dari hasil tool. Kode hasil diperiksa independen; API SSE sampai
DONE dan structured tool call kedua alias PASS. Sesi ini 79 unit,5 smoke,6 live terfokus
PASS; [laporan sederhana, kode dan evidence](../reports/P1_11_P1_12_OPENCODE_REPORT.md).

Template bersama/policy/runtime tetap identik; Docker Desktop yang semula mati dinyalakan
dan tiga container existing kembali dengan ID/image sama. Empat team/empat key fixture
terblokir tanpa menghapus audit. Ini tugas Python kecil, bukan proyek besar/Responses
parity, pilot nyata, seluruh22live atau release candidate.
**Next paket4: P1-13/F-07**, failure semantics provider/dependency. Rekomendasi belum
dijalankan otomatis: siapkan skenario aman, recovery dan koordinasi sebelum outage.

## Laporan setiap paket

Catat ID, masalah awal, file/perubahan kode, tujuan, command/hasil tes aktual, lokasi
evidence tersanitasi, batas hasil, keputusan owner, commit/review bila ada dan next task.
Simpan laporan di `reports/`, update baris terkait pada [Phase 1](phase-1.md) dan append
checkpoint pada [work log](../handover/WORK_LOG.md). Status `DONE_VERIFIED` mengikuti
Definition of Done, bukan hanya karena tes lokal hijau.
