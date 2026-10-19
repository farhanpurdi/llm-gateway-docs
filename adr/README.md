# Keputusan, evaluasi kesesuaian, dan perubahan yang tertunda

Baca [master](../MASTER_CONTEXT.md). Evaluasi 2026-10-10 memakai baseline
awal → handoff → source/bukti. Ini dokumen keputusan dan temuan; **bukan izin eksekusi**.

**Pembaruan 18 Oktober 2026:** Phase1 v0.0.1 ditutup dengan catatan melalui
APPROVED_OVERRIDE O-10. PR main merged; CVE diterima untuk fase ini; VM GCP/default/HTTP
awal, keamanan bertahap, snapshot/biaya menunggu manager dan target TTLRedis24jam
dicatat. [Tujuh feedback](../reports/PHASE1_V0_0_1_CLOSEOUT.md) mengungguli status
OPEN dalam snapshot review lama. Bukti implementasi yang belum ada tetap NOT_VERIFIED.

## 1. Kesimpulan evaluasi

Arsitektur utama **sesuai rancangan**: LiteLLM Data Plane, OpenAI saja, mapping kedua
alias tetap, virtual key, PostgreSQL, tiga repo, OpenCode, tanpa custom Control Plane/UI.
Tidak ditemukan perubahan provider atau pembangunan Phase 2/3 yang mendahului roadmap.
Backup, security scan, lifecycle dan runbook lebih rinci daripada MVP minimal, tetapi
masih relevan dengan security minimum dan acceptance P1; bukan alasan membuang pekerjaan.

Perbedaan terpenting adalah **cakupan bukti dan definisi selesai**. Handoff menutup H1–H10
lokal, sedangkan baseline menuntut P1-00…18, commit/review, pilot, sign-off dan tag release.
Konsolidasi ini mengoreksi pembacaan status, **tidak mencabut hasil tes yang memang lulus**.
Pada snapshot10Oktober, Phase1 belum selesai menurut exit gate awal. O-10 kemudian
menyetujui penutupan18Oktober dengan pengecualian eksplisit; hasil review lama tetap
menjelaskan gap, bukan membatalkan penerimaan pengguna yang lebih baru.

## 2. ADR awal dipertahankan

| ID | Keputusan awal / status asli | Posisi setelah evaluasi |
|---|---|---|
| ADR-001 | LiteLLM Data Plane / CONFIRMED | Sesuai implementasi |
| ADR-002 | OpenAI-only Phase1 / CONFIRMED | Runtime sesuai; exact guard F-01/F-02 terverifikasi static/offline 12 Oktober |
| ADR-003 | fast→Terra / CONFIRMED | Runtime sesuai; jangan substitusi diam-diam |
| ADR-004 | coding→Sol / CONFIRMED | Runtime sesuai; jangan substitusi diam-diam |
| ADR-005 | OpenCode client awal / CONFIRMED | Sesuai; workflow agent kecil kedua alias LOCAL_VERIFIED17Oktober, release/pilot nyata tetap belum |
| ADR-006 | Virtual key user/team, provider key server / BASELINE | Dipakai dan dites; bukan izin master key di client |
| ADR-007 | PostgreSQL sejak Phase1 / BASELINE | Terpasang, restore teruji |
| ADR-008 | Redis opsional saat bootstrap / BASELINE | Redis existing dependency operasional; O-10 mencatat target TTL24jam dan belum ada pembatasan pengguna Redis tambahan. Cache native/TTL dan alasan distributedcache belum dibuktikan |
| ADR-009 | Alias sebagai kontrak / BASELINE | Exact alias/upstream dan konsistensi katalog/runtime diperiksa; LOCAL_VERIFIED static/offline, gate release belum |
| ADR-010 | Control Plane terpisah mulai Phase2 / BASELINE | Belum dibangun; tetap tertunda |
| ADR-011 | Tiga repo; root/submodules bila root Git / BASELINE | Empat sibling repo dipertahankan. PR config#4/infra#7/E2E#6/docs#1 main merged; tree identik candidate. Root bukan Git/monorepo |
| ADR-012 | Git desired config, satu writer policy / BASELINE | Manual Git→API pada P1; konsistensi katalog dijaga validator config; reconciler tetap Phase2 |
| ADR-013 | Repo/image/dependency pinned saat deploy / BASELINE | Source main/CI/pin dan3lock berhash tersedia. O-10 menetapkan versi v0.0.1 serta penerimaan CVE fase ini; tag belum dibuat; dua kandidat DHI hanya evaluasi mendatang |
| ADR-014 | IdP SSO / OPEN | Tetap OPEN, tidak menebak vendor |
| ADR-015 | Hosting final / OPEN pada baseline | Target VM GCP/default/HTTP awal dan keamanan bertahap dipilih O-10. Hostedoffline/live manual4000 O-08 tetap. Deploy/keamanan VM belum diverifikasi |
| ADR-016 | Budget/RPM/TPM/jumlah user / OPEN pada baseline | Kini PARTIAL: policy pilot disetujui O-06; P1-09/P1-10 enforcement/reset/accounting LOCAL_VERIFIED13Oktober. Peserta, PIC/billing corporate dan cap/alert provider tetap OPEN |
| ADR-017 | Lisensi/fitur enterprise / OPEN | [Inventaris lisensi](../operations/license-inventory.md) bersumber resmi tersedia; penerimaan perusahaan dan inventaris client/dependency lengkap belum |

