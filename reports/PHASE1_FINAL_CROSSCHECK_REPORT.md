# Cross-check dan pengujian akhir Phase 1

**Snapshot teknis17Oktober2026.** Pengguna kemudian mereview/merge PR main dan
menutup Phase1 v0.0.1 dengan catatan18Oktober melalui O-10. Untuk status saat ini
baca [closeout v0.0.1](PHASE1_V0_0_1_CLOSEOUT.md); status IN_PROGRESS di laporan ini
menjelaskan checkpoint sebelum penutupan, bukan pembatalan keputusan terbaru.

Tanggal: **17 Oktober 2026, Asia/Jakarta**. Status: **IN_PROGRESS**.
**Pengujian teknis lokal akhir dan CI promosi PASS**; review dan gate server masih terbuka.
User meminta melanjutkan sampai akhir, memeriksa dari awal dan menjalankan full test.
Scope tetap Docker existing port4000, environment Python existing, OpenAI saja dan
tepat dua alias. Tidak ada environment/container baru atau deployment server.

Baca laporan ini dahulu. [Bukti eksekusi](phase1-final-evidence/README.md) menyimpan
output aktual; [32 file kode lengkap](PHASE1_FINAL_CODE_APPENDIX.md) dibuka hanya
bila perlu meninjau implementasi. Status acceptance dimiliki
[Phase1](../architecture/phase-1.md), keputusan dimiliki [register ADR](../adr/README.md).

## 1. Keputusan pengguna yang dipertahankan

- **O-01:** Docker yang sudah ada di port4000; staging dibatalkan. Tidak membuat
  pengganti staging, container scanner, atau deployment baru.
- **O-06:** pengujian memakai policy `pilot.yaml` milik pengguna: dua alias,
  budget team US$10/anggota US$2, RPM30/TPM100000. File aslinya tidak diubah.
- **O-08:** pengguna menyetujui CI offline GitHub + full live manual existing4000.
  Workflow staging lama dihapus; [gate lokal](../operations/local-release-gate.md)
  mengikat bukti SHA/hash/image/output/cleanup dengan review.
- **O-09:** pengguna menyetujui penyiapan draft PR promosi ke main dengan kedua
  history dipertahankan. Tiga PR dibuat; isi file identik candidate dan enam CI
  promosi PASS. Ini bukan izin merge protected branch, tag, deploy atau sign-off.
- **O-07:** jawaban pengguna "untuk itu bisa di skip dulu" menunda pilot nyata
  serta penentuan peserta/PIC yang ditanyakan. Ini penundaan, bukan pilot PASS,
  feedback buatan, penerimaan CVE/billing/server, atau izin Phase2.

## 2. Hasil pengujian aktual

| Pemeriksaan | Hasil sesi ini |
|---|---|
| CI config | **PASS 7/7**, 63 tes kontrak |
| CI infra | **PASS 7/7**, 23 tes operasi +8 regresi Compose |
| GitHub candidateCI | **6/6 validate/security PASS**, padaSHAcandidate3repo; infra diperbaiki dan diujiulang |
| GitHub promosi main O-09 | **6/6 validate/security PASS** pada tiga SHA merge baru; semua draft PR tanpa konflik merge |
| GitHub docs | **PASS** pada 5bfd9d9, run39008234039; pembaruan docs berikutnya harus lulus CI pada SHA terbaru |
| CI E2E | **PASS 8/8**, 97 tes offline |
| Checkout E2E terisolasi | **97 unit PASS**, tanpa repo config/infra di sebelahnya |
| Full regression pertama | 85 unit +5 smoke +28 live **PASS**, 13 skenario native **PASS**; live517,07detik |
| Full regression akhir | **PASS exit0**:97unit/5smoke/30live/2outage +13native. Live760,34detik; outage191,27detik |
| Error/retry native | **13 PASS**:429/500/timeout408, retry2 berarti maksimum3attempt;400 tidak diulang |
| Guard mock pada gateway | **6 PASS**:parameter simulasi berbahaya ditolak400; credential sama kembali inference200 |
| Outage dependency terfokus | **2 PASS,179,39detik**:PG/Redis, negative access, recovery, spend retained |
| Rotasi virtual key | **2 PASS,24,80detik**:kedua alias, scope sama, old denied, new accepted, audit retained |
| Release/rollback config | **PASS**:timeout180→181→180,5smoke pada setiap apply, inode/byte/ID/image sama |
| Backup/restore | **PASS 83 tabel**, jumlah baris dan fingerprint sama; DB uji khusus dalam PG existing |
| Secret scanner | History/current tiga komponen dan docs **PASS** setelah source stabil; pembaruan docs dipindai lagi sebelum push |
| Audit dependency Python | Range dan lock tiga repo **PASS**, tidak ada vulnerability yang diketahui auditor pada snapshot ini |
| Lock dependency | Tiga lock memakai versi existing; checksum PyPI dan `--require-hashes --dry-run` **PASS** |
| Image scanner | **PASS baseline existing**:LiteLLM0Critical/0High,PG1Critical/28High,Redis0Critical/2High |
| Privasi penutup | **261 row**:messages/response kosong,0raw-key pattern;3666baris log runtime tanpa raw-key/toy-source/response marker |
| Cleanup penutup | **296key dan97team fixture blocked**, audit tetap ada; tiga container sehat,ID/image sama |
| Biaya fixture sesi |140row berbiaya positif,total native **US$0,0605837**; termasuk percobaan/pengulangan, bukan invoice provider |

