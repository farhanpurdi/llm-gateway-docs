# Phase 1 — Gateway MVP, acceptance dan status nyata

Baca [master](../MASTER_CONTEXT.md) dahulu. Pemilik status P1 ada di file ini.
Snapshot evaluasi: 2026-10-10. **Phase 1 gate masih terbuka; H10D verified lokal.**
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
| P1-00 | Environment, owner, API/billing, model access; H1/H8 | PARTIAL: kedua alias live PASS via gateway | Owner/repo private/licensing/billing corporate belum diverifikasi; direct API call belum ada bukti terpisah |
| P1-01 | Root context + 3 repo + workflow/protection; H6/H7 | PARTIAL: 3 repo ada, H7 gate dikonfirmasi user | Dokumentasi sudah dipindah ke repo docs existing; migrasi/source masih dirty, review/PR final belum ada |
| P1-02 | Compose/PG/network/persistence; H1/H3/H5 | PARTIAL: existing Docker+PG, restore 83 tabel PASS | Gateway bind semua interface berlawanan default local-private; bukti persistence bukan test enforcement saat outage |
| P1-03 | Secrets, pinned release, health; H1/H2/H4 | LOCAL_VERIFIED: env600, no secrets scan, image spesifik, readiness+dependency diperbaiki | Belum pembuktian server/rotasi secret; lihat gate publikasi |
| P1-04 | Fast alias live; H8 | LOCAL_VERIFIED: inference `company-fast` PASS | Pertahankan exact mapping; hasil hanya credential/versi saat tes |
| P1-05 | Coding alias live; H8 | LOCAL_VERIFIED: inference `company-coding` PASS | Sama seperti P1-04 |
| P1-06 | Tepat 2 alias, catalog/ACL, validation; H6/H8 | PARTIAL: config aktif sesuai, validator PASS | **F-01:** validator menerima salah upstream/alias tambahan; belum cross-check seluruh katalog/provider/runtime |
| P1-07 | User/team/virtual key/attribution; H8/H9 | LOCAL_VERIFIED: user/team fixture, multi-key, attribution PASS | HR/SSO bukan scope Phase 1; pilot ownership tetap belum final |
| P1-08 | Fast-only deny coding, revocation; H8/H9 | LOCAL_VERIFIED: update team fast-only → coding403, restored200; blocked401/403 | Tidak menggeneralisasi ke seluruh jalur ACL/membership atau concurrent issuance |
| P1-09 | Pilot RPM/TPM/budget/duration; H8 | PARTIAL: team RPM dan tiny key budget enforced | TPM, member/team budget interaction, nilai pilot disetujui dan provider cap/alert belum dibuktikan |
| P1-10 | Cost/token per user/key/alias; H8/H9 | PARTIAL: spend positif dan history key/user/team retained | Pricing/token/per-alias reconciliation dengan provider billing belum diuji |
| P1-11 | OpenCode kedua alias + onboarding; H8/H10D | PARTIAL: template kedua alias, fast smoke PASS, provisioning script tersedia | Bukti OpenCode coding alias dengan credential developer dan alur onboarding end-to-end lengkap |
| P1-12 | Streaming/tools/agent coding; H8 | PARTIAL: API streaming fast; API forced tool call kedua alias PASS | Agent benar-benar menjalankan tool + menerima hasilnya + workflow coding kedua alias belum ada bukti rinci |
| P1-13 | Auth/ACL/budget/provider429/5xx; H8/H9 | PARTIAL: invalid/blocked/denied/key-budget/RPM PASS | Provider429/5xx/timeout, retry/error semantics dan auth/budget during DB outage belum tercakup |
| P1-14 | CI/scan/live environment/version lock; H6/H7/H10 | PARTIAL + override lokal: validator/scan/manifest lokal PASS | Candidate CI remote, version/dependency lock reproducible; workflow live masih menyebut staging; tidak boleh membuat staging untuk menutupnya |
| P1-15 | Security minimum, logs, persistence; H2/H3/H4/H5/H7 | PARTIAL: secret/private DB/backup/restore PASS | TLS/shared access, admin isolation, audit minimisasi isi log/spend, security findings review |
| P1-16 | Deploy/rollback/rotate/incident/backup; H5/H10 | PARTIAL: runbook + config-only release/rollback PASS | Re-deploy server dari compatible refs, image/schema compatibility, prosedur+drill rotasi key/secret sesuai scope |
| P1-17 | Pilot 2–5 developer & feedback | NOT_VERIFIED: belum ada bukti pilot pada arsip | Owner, peserta, budget, usage/cost feedback, issue log; fixture bukan pilot |
| P1-18 | Exit gate, release tag/sign-off | OPEN | Semua acceptance/pengecualian disetujui, source/CI final, tag/refs dan sign-off |