ADR-001…017 tetap memakai identitas asli. Keputusan penempatan dokumentasi baru tercatat
sebagai O-04 pada ADR-011 sesuai instruksi user; tidak menyetujui fitur runtime baru.

Detail tiap ADR ada di [indeks ADR](INDEX.md). Nomor contoh folder user tidak dipakai untuk
mengganti makna ID lama: ADR-002 tetap OpenAI-only; model alias adalah ADR-003/004/009.

## 3. Override user yang benar-benar diketahui

| ID | Instruksi/sumber | Cakupan | Yang tidak ikut disetujui |
|---|---|---|---|
| O-01 | User: Docker existing port4000, jangan staging/buat baru, hapus Compose staging | APPROVED_OVERRIDE untuk pekerjaan lokal H10; staging sebelumnya dibatalkan | Tidak otomatis menghapus semua release/security/pilot gate; tidak mengizinkan server/container baru |
| O-02 | User mengonfirmasi H7 merge gate GitHub sudah berjalan | Gate sebelumnya diterima sebagai konfirmasi user | Bukan bukti workflow candidate yang masih dirty sudah hijau |
| O-03 | User meminta gabungan context atau master+per-phase | Organisasi dokumen baru, evaluasi, navigasi sumber lama | Bukan izin perubahan major implementasi |
| O-04 | User meminta seluruh docs/report dipindah ke `llm-gateway-docs` dan handover diperjelas | Repo docs existing menjadi pemilik dokumentasi; master root lama menjadi penunjuk, ADR tetap bernomor asli | Bukan izin commit/push, parent Git/submodule, perubahan runtime atau penutupan gate Phase1 |
| O-05 | User 2026-10-13: limit final pilot memakai setting existing `default.yaml` | **SUPERSEDED oleh O-06** setelah user mengoreksi nama policy; dipertahankan sebagai riwayat | Bukan acuan pilot aktif; jangan memakai scope fast-only dari keputusan ini untuk final pilot |
| O-06 | Koreksi user 2026-10-13: gunakan `pilot.yaml` yang sudah disediakan untuk pengerjaan dan pengetesan final pilot | Policy pilot disetujui: `company-fast` dan `company-coding`, team US$10, anggota US$2, RPM30/TPM100000; script team existing memakai `30d`. Detail di [ADR-016](016-pilot-limits.md) | PIC/billing corporate, cap provider dan peserta belum diputuskan; persetujuan bukan bukti penerapan/enforcement pada team existing |
| O-07 | User2026-10-17 menjawab pertanyaan peserta pilot/PIC layanan-billing: "untuk itu bisa di skip dulu" | **APPROVED_OVERRIDE sementara:** pilot pengguna nyata P1-17 serta penentuan peserta/PIC yang ditanyakan ditunda; lanjut pekerjaan/pengujian teknis sampai tahap akhir | Bukan bukti pilot/feedback, penetapan PIC, approval billing/CVE/server, penghapusan gate teknis atau izin memulai Phase2 |
| O-08 | User17Oktober2026 memilih "Setuju A: CI offline + live lokal4000 (disarankan)" atas proposal M-01/ADR-015 | **APPROVED_OVERRIDE:** hapus workflow live staging lama, pertahankan hosted validate/security offline; full live manual existing4000 dengan sourceSHA/hash, image/digest, output+exit0, cleanup/recovery dan review bukti | Bukan candidateCI/sign-offPASS, waiverCVE/TLS/server, pemasangan runner/secrets baru atau izin deploy/Phase2. [Prosedur](../operations/local-release-gate.md) |
| O-09 | User 17 Oktober 2026: "Setuju, siapkan PR promosi main (disarankan)" atas opsi A [proposal promosi](../reports/PHASE1_MAIN_PROMOTION_PROPOSAL.md) | **APPROVED_OVERRIDE:** pertahankan kedua history melalui merge `--allow-unrelated-histories` pada branch baru, push tanpa force dan buat draft PR ke main. Tiga merge tree identik dengan candidate; config #4, infra #7, E2E #6 tersedia | Bukan izin merge protected main/develop, force-push, tag, deploy, perubahan image/container atau sign-off. Required review/checks dan gate CVE/server tetap berlaku |
| O-10 | Pengguna18Oktober2026 memberikan tujuh feedback dan menyatakan "versi rilis v0.0.1, phase 1 dapat di tutup dengan beberapa catatan" | **APPROVED_OVERRIDE:** penutupan Phase1 v0.0.1 dengan PR main merged, CVE image diterima untuk fase ini, dua kandidat DHI, VM GCP/default/HTTP awal dan keamanan bertahap, snapshot/biaya dibahas manager, target TTLRedis24jam serta belum ada pembatasan pengguna Redis tambahan. [Rincian keputusan](../reports/PHASE1_V0_0_1_CLOSEOUT.md) | Bukan bukti deploy/keamanan server, snapshot aktif, tag Git, cache/TTL sudah aktif, penghapusan CVE, approval biaya/lisensi perusahaan atau dimulainya Phase2/3. Pekerjaan ini hanya mencatat dan memberi panduan |

