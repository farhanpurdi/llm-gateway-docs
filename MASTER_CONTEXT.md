# Project Context Master — LLM Gateway

Versi konsolidasi 1.9 · diperbarui 2026-10-17 · Bahasa kerja: Indonesia.
**Baca [README](README.md) untuk navigasi, lalu mulai context proyek di sini.** Dokumen ini menggabungkan rancangan awal dan pekerjaan aktual;
keputusan desain tidak berubah hanya karena kode atau tes yang ada berbeda.

## 1. Konteks satu menit

Bangun gateway LLM internal perusahaan: **OpenCode → LiteLLM → OpenAI API**.
Developer memakai virtual key, bukan master/provider key. PostgreSQL menyimpan identitas,
key, dan spend. LiteLLM adalah **Data Plane**; custom **Control Plane** baru Phase 2.

| Kontrak Phase 1 yang dipertahankan | Nilai |
|---|---|
| Provider | **OpenAI saja**, tidak ada cross-provider fallback |
| Alias fast | `company-fast` → `openai/gpt-5.6-terra` |
| Alias coding | `company-coding` → `openai/gpt-5.6-sol` |
| Client pertama | OpenCode; jangan mengembalikan template lama tanpa mengecek versi |
| Repo | Tiga komponen: infra/config/e2e; dokumentasi: `llm-gateway-docs` |
| Environment yang diizinkan saat ini | **Docker existing, port 4000**; jangan membuat staging/environment/container baru |
| Posisi | **Phase 1: fungsi lokal teruji; exit gate/release/pilot belum selesai** |
| Phase 2 / Phase 3 | Belum dimulai; tidak otomatis aktif setelah H10D |

**H1–H10D adalah checkpoint teknis lokal, bukan pengganti P1-00…P1-18.**
Bukti terakhir 10 Oktober: 37 E2E/unit (22+3+12), 12 tes operasional, OpenCode fast smoke,
restore 83 tabel, config release/rollback, dan scan sesuai baseline lulus.
Bukti tersebut dibaca ulang pada sesi konsolidasi; **bukan pengujian live baru**.
Pada 12 Oktober, P1-06/F-01/F-02 diimplementasikan: 63 tes config, 22 infra dan 29 unit E2E
PASS static/offline. Gate publikasi/live candidate/pilot tetap terbuka; lihat [laporan](reports/P1_06_MODEL_CONTRACT_REPORT.md).
Pada 13 Oktober, user mengoreksi acuan pengerjaan dan pengujian final pilot menjadi
`policies/teams/pilot.yaml` (O-06), menggantikan pilihan default sebelumnya:
kedua alias, budget team US$10, anggota US$2, RPM30/TPM100000. Script existing memakai
durasi team `30d`. P1-09 memperbaiki durasi anggota yang null menjadi `30d`.
Pada LiteLLM1.104.0 existing, reset `30d` ke awal bulan berikutnya 00:00 UTC;
scheduler memeriksa sekitar setiap10menit. P1-09/P1-10 kini LOCAL_VERIFIED:
147 tes offline, 4 smoke dan 11 live PASS. [Laporan/kode/batas](reports/P1_09_P1_10_LIMITS_COST_REPORT.md)
dan [ADR-016](adr/016-pilot-limits.md); Phase 1 exit gate tetap terbuka.
Pada17Oktober, P1-11/P1-12 LOCAL_VERIFIED: onboarding operator asli dan workflow
OpenCode2.0.18 kedua alias read→edit→shell→hasil tool PASS, kode diperiksa independen,
SSE/API tools kedua alias PASS. Sesi ini 79 unit/5 smoke/6 live terfokus PASS;
[laporan/kode/batas](reports/P1_11_P1_12_OPENCODE_REPORT.md). Ini bukan pilot nyata.

**Pekerjaan aktif:** user meminta lanjut sampai akhir dan full cross-check/test.
Full run akhir **PASS, exit0**:97unit,5smoke,30live,2outage dan13skenario native.
Config63tes dan infra31tes(23operasi+8regresi Compose) PASS lokal. Restore83tabel,
rotasi key kedua alias, config rollback dan audit privasi/cleanup PASS. Tiga candidate
sudahcommit/push sebagai draftPR kedevelop existing; CI/review dan docs candidate
masih dituntaskan. [Laporan](reports/PHASE1_FINAL_CROSSCHECK_REPORT.md),
[manifest source](reports/phase1-final-evidence/candidate-source-manifest.json)
dan checkpoint terbaru [work log](handover/WORK_LOG.md) menjadi acuan kelanjutan.
**O-07:**pilot nyata/peserta/PIC ditunda. **O-08:**CIofflineGitHub + full live manual
Dockerexisting4000 disetujui; workflowstaging lama dihapus. Keduanya bukan pilotPASS,
waiverCVE/TLS/server atau sign-offPhase1. Policy tes O-06 tetap sama.