## 3. H1–H10D: pertahankan hasil, jangan perluas klaim

| Checkpoint | Bukti lokal yang tetap sah | Batas |
|---|---|---|
| H1 | Image LiteLLM1.104.0, PG16.15, Redis7.4.11-alpine | Tag spesifik bukan digest-only deployment; Python masih version range |
| H2 | Env600, secret scan PASS, backup env privat | Bukan audit bahwa semua isi runtime log bebas prompt/PII |
| H3 | DB/Redis tidak publish port; mount read-only | Gateway publish `0.0.0.0`/IPv6:4000 |
| H4 | Stop/start dependency terdeteksi, recovery PASS | Bukan bukti request inferensi/auth/budget fail-closed selama outage |
| H5 | Dump/checksum/restore, 83 tabel identik | DB test dalam PG existing; belum boot aplikasi terhadap DB restore |
| H6 | Infra7/7, config6/6, E2E8/8 | Validator mempunyai gap kontrak F-01 |
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

HEAD lokal yang diperiksa pada konsolidasi, **bukan commit berisi semua perubahan**:

- infra: `05f77497f18c2c4edf2ab1cbf938d10ca0f5b484` + dirty/untracked;
- config: `b2cf9b04d83cca45db4f350ac5c4be9fbf8ea030` + dirty;
- e2e: `6151e07109c9832ce776a078921574d695f45134` + dirty/untracked.

Manifest ignored `releases/phase1-h10d-local-20261010-final` adalah snapshot lokal, bukan
tag atau lock versi rilis yang sudah disetujui. Context/reports sekarang di repo `llm-gateway-docs`, belum commit/push setelah migrasi.

## 5. Penutupan gap: urutan usulan, belum perintah eksekusi

1. **P1-06/F-01:** kunci exact alias/provider/upstream, sinkronisasi validator katalog/runtime,
   negative test alias/model/provider tak disetujui. Pertahankan filename identity dan satu client.
2. **P1-09/10/12/13:** lengkapi acceptance limits, biaya/token, OpenCode agent, provider errors
   serta perilaku request ketika dependency mati; jangan menganggap test health sebagai pengganti.
3. **P1-14/15/16:** sepakati keputusan major tersisa (M-01/M-02/M-04/M-05; penempatan docs M-03 sudah dipilih), kemudian
   kelola release refs/dependency lock/CI target, security/privacy, rotasi dan runbook server.
4. **P1-17:** pilot kecil dengan owner/budget yang disetujui dan catatan feedback.
5. **P1-18:** sign-off, release tag/refs, bukti acceptance atau pengecualian eksplisit.

Urutan dapat disesuaikan user; jangan mengubah OPEN menjadi waived tanpa keputusan.
Tidak perlu mengulang seluruh H1–H10 karena ada gap baru; test ulang yang relevan setelah perubahan.

## 6. Exit gate aktual

- [x] Kedua alias live via virtual key dan gateway terbukti pada credential saat tes.
- [x] PostgreSQL persisten; identitas pengguna, izin akses, pencabutan credential, budget per key, RPM team dan pencatatan spend dasar telah diuji.
- [ ] Exact catalog/provider contract dijaga validator dan negative tests.
- [ ] Acceptance OpenCode/agent, token/cost dan limit semantics lengkap atau keterbatasan disetujui.
- [ ] Provider failure dan data-handling/privacy/security baseline untuk shared service diterima.
- [ ] Target verifikasi release disetujui tanpa melanggar larangan staging sekarang; CI final PASS.
- [ ] Deployable refs/dependency versions, review Git, compatible rollback/rotasi dan backup luar host.
- [ ] Pilot2–5 dan feedback, owner/budget, release tag dan sign-off.

**Berhenti sebelum perubahan major.** Jangan membuat environment baru, mengubah routing,
mengganti image, menghapus Redis, membentuk parent Git/submodules, atau mengurangi gate
hanya untuk mengejar checklist hijau.