Urutan roadmap masih Phase1→Phase2→Phase3. Pengecualian staging mengikuti O-01;
bila target acceptance server/CI perlu berubah, desain alternatif harus dibahas dahulu.

## 4. Register temuan yang dapat ditindaklanjuti

| ID | Kategori / perbandingan baseline dengan fakta | Dampak dan tindak lanjut |
|---|---|---|
| F-01 | **Gap enforcement kontrak — LOCAL_VERIFIED 2026-10-12:** sebelumnya wrong upstream/extra alias lolos | Dua CLI config dan guard release sekarang menolak pelanggaran exact alias/model/provider/env, duplikat dan routing alternatif. Tes offline PASS; commit/review/live terbaru belum. [Laporan](../reports/P1_06_MODEL_CONTRACT_REPORT.md) |
| F-02 | **Gap konsistensi config — LOCAL_VERIFIED 2026-10-12:** sebelumnya katalog/provider/runtime terpisah tanpa cross-check | Kedua CLI memeriksa filename identity, route/status model dan provider metadata terhadap ADR/runtime. Drift serta perubahan bersama ke upstream salah ditolak. Katalog tetap deskriptif; belum generator/reconciler. [Bukti](../reports/p1-06-evidence/contract-matrix.json) |
| F-03 | **Drift operasional:** Redis opsional desain awal, tetapi Compose depends_on dan readiness/release kini membutuhkan Redis | Kebutuhan/rationale belum terbukti; jangan menghapus container. M-02 diperlukan sebelum perubahan dependensi |
| F-04 | **Exposure diputuskan bertahap O-10:** gateway lokal publish4000 semua interface; pengguna memilih VM GCP/default/HTTP awal | Keamanan HTTP/HTTPS/firewall/admin belum diterapkan/diverifikasi di VM; pengecualian penutupan dicatat, bukan bukti kontrol aman |
| F-05 | **Gap limits/cost ditutup lokal:** P1-09/P1-10 shared RPM/TPM/recovery, budget key/member/team, reset dan token/biaya kedua alias PASS; bug durasi anggota null diperbaiki | LOCAL_VERIFIED pada fixture/teks pendek/default tier; invoice billing, workload lain/concurrency, cap/alert provider dan candidate release tetap belum. [Laporan](../reports/P1_09_P1_10_LIMITS_COST_REPORT.md) |
| F-06 | **Gap OpenCode ditutup lokal 2026-10-17:** onboarding operator asli, agent kedua alias read/edit/shell/hasil tool dan kode hasil verifikasi PASS; SSE/API tools kedua alias PASS | LOCAL_VERIFIED pada fixture Python kecil/OpenCode2.0.18 dan adapter template existing. Bukan proyek besar/Responses parity/pilot nyata atau release DONE. [Laporan](../reports/P1_11_P1_12_OPENCODE_REPORT.md) |
| F-07 | **LOCAL_VERIFIED17Oktober:**13native SDK/router/handler simulated429/500/408+retry,6HTTPmockguard/recovery,2PG/Redis outage deny/recovery/spendPASS | Simulasi native dipisahkan dari providerIO nyata. PadaPGdown request tidak terverifikasi503; Redis belum menjadi nativecache. [Bukti](../reports/phase1-final-evidence/README.md); bukan concurrency/HA/releaseDONE |
| F-08 | **Release scope lebih sempit:** config-only rollback diulang 17 Oktober, inode/byte/ID/image sama; key rotation/restore PASS | Tiga lock berhash, commit/hash source dan CI candidate/promosi PASS tersedia. Review/tag/server belum; config-only bukan recovery lintas image/schema |
| F-09 | **Target diselesaikan O-08,17Oktober:** workflow live staging dihapus; hostedCIoffline + full live manual Dockerexisting4000 | [Gate lokal](../operations/local-release-gate.md) mengikat buktiSHA/hash/image/exit/cleanup dengan review. CandidateCI dan sign-off masih terpisah; tidak ada runner/secrets/environment baru |
| F-10 | **Audit privasi lokal PASS 17 Oktober:** 261 row spend tanpa messages/response/raw-key pattern, 3666 baris log tanpa raw-key/toy markers; secret scan PASS | Sampling bukan jaminan seluruh trafik/data/PII. Retention, akses admin dan penerimaan risiko produksi tetap terbuka; baseline CVE PASS bukan risk acceptance |
| F-11 | **Dokumen saling menimpa:** master awal PLANNING; handoff H10D COMPLETE; struktur staging/count lama masih terselip | Diselesaikan untuk navigasi dengan master aktif + status per-P1 + banner arsip. Jangan menjalankan ulang bootstrap dari snapshot awal |
| F-12 | **Penutupan disetujui O-10:** main empat repo merged dan teknis lokal/CI PASS; versi v0.0.1 ditetapkan | Manager/billing/license/data, deployment/snapshot/TTL/tag/pilot nyata tetap tercatat sebagai tindak lanjut; Phase2/3 tidak dimulai |

