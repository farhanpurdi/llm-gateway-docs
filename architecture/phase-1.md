# Phase 1 — Gateway MVP, acceptance dan status nyata

**Checkpoint aktif17Oktober2026: P1-FINAL sedang berjalan.** User meminta sampai
akhir dan full test. Native error/retry13kasus, guardHTTP6kasus, outagePG/Redis2kasus,
rotasi virtualkey keduaalias dan config-only rollback sudahPASS. CI lokal terbaru:
config63tes, infra31tes(23operasi+8Compose), E2E97unitPASS. Fullrun exit0:
97unit/5smoke/30live/2outage+13nativePASS. O-08 hostedoffline + live manual4000
diterapkan; workflowstaging dihapus dan3draftPRcandidate kedevelop tersedia;
[laporan aktif](../reports/PHASE1_FINAL_CROSSCHECK_REPORT.md) memiliki status terkini.
Pilot nyata/peserta/PIC ditundaO-07; gate release/server tetap terbuka.

Baca [master](../MASTER_CONTEXT.md) dahulu. Pemilik status P1 ada di file ini.
Snapshot evaluasi: 2026-10-10. **Phase 1 gate masih terbuka; H10D verified lokal.**
Pemeriksaan source/Git dan [rencana penutupan](phase-1-completion-plan.md) diperbarui
2026-10-12. Setelah sesi rencana, P1-06/F-01/F-02 diimplementasikan dan diuji static/offline;
tidak ada tes live baru. Lihat [laporan P1-06](../reports/P1_06_MODEL_CONTRACT_REPORT.md).
Pada 2026-10-13, user mengoreksi policy pengerjaan/tes final pilot menjadi `pilot.yaml`;
keputusan [ADR-016/O-06](../adr/016-pilot-limits.md) menjadi acuan P1-09/P1-10.
Implementasi/test paket ini kini LOCAL_VERIFIED: 147 offline, 4 smoke dan 11 live PASS;
lihat [laporan terbaru](../reports/P1_09_P1_10_LIMITS_COST_REPORT.md). Gate release tetap terbuka.
Pada 2026-10-17, P1-11/P1-12 juga LOCAL_VERIFIED: onboarding operator asli, kedua
agent OpenCode, streaming/tools PASS; 79 unit, 5 smoke dan 6 live terfokus.
[Laporan/kode](../reports/P1_11_P1_12_OPENCODE_REPORT.md); bukan seluruh suite live atau pilot nyata.
Dasar: [rancangan §8](../archive/PROJECT_MASTER_CONTEXT.md#8-roadmap-phase-1--urutan-pengerjaan-yang-harus-diikuti),
source tiga repo, dan bukti tersimpan. Tidak menjalankan ulang runtime pada sesi evaluasi.

## 1. Kontrak dan layout aktual

OpenAI saja; `company-fast` → `openai/gpt-5.6-terra`, `company-coding` → `openai/gpt-5.6-sol`.
Virtual key per user/workload, metadata user/team, ACL, budget/spend via native LiteLLM.
Tidak ada custom UI/control plane/SSO/multi-provider fallback pada scope fase ini.

| Komponen | Lokasi source aktif |
|---|---|
| Runtime container | [infra/docker-compose.yml](../../llm-gateway-infra/docker-compose.yml) |
| Config yang di-mount | [config/config/litellm_config.yaml](../../llm-gateway-config/config/litellm_config.yaml) |
| Katalog deskriptif | `llm-gateway-config/models/*.yaml`, `providers/openai.yaml` |
| Policy input provisioning | `llm-gateway-config/policies/teams/*.yaml` → script infra → LiteLLM API |
| OpenCode template aktual | [opencode.jsonc](../../llm-gateway-config/clients/opencode/opencode.jsonc) |
| HTTP client E2E | [tests/client.py](../../llm-gateway-e2e/tests/client.py) |
| Provisioning/cleanup tes | [tests/conftest.py](../../llm-gateway-e2e/tests/conftest.py) |
| Runbook | [operasional](../operations/README.md); source script tetap di repo infra |

Nama file berbeda dari contoh awal bukan alasan melakukan rename massal. Katalog YAML
bukan deployment source otomatis; config runtime harus tetap konsisten dengannya.
Model ID diturunkan dari filename `models/`, tidak menambah `logical_name` di sana.

## 2. Peta P1-00…P1-18 ke pekerjaan yang ada

Status kolom ini **teknis lokal**, bukan `DONE_VERIFIED` release. Task dengan sebagian
acceptance belum terbukti tetap PARTIAL meskipun milestone H terkait dinyatakan PASS.

| ID | Acceptance awal / pemetaan H | Status dan bukti yang tersedia | Yang belum ditutup |
|---|---|---|---|
| P1-00 | Environment, owner, API/billing, model access; H1/H8 | PARTIAL: kedua alias live PASS via gateway; empat repoGitHub private terverifikasi17Oktober; inventaris lisensi tersedia | Billing/cap dan penerimaan lisensi belum; peserta/PIC ditundaO-07. Direct API call belum ada bukti terpisah |
| P1-01 | Root context + 3 repo + workflow/protection; H6/H7 | PARTIAL:4repo private; H7/H8merged kedevelop terverifikasi;3candidatecommit/push/draftPR, docs candidate disiapkan | Review/CI candidatefinal dan promosi mainunrelated belumselesai; tidak forcepush |
| P1-02 | Compose/PG/network/persistence; H1/H3/H5 | PARTIAL: existing Docker+PG, restore 83 tabel PASS | Gateway bind semua interface berlawanan default local-private; bukti persistence bukan test enforcement saat outage |
| P1-03 | Secrets, pinned release, health; H1/H2/H4 | LOCAL_VERIFIED: env600, no secrets scan, image spesifik, readiness+dependency diperbaiki | Belum pembuktian server/rotasi secret; lihat gate publikasi |
| P1-04 | Fast alias live; H8 | LOCAL_VERIFIED: inference `company-fast` PASS | Pertahankan exact mapping; hasil hanya credential/versi saat tes |
| P1-05 | Coding alias live; H8 | LOCAL_VERIFIED: inference `company-coding` PASS | Sama seperti P1-04 |
| P1-06 | Tepat 2 alias, catalog/ACL, validation; H6/H8 | LOCAL_VERIFIED (static/offline 2026-10-12): exact alias/provider/upstream/env, katalog konsisten; 63 tes config, 22 infra, 29 unit E2E PASS | Commit/review/CI remote dan eksekusi live assertion exposure terbaru belum; bukan release DONE. Model dinamis DB/API admin di luar bukti static |
| P1-07 | User/team/virtual key/attribution; H8/H9 | LOCAL_VERIFIED: user/team fixture, multi-key, attribution PASS | HR/SSO bukan scope Phase 1; pilot ownership tetap belum final |
| P1-08 | Fast-only deny coding, revocation; H8/H9 | LOCAL_VERIFIED: update team fast-only → coding403, restored200; blocked401/403 | Tidak menggeneralisasi ke seluruh jalur ACL/membership atau concurrent issuance |
| P1-09 | Pilot RPM/TPM/budget/duration; H8 | LOCAL_VERIFIED 2026-10-13: policy pilot persisten, RPM/TPM shared+recovery, key/member/team budgets; bug reset anggota diperbaiki, reset otomatis dan cumulative spend retained PASS | Release commit/review/CI candidate, peserta/penerapan pilot nyata dan cap/alert provider belum; anggota lama tidak dimigrasikan. Reset kalender UTC dan scheduler sekitar10menit; bukan hard prepaid cap/concurrency proof |
| P1-10 | Cost/token per user/key/alias; H8/H9 | LOCAL_VERIFIED 2026-10-13: kedua alias, token/spend request dan counter key/member/user/team cocok dengan respons provider+harga standar resmi | Invoice/provider billing, cache/long context/tier lain dan workload streaming/tools belum direkonsiliasi. Harga snapshot13Oktober; gate publikasi/candidate masih berlaku |
| P1-11 | OpenCode kedua alias + onboarding; H8/H10D | LOCAL_VERIFIED 2026-10-17: script onboarding operator asli/policy pilot, internal_user + key developer, exact dua model; kedua alias dipakai agent OpenCode2.0.18 | Commit/review/CI candidate, distribusi credential/onboarding manusia dan pilot nyata belum; template/config pribadi tidak diubah |
| P1-12 | Streaming/tools/agent coding; H8 | LOCAL_VERIFIED 2026-10-17: kedua alias read→edit→shell verifier→receipt hasil tool, kode diuji independen; SSE sampai DONE dan structured tool API PASS | Fixture Python kecil/default adapter Chat Completions; proyek besar/semua tool/Responses parity belum. Security permission fixture bukan kebijakan client perusahaan; release gate tetap terbuka |
| P1-13 | Auth/ACL/budget/provider429/5xx; H8/H9 | LOCAL_VERIFIED17Oktober:13native simulated429/500/408+retry;6HTTPguard/recovery;2outagePG/Redis deny/recovery/spend PASS | Error upstream disimulasikan tanpa providerIO, bukan sengaja memicu429provider. Satu runtimeexisting/cache lokal; bukan concurrency/HA proof. [Bukti](../reports/phase1-final-evidence/README.md) |
| P1-14 | CI/scan/live environment/version lock; H6/H7/H10 | PARTIAL:3lock berhash/dry-run/audit dan CI lokalPASS; O-08 hostedoffline + live manualexisting4000 diterapkan, workflowstaging dihapus | CandidateCI/review dituntaskan; [gate lokal](../operations/local-release-gate.md) mengikatSHA/hash/output. Main/servergate terpisah |
| P1-15 | Security minimum, logs, persistence; H2/H3/H4/H5/H7 | PARTIAL: secret scan/audit, backuprestore83tabel dan minimisasi data/log initial PASS17Oktober | TLS/shared access/admin isolation dan penerimaan temuanPG1C/28H/Redis2H belum; samplingprivasi bukan jaminan seluruh trafik |
| P1-16 | Deploy/rollback/rotate/incident/backup; H5/H10 | PARTIAL:17Oktober config180→181→180+5smoke tiapapply, sameinode/byte/ID/image PASS; rotasi key keduaalias tanpa hapus audit dan restore83tabel PASS | Server compatible refs, lintasimage/schema, master/provider/salt rotation dan backup luarhost belum; [runbook](../operations/deployment.md) |
| P1-17 | Pilot 2–5 developer & feedback | APPROVED_OVERRIDE sementara O-07,2026-10-17: user mengizinkan skip pilot nyata/penentuan peserta-PIC dahulu | Penggunaan/feedback nyata tetap NOT_VERIFIED; bukan bukti pilot selesai. Policy pilot tetap O-06; penundaan bukan approval billing/server/CVE |
| P1-18 | Exit gate, release tag/sign-off | OPEN | Semua acceptance/pengecualian disetujui, source/CI final, tag/refs dan sign-off |

## 3. H1–H10D: pertahankan hasil, jangan perluas klaim

| Checkpoint | Bukti lokal yang tetap sah | Batas |
|---|---|---|
| H1 | Image LiteLLM1.104.0, PG16.15, Redis7.4.11-alpine | Tag spesifik bukan digest-only deployment; Python masih version range |
| H2 | Env600, secret scan PASS, backup env privat | Bukan audit bahwa semua isi runtime log bebas prompt/PII |
| H3 | DB/Redis tidak publish port; mount read-only | Gateway publish `0.0.0.0`/IPv6:4000 |
| H4 | Stop/start dependency terdeteksi, recovery PASS | Bukan bukti request inferensi/auth/budget fail-closed selama outage |
| H5 | Dump/checksum/restore, 83 tabel identik | DB test dalam PG existing; belum boot aplikasi terhadap DB restore |
| H6 | Snapshot H: infra7/7, config6/6, E2E8/8 | Gap F-01/F-02 dari snapshot ini diperbaiki offline pada 12 Oktober; config sekarang 7 tahap |
| H7 | History/working-tree scan, Python audit, image baseline PASS | PG1C/28H, Redis0C/2H tersisa; H7 GitHub menurut konfirmasi user |
| H8 | Inference/stream/ACL/RPM/key budget; tool calling kedua alias | Coverage budget/TPM/cost/provider-error belum menyeluruh |
| H9A–D | Dua key user, pagination, block, deny, retention | Snapshot; freeze provisioning manual; history fixture kecil satu halaman |
| H9E | 22 unit; required lifecycle, runner unit→smoke→live | Unit simulasi bukan jaminan seluruh concurrency di production |
| H10A | Existing4000, Compose staging dihapus sesuai user | Pengecualian target lokal, bukan waiver semua release gate |
| H10B/C | Config180→181→180, smoke tiap tahap, ID sama | Tidak deploy image baru, tidak migrasi/downgrade schema/server |
| H10D | Runbook/checklist tersedia | Bukan bukti pilot/sign-off/server siap |

## 4. Peta bukti dan provenance

Semua bukti di bawah dari eksekusi **2026-10-10 sebelumnya**, dibaca saat konsolidasi.
Jangan mengubah timestamp atau mengklaim tes baru hanya karena dokumen diperbarui.

| Bukti | Isi |
|---|---|
| [full-regression-final](../reports/phase1-evidence/full-regression-final.txt) | 22 unit + 3 smoke + 12 live; 19 fungsi pytest total setelah parameterisasi |
| [infra-validation](../reports/phase1-evidence/infra-validation.txt) | 7 tahap dan 12 tes operasi |
| [config-validation](../reports/phase1-evidence/config-validation.txt) / [e2e-validation](../reports/phase1-evidence/e2e-validation.txt) | 6/6 dan 8/8 |
| [opencode](../reports/phase1-evidence/opencode.txt) | OpenCode company-fast basic response; detail agent tools tidak ada |
| [backup-restore](../reports/phase1-evidence/backup-restore.txt) | 83 tabel identik |
| [release-rollback](../reports/phase1-evidence/release-rollback.txt) | Config release+rollback dan smoke |
| [failure-recovery-final](../reports/phase1-evidence/failure-recovery-final.txt) | Dependency outage/recovery; label HTTP di log berasal dari script yang kini menggabungkan HTTP+dependency |
| [runtime-audit](../reports/phase1-evidence/runtime-audit.txt) | ID/image/port/env parity tanpa nilai secret |
| [containers-security](../reports/phase1-evidence/containers-security.txt) / [CVE](../reports/phase1-evidence/vulnerability-details.json) | Hasil/baseline per-image; bukan scan baru pada sesi review |
| `reports/phase1-evidence/secrets-{infra,config,e2e}.txt`, `dependencies-*.txt` | Security scan ketiga repo |
| [validator-contract-check](../reports/context-review/validator-contract-check.json) | **Bukti baru review:** salinan sementara wrong upstream/extra alias diterima validator; runtime tidak disentuh |
| [P1-06 report](../reports/P1_06_MODEL_CONTRACT_REPORT.md) / [evidence](../reports/p1-06-evidence/README.md) | **Bukti 2026-10-12:** dua CLI menolak wrong upstream/extra alias/catalog drift, guard release dan assertion exposure diperketat; 114 tes offline PASS |

HEAD lokal yang diperiksa pada konsolidasi, **bukan commit berisi semua perubahan**:

- infra: `05f77497f18c2c4edf2ab1cbf938d10ca0f5b484` + dirty/untracked;
- config: `b2cf9b04d83cca45db4f350ac5c4be9fbf8ea030` + dirty;
- e2e: `6151e07109c9832ce776a078921574d695f45134` + dirty/untracked.

Manifest ignored `releases/phase1-h10d-local-20261010-final` adalah snapshot lokal, bukan
tag atau lock versi rilis yang sudah disetujui. Context/reports berada di repo
`llm-gateway-docs`, migrasi tercatat pada commit lokal `1d07d02` (pemeriksaan 2026-10-12).
Push/review remote belum diperiksa. Source komponen masih dirty/untracked;
pembaruan rencana sesi ini belum commit.

## 5. Penutupan gap: urutan dan progres

User meminta melanjutkan pekerjaan dan melihat plan pada 2026-10-12. Urutan rinci,
bukti selesai serta keputusan prasyarat ada pada [rencana penutupan](phase-1-completion-plan.md).
Paket pertama P1-06/F-01/F-02 telah diimplementasikan dan LOCAL_VERIFIED static/offline;
gate commit/review/live tetap tersisa. Keputusan major diperlukan sebelum tindakan terkait.

1. **P1-06/F-01/F-02 — LOCAL_VERIFIED:** exact alias/provider/upstream, konsistensi katalog/runtime
   dan tes negatif tersedia; filename identity dan satu client dipertahankan. Selesaikan gate publikasi/live pada candidate final.
2. **P1-09/P1-10 — LOCAL_VERIFIED:** limits/persistence/reset dan token/biaya standar
   kedua alias PASS; pertahankan batas bukti/owner cap dan gate candidate.
   **P1-11/P1-12 — LOCAL_VERIFIED:** onboarding dan agent kedua alias memakai hasil
   tool, serta SSE/API tools PASS pada17Oktober. **P1-13 LOCAL_VERIFIED:** native
   simulation/error/retry dan requestauth/budget/outagerecovery PASS padaexisting.
3. **P1-14/15/16:** sepakati keputusan major tersisa (M-01/M-02/M-04/M-05; penempatan docs M-03 sudah dipilih), kemudian
   kelola release refs/dependency lock/CI target, security/privacy, rotasi dan runbook server.
4. **P1-17:** pilot nyata/peserta/PIC ditunda dahulu atas instruksiuserO-07; bukan pilotPASS.
5. **P1-18:** sign-off, release tag/refs, bukti acceptance atau pengecualian eksplisit.

Urutan dapat disesuaikan user; jangan mengubah OPEN menjadi waived tanpa keputusan.
Tidak perlu mengulang seluruh H1–H10 karena ada gap baru; test ulang yang relevan setelah perubahan.

## 6. Exit gate aktual

- [x] Kedua alias live via virtual key dan gateway terbukti pada credential saat tes.
- [x] PostgreSQL persisten; identitas pengguna, izin akses, pencabutan credential, budget per key, RPM team dan pencatatan spend dasar telah diuji.
- [x] Exact catalog/provider contract dijaga validator dan negative tests (static/offline 12 Oktober; gate publikasi/live tetap berlaku).
- [x] P1-09/P1-10 limits/reset dan token/cost standar kedua alias LOCAL_VERIFIED pada13Oktober; batas scope/invoice/candidate tetap disebut.
- [x] Acceptance lokal P1-11/P1-12: onboarding/agent kedua alias dan penggunaan hasil tool, SSE/API tools PASS17Oktober; batas fixture/candidate tetap berlaku.
- [ ] Provider failure dan data-handling/privacy/security baseline untuk shared service diterima.
- [ ] Target verifikasi release disetujui tanpa melanggar larangan staging sekarang; CI final PASS.
- [ ] Deployable refs/dependency versions, review Git, compatible rollback/rotasi dan backup luar host.
- [x] Pilot2–5/peserta/PIC ditunda sementaraO-07; feedback nyata tetapNOT_VERIFIED.
- [ ] Keputusan biaya/keamanan yang tersisa, release tag/refs dan sign-off.

**Berhenti sebelum perubahan major.** Jangan membuat environment baru, mengubah routing,
mengganti image, menghapus Redis, membentuk parent Git/submodules, atau mengurangi gate
hanya untuk mengejar checklist hijau.