## 2. Urutan baca dan pemilik informasi

1. Baca master ini seluruhnya.
2. Baca **[Phase 1](architecture/phase-1.md)**: tabel P1, pemetaan H, bukti, gap, next task.
3. Baca **[Keputusan dan evaluasi drift](adr/README.md)** sebelum mengubah scope/arsitektur.
4. Baca **[Log dan handoff aktif](handover/WORK_LOG.md)** untuk checkpoint terbaru.
5. Hanya bila relevan, baca [Phase 2](architecture/phase-2.md) atau [Phase 3](architecture/phase-3.md).
6. Buka source/runbook/bukti yang ditautkan oleh item aktif; jangan memuat semua arsip kode di awal chat.

| Dokumen | Perannya sekarang |
|---|---|
| `MASTER_CONTEXT.md` | Satu pintu masuk dan aturan lintas fase; master konsolidasi aktif |
| `architecture/phase-1.md` | Pemilik status acceptance P1 dan pemetaan ke H1–H10D |
| `architecture/phase-2.md`, `architecture/phase-3.md` | Roadmap masa depan; tidak berisi klaim implementasi |
| `adr/README.md` + `adr/001…017-*.md` | Register keputusan/drift; detail setiap ADR mempertahankan ID asli |
| `handover/WORK_LOG.md` | Catatan perubahan context, bukti dan tugas berikutnya |
| [PROJECT_MASTER_CONTEXT.md](archive/PROJECT_MASTER_CONTEXT.md) | Baseline rancangan asli; teks PLANNING/TODO adalah snapshot awal |
| [LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md](archive/LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md) | Arsip detail H1–H10; potongan kode/status lama bukan instruksi eksekusi terbaru |
| [Laporan H1–H10](reports/PHASE1_H1_H10_REPORT.md) | Hasil sesi implementasi sebelumnya, bukan penutupan seluruh gate awal |

Kedua sumber asli dipertahankan, hanya diberi penunjuk baca. Jangan memperbarui tiga master
secara paralel. Status aktif cukup di dokumen fase; master tetap ringkas dan log append-only.
Permintaan user terbaru memusatkan semua dokumentasi/laporan ke repo `llm-gateway-docs` yang sudah ada.
Dokumen root lama sudah tidak ada pada pemeriksaan 2026-10-12; rancangan awal dan handoff lengkap berada di `archive/`.
Ini perubahan kepemilikan dokumentasi yang diizinkan, bukan perubahan Data Plane/roadmap fase.

## 3. Urutan otoritas dan disiplin bukti

Permintaan eksplisit terbaru user → ADR yang disetujui → master konsolidasi + baseline
keputusan yang dirujuk → source/bukti kondisi terpasang → catatan historis.
**Source membuktikan keadaan aktual, bukan mengesahkan penyimpangan desain.**
Usulan/temuan tidak menjadi persetujuan hanya karena ditulis dalam dokumen.

| Status | Arti |
|---|---|
| `LOCAL_VERIFIED` | Ada implementasi dan bukti lokal dalam batas skenario yang disebut |
| `PARTIAL` | Sebagian acceptance terbukti, sisanya belum |
| `OPEN` / `NOT_VERIFIED` | Keputusan/bukti belum tersedia; bukan otomatis bug |
| `NOT_STARTED` | Pekerjaan belum dimulai |
| `APPROVED_OVERRIDE` | Perubahan spesifik yang memang diinstruksikan user; jangan perluas cakupannya |
| `PROPOSED` | Belum diizinkan/diterapkan |
| `DONE_VERIFIED` | Acceptance lengkap + commit/PR/review sesuai policy + bukti + docs |

Jangan menyamakan file dibuat, pytest collection, scan PASS, health HTTP 200, atau test
unit dengan acceptance live/production. Kegagalan lama yang sudah diperbaiki tetap ada
sebagai riwayat. Model access terbukti melalui gateway untuk credential saat tes;
akses langsung API/billing corporate dan akurasi harga belum otomatis terbukti.