### Bukti awal F-01 — snapshot review 2026-10-10

[validator-contract-check.json](../reports/context-review/validator-contract-check.json)
menjalankan validator yang sama pada direktori sementara:

```text
unchanged config           → exit 0
wrong upstream/provider    → exit 0 (seharusnya ditolak oleh kontrak Phase1)
extra alias                → exit 0 (seharusnya ditolak oleh kontrak tepat dua alias)
```

Config asli tidak berubah; tidak ada Docker, provider request, atau deployment.
Source terkait: [validate-runtime-config.py](../../llm-gateway-config/scripts/ci/validate-runtime-config.py),
[validate-model-catalog.py](../../llm-gateway-config/scripts/ci/validate-model-catalog.py),
[test_models.py](../../llm-gateway-e2e/tests/test_models.py),
[release validator](../../llm-gateway-infra/scripts/release/manage.py).
Pada snapshot review tersebut, release validator belum memeriksa exact upstream.
Perbaikan 2026-10-12 memperketat guard release dan kedua CLI config; hasil terbaru pada
[laporan P1-06](../reports/P1_06_MODEL_CONTRACT_REPORT.md). Evidence lama tetap dipertahankan.

## 5. Perubahan major: beri tahu dan minta keputusan sebelum implementasi

**O-10 menutup Phase1 dengan catatan. M-01 memilih VM GCP/keamanan bertahap; M-02 mendapat target TTL24jam yang belum diterapkan; M-04 diterima sebagai risiko untuk fase ini; M-05 dibahas manager/pilot tetap ditunda. M-03 penempatan/publikasi/review/merge docs selesai. Tindak lanjut operasional tetap NOT_VERIFIED bila belum ada bukti.** Pilihan di bawah adalah bahan
keputusan, bukan roadmap baru yang diam-diam disetujui.