Angka offline unik adalah **191** (63+31+97), bukan penjumlahan seluruh pengulangan.
Suite E2E final memiliki134kasus:97unit,5smoke,30live biasa dan2maintenance.
13skenario native adalah probe tambahan, bukan pytest/provider request.
Tes rotasi, agent dan guard terfokus juga berada dalam live suite; jangan dihitung dua kali.

## 3. Laporan per milestone P1

| Milestone | Penambahan/pembaruan dan hasil sederhana | Status/batas |
|---|---|---|
| P1-00: akses dan kepemilikan | Kedua model dapat dipakai via gateway. Empat repo GitHub dikonfirmasi private. Inventaris lisensi dengan sumber resmi ditambahkan | PARTIAL:billing/cap/lisensi perusahaan belum diterima; peserta/PIC ditundaO-07 |
| P1-01: repo dan workflow | Source disimpan pada commit/draft PR. O-09 menyatukan kedua history pada branch baru; isi file tetap sama. Enam CI promosi PASS | PARTIAL: tiga draft PR ke main dan docs #1 tersedia; review/merge belum dilakukan |
| P1-02: runtime dan database | PG dipadamkan singkat pada container yang sama; request yang tak dapat diverifikasi ditolak. Setelah pulih kedua alias dan pencatatan biaya bekerja | LOCAL proof tersedia; jaringan/TLS server belum |
| P1-03: secret/health/versi | Tidak mengganti image atau secret pengguna. Error tes disensor; health dicek setelah maintenance | LOCAL_VERIFIED; rotasi master/provider/salt produksi belum dilakukan |
| P1-04: fast | Inference `company-fast` diuji ulang dalam full suite | Mapping tetap `openai/gpt-5.6-terra` |
| P1-05: coding | Inference `company-coding` diuji ulang dalam full suite | Mapping tetap `openai/gpt-5.6-sol` |
| P1-06: kontrak model | Validator63kasus dan exposure tepat dua alias diperiksa ulang | LOCAL_VERIFIED; tidak membuka provider/alias baru |
| P1-07: identitas dan atribusi | User/team/multi-key, logspend dan cleanup fixture diuji ulang | Identitas disposable; audit tidak dihapus |
| P1-08: izin dan pencabutan | Fast-only menolak coding, keyblocked ditolak; diuji juga saat gangguan/pemulihan dan rotasi | LOCAL_VERIFIED; bukan jaminan provisioning bersamaan/SSO |
| P1-09: limit dan reset | RPM/TPM bersama, recovery, budget key/member/team dan reset anggota dijalankan ulang. Bug durasi anggota sudah diperbaiki pada sesi sebelumnya | Reset30d kalender UTC; scheduler sekitar10menit. Bukan hard prepaid cap atau migrasi anggota lama |
| P1-10: token/biaya | Usage kedua alias dibandingkan dengan respons provider, token, harga oracle dan counter native | Teks pendek/default tier; bukan invoice reconciliation |
| P1-11: onboarding | Script operator asli dan virtual key developer dipakai ulang oleh OpenCode | Native onboarding/fixture; distribusi credential kepada manusia belum diuji |
| P1-12: agent/tools/streaming | Kedua agent membaca/mengedit kode, menjalankan shell verifier dan memakai receipt hasil tool; SSE/API tools diperiksa ulang | Fixture coding kecil; bukan seluruh proyek/tool/adapter |
| P1-13: failure semantics | Tambah guardHTTP,13probe native dan tes outagePG/Redis dengan recovery otomatis | LOCAL_VERIFIED; error upstream disimulasikan tanpa providerIO; outage memakai layanan nyata existing |
| P1-14: reproducibility/CI | Tambah tiga lock berhash di validate workflows; perbaiki unit checkout tunggal dan perbedaan JSON Compose di CI | PARTIAL: O-08 diterapkan; CI candidate dan enam CI promosi PASS. Review, SHA docs terbaru dan server gate tetap diperiksa |
| P1-15: keamanan/privasi | Periksa log dan spend tanpa menyimpan isi sensitif; scan source/dependency/image. Dua false-positive scanner docs diverifikasi sebagai hashID blocked | PARTIAL:TLS/admin boundary, CVE dan keputusan data perusahaan belum |
| P1-16: operasional | Ulang restore83tabel, config-only release/rollback dan rotasi virtualkey kedua alias; perbarui incident/lifecycle runbook | PARTIAL:server/upgrade schema/image, backup luarhost dan rotasi secret produksi belum |
| P1-17: pilot manusia | Tidak membuat data peserta/feedback palsu | APPROVED_OVERRIDE sementaraO-07; pilot nyata tetap NOT_VERIFIED |
| P1-18: exit gate | Source hash, tiga draft PR promosi ke main, docs #1 dan enam CI promosi PASS dihimpun untuk reviewer | OPEN sampai review/keputusan release dan sign-off tersedia; belum merge/tag/deploy |