## 4. Aturan yang tidak boleh dilanggar

- Phase 1 tetap dua alias dan OpenAI saja. Perubahan mapping/provider membutuhkan ADR/persetujuan.
- Jangan membangun custom UI, SSO, backend control plane, billing engine atau HA pada Phase 1.
- Security minimum (TLS lintas mesin, secret, ACL, backup) tetap Phase 1; enterprise scale Phase 3.
- Gunakan satu `LiteLLMClient` di E2E: `tests/client.py` HTTP, `conftest.py` fixture/cleanup,
  `test_*.py` assertion. Jangan tambah admin client abstraction kedua.
- `models/*.yaml`: identitas dari filename; bukan file config runtime yang otomatis di-load.
- Jangan hard-delete audit. Offboarding sekarang snapshot + koordinasi freeze provisioning;
  belum ada atomic revocation terhadap penerbitan key bersamaan atau integrasi SSO.
- Redis ada dan menjadi dependency operasional sekarang, tetapi kebutuhan distributed cache/
  rate limiting belum dibuktikan. Jangan menghapusnya atau mengklaim wajib desain tanpa keputusan.
- Jangan menaikkan vulnerability baseline diam-diam. PASS baseline bukan zero vulnerabilities.
- Jangan menaruh `.env`, raw virtual key, dump, prompt sensitif, atau salt dalam Git/context.
- Jangan membuat staging lagi. Perintah scanner default yang membuat container juga tidak
  dijalankan pada constraint sekarang; gunakan opsi native bila pengujian memang diperlukan.
- Perubahan major harus dijelaskan dahulu: masalah, opsi, dampak, risiko, migrasi/rollback,
  dan persetujuan user. Sesi konsolidasi ini tidak mengimplementasikannya.

## 5. Keadaan penting dan langkah berikutnya

Root workspace bukan repo Git; tiga komponen dan satu repo dokumentasi terpisah.
Remote main docs cocokHEAD1d07d02 saat audit. Source komponen kini tersimpan pada
branchcandidate baru yang bersih; draftPR kedevelop mengikuti jalurPRH7/H8 yang
sudahmerged. Main tiga komponen masih initialREADME dan historynya terpisah;
jangan forcepush/mergeunrelated tanpa [keputusan promosi](reports/PHASE1_MAIN_PROMOTION_PROPOSAL.md).
Docs baru difinalisasi. CI lama bukan pengganti CI candidate yang sedang diperiksa.
Belum ada tag/sign-off/deployment server. Pilot nyata ditunda sementaraO-07.

**Risiko/gap yang harus dibaca sebelum deploy:**
- Validator config dan release mengunci exact upstream/provider/alias; F-01/F-02
  LOCAL_VERIFIED static/offline. Exposure API tepatduaalias diuji ulang pada fullsuite;
  publikasi candidate sudah ada; review/CI final harus sesuaiSHA terbaru.
- Gateway bind semua interface; TLS/admin isolation server belum dibuktikan.
  Audit lokal261rowspend/3666loglines tanpa isi pesan/rawkey serta296key/97teamblockedPASS;
  sampling sesi ini bukan jaminan seluruh trafik historis/masa depan.
- RPM/TPM shared+recovery, budget key/member/team dan reset anggota terbukti pada fixture
  existing4000; belum stress/concurrency/multi-pod atau penerapan peserta pilot nyata.
- Token/biaya kedua alias cocok dengan respons provider dan harga standar resmi;
  invoice billing/cache/tier/workload lain belum direkonsiliasi. Harga snapshot13Oktober.
- OpenCode kedua alias terbukti pada tugas Python kecil dengan penggunaan hasil tool;
  proyek besar/semua tool/Responses parity dan pilot nyata belum dibuktikan.
- Provider429/500/timeout408+retry terbukti dengan simulasi SDK/router/handler native;
  HTTPmock berbahaya ditolak400. OutagePG/Redis membuktikan deny/recovery/spend lokal,
  bukan testprovidererror nyata/concurrency/HA. Lihat laporanP1-FINAL.