| ID | Keputusan yang dibutuhkan | Usulan yang dibahas dan trade-off | Batas tindakan saat ini |
|---|---|---|---|
| M-01 | Target verifikasi dan server tanpa staging; ADR-015 | O-08 hostedoffline/live manual existing4000 diterapkan; O-10 memilih VM GCP/default/HTTP awal dan keamanan bertahap | Penutupan fase disetujui dengan catatan; deployment/firewall/admin/TLS VM belum dieksekusi/diverifikasi oleh dokumentasi |
| M-02 | Peran Redis; ADR-008 | O-10 menetapkan target TTL24jam, belum ada pembatasan pengguna tambahan. Runtime belum memakai nativecache; readiness/release tetap membutuhkan Redis | Pertahankan existing. Tentukan scope key sebelum implementasi; belum mengaktifkan TTL/cache/ACL atau mengubah jaringan |
| M-03 | Penempatan/versioning context; ADR-011 | Selesai: repo docs existing, migrasi dipertahankan dan docs#1 main merged | Pembaruan closeout lokal perlu publikasi terpisah; tidak membuat parent Git/monorepo |
| M-04 | Penanganan CVE/image; ADR-013 | APPROVED_OVERRIDE O-10: risiko image diterima untuk Phase1; kandidat dhi.io/postgres:16.15-alpine3.23 dan dhi.io/redis:7.4.11-debian13 untuk evaluasi masa depan | Tidak mengganti image, recreate atau menaikkan baseline; temuan tidak dinyatakan hilang. Masa dukung/digest/kompatibilitas kandidat perlu diperiksa saat evaluasi |
| M-05 | Ownership/data/biaya pilot; ADR-016/017 | O-06 policy pilot tetap; O-07 pilot/peserta/PIC ditunda. O-10: biaya dan backup/snapshot dibahas manager, fase ditutup dengan catatan | Approval manager, invoice/cap provider, lisensi/retensi/ownership dan jadwal/restore snapshot belum dibuat-buat |

Memperkuat validator F-01/F-02 dan menambah tes acceptance pada kontrak yang sama adalah
penutupan gap Phase1, **bukan rewrite arsitektur**. Paket ini diimplementasikan setelah
user meminta langkah pertama dikerjakan pada 2026-10-12; LOCAL_VERIFIED static/offline.
Sesi P1-06 tidak menyetujui M-01/M-02/M-04/M-05. Pada 2026-10-13 user kemudian
menyetujui bagian limit pilot M-05 melalui O-05, kemudian mengoreksi policy menjadi
`pilot.yaml` melalui O-06 untuk pengerjaan/tes final pilot; bagian lain tetap OPEN.
Pembatalan staging sudah diizinkan O-01; tidak perlu meminta ulang izin yang sama.
Penghapusan gate pilot/security atau penerimaan keterbatasan besar juga keputusan major.

## 6. Risiko awal yang tidak boleh hilang saat pindah context

| Risiko awal | Status konsolidasi |
|---|---|
| R-01 model access | Kedua model via gateway teruji; ownership/billing/direct account validation masih sebagian |
| R-02 OpenCode parity | Agent workflow kecil kedua alias dan API tools/SSE terbukti17Oktober; proyek besar/semua tool/Responses parity tidak otomatis terbukti |
| R-03 cost | Harga standar/token/biaya kedua alias cocok; invoice/tier/workload lain dan corporate cap/alert masih terbuka; policy pilot disetujui O-06 |
| R-04 DB outage semantics | Request auth/budget saat outage dan recovery/spend retained PASS 17 Oktober pada existing lokal; bukan concurrency/HA proof |
| R-05 budget precedence | Key/member/team dan shared RPM/TPM teruji lokal; bukan concurrency/multi-pod/stress/prepaid cap atau migrasi seluruh anggota existing |
| R-06 dua writer policy | Manual Git/API sekarang; ownership per domain dan reconciler Phase2 wajib |
| R-07 disable SSO vs key | SSO belum ada; snapshot offboarding manual bukan deprovision end-to-end |
| R-08 licensing | OPEN; jangan mengasumsikan enterprise capability termasuk lisensi |
| R-09 ownership | PIC platform/security/billing/reviewer belum disahkan dalam bukti |
| R-10 hosting/domain/IdP/data region | VM GCP/default/HTTP awal dipilih O-10; domain, hardening dan deployment aktual belum diverifikasi |

## 7. Cara mencatat ADR berikutnya

Sebut ID, keadaan sebelum, masalah, opsi, pilihan, backward compatibility, dampak
security/cost/data, rencana test/migrasi/rollback, **siapa menyetujui dan kapan**, serta
PR/commit implementasi. Jika belum ada persetujuan, tulis PROPOSED. Jangan mengubah
CONFIRMED atau menutup exception hanya atas dasar rekomendasi model.