## 4. Cross-check H1–H10 dari awal

| Checkpoint lama | Pemeriksaan ulang sekarang |
|---|---|
| H1: image/Compose | Validator infra dan image scan berjalan pada versi existing; tidak pull/recreate. Manifest mencatat digest/ID |
| H2: secret | History/current scan, error/header repr tersensor, privacy audit dan backup privat diperiksa |
| H3: jaringan/mount | DB/Redis tidak dipublish; config read-only dan inode dipertahankan saat rollback. Gateway masih bind semua interface; TLS/server gate tetap terbuka |
| H4: health/recovery | Pengujian kini mencakup request auth/ACL/budget selama outage, bukan hanya HTTPhealth; recovery dan spend diperiksa |
| H5: backup | Dump/checksum/restore DB uji existing;83tabel sama. Dump dan `.env` tidak masuk laporan/Git |
| H6: validator | Config7/7,infra7/7,E2E8/8; kontrak alias/provider tetap dikunci |
| H7: merge/security | CI lama dikonfirmasiGitHub; candidate baru tiga komponen sudah dipublikasikan sebagai draftPR. Scan baseline bukan zero-CVE |
| H8: inference/policy | Kedua alias, streaming/tools, ACL, atribusi, RPM/TPM/budget diuji ulang |
| H9A–E: lifecycle/regression | Multi-key/offboard/audit retained, validator mandatory25fungsi dan97unit; partial setup/cleanup kini lebih aman |
| H10A–D: operasi/handover | Existing4000 dipertahankan. Release/rollback/drill key/restore diulang; runbook dan konteks aktif diperbarui |

Tidak semua acceptance server dapat diganti tes laptop. Detail gate tersebut tersedia
pada [checklist deploy](../operations/phase1-checklist.md).

## 5. Bug/gap yang ditemukan dan perbaikannya

| Temuan | Perbaikan dan pembuktian |
|---|---|
| Unit OpenCode membaca template repo config yang tidak tersedia pada checkout CI E2E tunggal | Unit transform memakai kontrak fixture; live tetap membaca template asli. Checkout terisolasi97unitPASS |
| Fixture lama baru membersihkan setelah setup lengkap | Registry cleanup didaftarkan segera setelah team dibuat; kegagalan setup tetap memblokir key/team. Teardown memeriksa hasil dan melaporkan kegagalan |
| Exception transport Requests dapat membawa URL/body bercredential; beberapa assertion lama mencetak responsebody | Sharedclient mengubahnya menjadi error tersensor, header/credential repr disembunyikan, assertionbody dihapus;5regresi privasiPASS |
| Tes rotasi awal menganggap counterspend selesai bersamaan dengan rowspend | QueryPG membuktikan data tetap ada; tes menunggu kedua flush asinkron dengan timeout45detik. Kedua aliasPASS tanpa mengubah native accounting |
| Tes fault awal mengira mock request langsung menghasilkan429 | Runtime sengaja menolak400. Pengaman dipertahankan; error/retry diuji lewatSDK/router/handler native pada proses terpisah dalam container existing |
| Harness native pertama belum mengirim metadata yang diwajibkan router | Bentuk metadata diperbaiki;13kasusPASS. Ini perbaikan harness, bukan patch LiteLLM |
| Gitleaks docs menandai dua token64hex pada evidence lama | Keduanya hashID native yang telahblocked. Allowlist dua hashID dan lima checksum source terverifikasi persis; canary lain tetap terdeteksi, tidak mengecualikan path/rule dan tidak mengedit evidence lama |
| Validatorinfra berbeda hasil lokal/CI karena JSONCompose menghilangkan false | Nilai false kini diwajibkan dariYAMLsumber, normalizedtrue/null tetapditolak;8regresi danCIvalidatePASS tanpa mengubah runtimeYAML |
| Python dependency hanya memakai range | Tambahkan pin versi existing dan seluruh checksum file rilisPyPI; CI memakai --require-hashes; dry-run/auditPASS |