- Release/rollback hanya config, image/schema sama; bukan deployment server lintas versi.
- Scan ulang17Oktober:PostgreSQL1Critical/28High, Redis2High, LiteLLM0/0;
  baselinePASS bukan penerimaan risiko deploy. TargetliveCI disetujuiO-08; CVE/server memerlukan
  [keputusan konkret](reports/PHASE1_RELEASE_DECISIONS.md).

**Sesi terbaru17Oktober:** P1-11/P1-12 dikerjakan atas instruksi melanjutkan user.
Onboarding operator asli/policy pilot, agent kedua alias, SSE/API tools LOCAL_VERIFIED;
[79 unit/5 smoke/6 live terfokus PASS](reports/P1_11_P1_12_OPENCODE_REPORT.md).
Docker Desktop semula mati lalu dinyalakan; tiga container existing berjalan kembali
dengan ID/image sama. Tidak membuat environment/container atau mengubah template/policy.
Empat team/empat key fixture diblokir dan audit dipertahankan; candidate/release tetap terbuka.

**Sesi13Oktober:** P1-09/P1-10 dikerjakan sesuai `pilot.yaml` (O-06). Bug durasi anggota
diperbaiki; persistence/limits/reset dan token/biaya kedua alias LOCAL_VERIFIED,
[147 offline +4 smoke +11 live PASS](reports/P1_09_P1_10_LIMITS_COST_REPORT.md).
Identitas tes diblokir, audit dipertahankan; sembilan asset config/policy tetap identik
dan tiga ID container sama. P1-06/F-01/F-02 sebelumnya tetap LOCAL_VERIFIED,
[114 tes offline pada snapshot12Oktober](reports/P1_06_MODEL_CONTRACT_REPORT.md).
P1-CLOSEOUT-PLAN/DOC-MIGRATE/DOC-CONSOLIDATE tetap tercatat sebagai sesi sebelumnya.
**Next action aktif:** tutup CI candidate dan docsPR/validasi, lalu review keputusan
promosi main/CVE/server yang tersisa. Full test, outage, rotasi, rollback dan privacy
lokal sudahPASS. Jangan mengulang paidtest untuk metadataCI saja tanpa alasan baru.
P1-09…P1-13 tetap LOCAL_VERIFIED; commit/review/CI/sign-off sesuai gate masing-masing
sebelum releaseDONE. Tidak mulai deployment atau Phase2 otomatis.
M-03 penempatan dokumentasi diselesaikan dengan repo docs existing atas instruksi user;
commit lokal docs terverifikasi, publikasi remote belum diperiksa.
M-01/M-02/M-04 tetap terbuka; bagian lain M-05 (PIC/billing/provider cap, lisensi,
data/retensi dan peserta pilot) tetap terbuka dalam register drift.

## 6. Prompt chat baru

```text
Mulai dari llm-gateway-docs/README.md dan llm-gateway-docs/MASTER_CONTEXT.md.
Lanjutkan architecture/phase-1.md, adr/README.md, handover/WORK_LOG.md di repo docs.
Pertahankan OpenAI-only, dua alias yang ditetapkan, tiga repo komponen dan Docker existing 4000.
H10D lokal selesai bukan Phase 1 exit gate. Cocokkan source/Git dengan bukti sebelum coding.
Kerjakan item yang diminta; P1-06/F-01/F-02 LOCAL_VERIFIED static/offline.
P1-09/P1-10 LOCAL_VERIFIED: 147offline/4smoke/11live PASS; lihat laporan sesi13Oktober.
Pilot memakai pilot.yaml (O-06): kedua alias, teamUS$10/anggotaUS$2/RPM30/TPM100000.
Durasi team/anggota30d memakai awal bulan berikutnya UTC; pemeriksaan reset sekitar10menit.
P1-11/P1-12 LOCAL_VERIFIED17Oktober:79unit/5smoke/6live terfokus PASS, bukan seluruh suite.
Lanjut checkpointP1-FINAL sesuai instruksi user sampai akhir dan full test;
lihat laporan aktif/worklog untuk hasil terbaru dan proses yang masih berjalan.
Pilot nyata/peserta/PIC ditundaO-07, bukan pilot PASS. Bagian lain M-05/gate releaseOPEN.
Jangan outage tanpa koordinasi scope/recovery atau menjalankan tes gateway paralel.
Jangan buat staging atau mulai Phase 2; minta keputusan sebelum perubahan major.
Laporkan ID, file, hasil tes aktual, batasan, commit jika ada, dan update dokumen fase/log.
```