Redis belum dihubungkan sebagai nativecache dalam runtime YAML. Saat Redis mati,
validrequest tetap200 dan deny tetap401/403/422; dependencyhealth tetap gagal.
Ini alasan mencatat M-02 secara jujur, bukan menghapus Redis atau menjanjikan
rate-limit terdistribusi. File policy, model, provider dan client template tetap sama.

## 6. Kode dan cara mengulang

Contoh inti perubahan pada satu HTTPclient:

```python
except requests.RequestException as error:
    raise GatewayTransportError(
        f"Gateway GET transport failed: {type(error).__name__}; details suppressed"
    ) from None
```

[Snapshot kode lengkap32file](PHASE1_FINAL_CODE_APPENDIX.md) mencakup sharedclient,
fixture, tes baru/unit, runner, validator, lock/workflow dan kode drill. Setiap file
memiliki hash; manifest dapat dibandingkan dengan source saat handover.

Dari rootworkspace gunakan venvexisting, lalu jalankan gatewaytests secara serial:

```bash
source .venv/bin/activate
cd llm-gateway-e2e
./scripts/ci/validate.sh
./scripts/run-all.sh --include-outage
```

`--include-outage` benar-benar menghentikan PostgreSQL/Redisexisting sebentar;
pastikan maintenance terkoordinasi. Runner biasa tidak menjalankan outage. Script
recovery memulai kembali container yang sama, fixture memblokir key/team dan tidak
menghapus audit. Jangan menjalankan kedua runner bersamaan atau mengaktifkan
`dangerously_allow_mock_testing_request_params` untuk membuat tes hijau.

## 7. Keputusan/gate yang belum ditutup

[Proposal konkret](PHASE1_RELEASE_DECISIONS.md) menjelaskan tindakan, dampak dan
rollback sebelum perubahan major. Target live CI disetujui O-08/ADR-015 dan diterapkan.
Penyiapan PR promosi main disetujui O-09 dan selesai dengan CI PASS; persetujuan
tersebut tidak mencakup merge protected main atau deployment server.

ImagebaselinePASS tetap menyisakanPG1Critical/28High danRedis2High. Critical berada
pada Go stdlib dalam binarygosu; package finding bukan bukti exploitability maupun
penerimaan risiko. Image/runtime tidak diubah diam-diam. TLS/admin isolation pada
server, backup terenkripsi luarhost, billing/cap dan penerimaan lisensi belum diuji
atau disetujui. Tiga branch promosi telah dipush untuk draft PR ke main; belum merge
protected main/develop, tag, deploy atau sign-off Phase 1.

**Penutupan Phase 1 tetap terbuka.** Full suite dan privacy/cleanup lokal sudah PASS;
review manusia dan keputusan release yang tersisa harus ditutup sesuai bukti.

PR aktif untuk review ke **main**:
[config #4](https://github.com/farhanpurdi/llm-gateway-config/pull/4),
[infra #7](https://github.com/farhanpurdi/llm-gateway-infra/pull/7),
[E2E #6](https://github.com/farhanpurdi/llm-gateway-e2e/pull/6) dan
[docs #1](https://github.com/farhanpurdi/llm-gateway-docs/pull/1).
Ketiganya memakai branch `release/phase1-main-review-20261017`; draft lama ke
develop (config #3/infra #6/E2E #5) tetap terbuka sebagai jejak candidate sebelumnya.
Main tiga komponen masih initial README. O-09 hanya mengizinkan penyiapan PR;
[keputusan promosi](PHASE1_MAIN_PROMOTION_PROPOSAL.md),
[bukti tree/parent](phase1-final-evidence/main-promotion-candidates.json) dan
[enam CI promosi PASS](phase1-final-evidence/main-promotion-ci-final.json)
menjadi acuan reviewer. Tidak ada force-push, merge protected branch, tag atau deploy.

Scan docs penutupan sempat menandai14nilai pada dua manifest source. Semuanya
cocok dengan7path file asli (5checksum unik), bukan credential. Nilai tersebut
diverifikasi ulang lalu ditambahkan persis keallowlist; canary64hex lain tetap
terdeteksi. Tidak mengecualikan path/rule/hash sembarang. [Proof](phase1-final-evidence/docs-source-hash-findings-verification.json)
dan [canary](phase1-final-evidence/docs-source-hash-canary.json).
