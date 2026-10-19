# Phase 1 — Gateway MVP, acceptance dan status nyata

**Status 18 Oktober 2026: Phase 1 DITUTUP DENGAN CATATAN, versi v0.0.1.**
Dasar penutupan: persetujuan pengguna **APPROVED_OVERRIDE O-10** setelah hasil
teknis lokal/CI lulus dan PR main direview/merged. Tujuh feedback serta daftar
lanjutan berada di [closeout v0.0.1](../reports/PHASE1_V0_0_1_CLOSEOUT.md).

Full run17Oktober PASS exit0:97unit/5smoke/30live/2outage dan13skenario native.
Config63 dan infra31 offline PASS; restore83tabel, rotasi key, config-only rollback,
agent/tools/streaming dan privasi/cleanup PASS. Ini bukti lokal, bukan tes VM GCP.
Main keempat repo identik candidate; PR config#4/infra#7/E2E#6/docs#1 merged.

CVE image diterima untuk fase ini. Pengguna memilih VM GCP/default/HTTP awal dan
keamanan bertahap. Snapshot/backup dan biaya menunggu diskusi manager. TTLRedis24jam
ditetapkan sebagai target yang belum diterapkan; akses Redis tambahan belum dibatasi
oleh kebijakan yang disepakati. Pilot nyata/peserta/PIC tetap ditundaO-07.
Phase2/3 NOT_STARTED. Tag Git v0.0.1 dan deployment VM belum dibuat/dibuktikan sesi ini.

Baca [master](../MASTER_CONTEXT.md) dahulu. File ini pemilik status acceptance P1.
Baris di bawah memisahkan hasil teknis dan pengecualian penutupan; tidak seluruhnya
diubah menjadi DONE_VERIFIED. Bagian sejarah H dan bukti10Oktober tetap dipertahankan.

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

Status kolom ini membedakan bukti teknis dan keputusan pengguna. O-10 menutup fase
dengan catatan tanpa mengubah pemeriksaan server/pilot/TTL yang belum ada menjadi PASS.

| ID | Acceptance awal / pemetaan H | Status dan bukti yang tersedia | Yang belum ditutup |
|---|---|---|---|
| P1-00 | Environment, owner, API/billing, model access; H1/H8 | PARTIAL teknis; penutupan melalui O-10: kedua alias teruji, repo private, inventaris lisensi tersedia | Biaya dibahas dengan manager; cap/alert/invoice/lisensi/ownership perusahaan belum disahkan. Peserta/PIC ditunda O-07 |
| P1-01 | Repo/workflow/review/main; H6/H7 | DONE_VERIFIED untuk publikasi/review/merge: empat PR main merged, source tree sama dengan candidate dan CI promosi/docs PASS | Nama v0.0.1 ditetapkan; tag/publikasi release belum dibuat. [Refs dan batas](../reports/PHASE1_V0_0_1_CLOSEOUT.md) |
| P1-02 | Compose/PG/network/persistence; H1/H3/H5 | LOCAL_VERIFIED pada Docker existing4000: persistence, restore83tabel, outage/recovery PASS | VM GCP/default network dipilih O-10; deploy/jaringan server belum diuji, hardening bertahap |
| P1-03 | Secrets, pinned release, health; H1/H2/H4 | LOCAL_VERIFIED: env600, no secrets scan, image spesifik, readiness+dependency diperbaiki | Belum pembuktian server/rotasi secret; lihat gate publikasi |
| P1-04 | Fast alias live; H8 | LOCAL_VERIFIED: inference `company-fast` PASS | Pertahankan exact mapping; hasil hanya credential/versi saat tes |
| P1-05 | Coding alias live; H8 | LOCAL_VERIFIED: inference `company-coding` PASS | Sama seperti P1-04 |
| P1-06 | Dua alias/catalog/ACL; H6/H8 | LOCAL_VERIFIED:63tes config dan exposure dua alias fullsuite PASS; source main/review/CI terverifikasi | Model dinamis DB/admin di luar bukti static; kontrak exact tetap dipertahankan |
| P1-07 | User/team/virtual key/attribution; H8/H9 | LOCAL_VERIFIED: user/team fixture, multi-key, attribution PASS | HR/SSO bukan scope Phase 1; pilot ownership tetap belum final |
| P1-08 | Fast-only deny coding, revocation; H8/H9 | LOCAL_VERIFIED: update team fast-only → coding403, restored200; blocked401/403 | Tidak menggeneralisasi ke seluruh jalur ACL/membership atau concurrent issuance |
| P1-09 | Pilot RPM/TPM/budget/duration; H8 | LOCAL_VERIFIED: policy pilot, shared RPM/TPM/recovery, key/member/team budget dan reset PASS; source merged | VM/peserta nyata belum; cap biaya dibahas manager O-10. Anggota lama belum dimigrasikan; reset kalender UTC sekitar10menit bukan hard prepaid cap |
| P1-10 | Cost/token per user/key/alias; H8/H9 | LOCAL_VERIFIED: token/spend kedua alias cocok respons provider dan harga oracle; source merged | Invoice/provider cap serta workload/tier lain belum direkonsiliasi; biaya dibahas manager O-10 |
| P1-11 | OpenCode/onboarding; H8/H10D | LOCAL_VERIFIED: script operator/pilot dan virtual key developer, agent OpenCode2.0.18 kedua alias PASS; source merged | Onboarding manusia/VM belum terbukti; pilot nyata ditunda O-07 |
| P1-12 | Streaming/tools/agent coding; H8 | LOCAL_VERIFIED: read/edit/shell/hasil tool dan verifikasi kode, SSE/API tools kedua alias PASS; source merged | Fixture coding kecil dan adapter template existing; bukan semua proyek/tool/Responses parity |
| P1-13 | Auth/ACL/budget/provider429/5xx; H8/H9 | LOCAL_VERIFIED17Oktober:13native simulated429/500/408+retry;6HTTPguard/recovery;2outagePG/Redis deny/recovery/spend PASS | Error upstream disimulasikan tanpa providerIO, bukan sengaja memicu429provider. Satu runtimeexisting/cache lokal; bukan concurrency/HA proof. [Bukti](../reports/phase1-final-evidence/README.md) |
| P1-14 | CI/scan/version lock; H6/H7/H10 | LOCAL_VERIFIED:3lock berhash, CI lokal/enam CI promosi/docs PASS; main source identik candidate; O-08 diterapkan | Penutupan v0.0.1 O-10; tag Git dan deployment server belum dipublikasikan/diverifikasi |
| P1-15 | Security/privacy/persistence; H2/H3/H4/H5/H7 | APPROVED_OVERRIDE O-10: audit/scan lokal PASS sesuai scope; CVE image diterima dan keamanan server bertahap | CVE tetap ada, dua kandidat DHI belum diuji. TLS/admin/network/retensi server belum terbukti; penutupan bukan zero-CVE atau approval perusahaan |
| P1-16 | Deploy/rollback/rotate/incident/backup; H5/H10 | LOCAL_VERIFIED operasi lokal; penutupan APPROVED_OVERRIDE O-10: config rollback, rotasi key dan restore83tabel PASS | Snapshot GCP opsi awal menunggu diskusi manager; belum ada jadwal/retensi/restore snapshot/deploy VM/rollback lintasimage yang terbukti |
| P1-17 | Pilot 2–5 developer & feedback | APPROVED_OVERRIDE sementara O-07,2026-10-17: user mengizinkan skip pilot nyata/penentuan peserta-PIC dahulu | Penggunaan/feedback nyata tetap NOT_VERIFIED; bukan bukti pilot selesai. Policy pilot tetap O-06; penundaan bukan approval billing/server/CVE |
| P1-18 | Exit gate/release/sign-off | APPROVED_OVERRIDE O-10: pengguna menutup Phase1 dengan catatan, versi v0.0.1,18Oktober2026 | Tag/publikasi release administratif dan deployment belum dilakukan; L-01…L-07 adalah tindak lanjut, Phase2/3 tetap NOT_STARTED |

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

## 5. Penutupan gap dan keputusan pemilik

Implementasi P1-06/P1-09…P1-13, regresi/CI, backup/restore, rotasi dan rollback
memiliki bukti lokal yang ditautkan pada laporan teknis. Pengguna mereview dan
menggabungkan PR source/dokumentasi ke main. Pada18Oktober2026 pengguna memilih
**v0.0.1 dan penutupan Phase1 dengan catatan (O-10)**.

Penerimaan ini mengubah status penutupan fase. Pengecualian CVE, keamanan bertahap,
snapshot/biaya, TTL Redis yang belum diterapkan dan pilot nyata ditunda tetap
terlihat pada [closeout](../reports/PHASE1_V0_0_1_CLOSEOUT.md). Jangan menghapusnya
atau membuka kembali fase hanya karena membaca status OPEN dalam snapshot lama.

## 6. Exit gate aktual

- [x] Fungsi gateway, dua alias, virtual key/ACL/limits/spend serta agent/tools/streaming teruji lokal.
- [x] Full suite134pytest+13native PASS exit0; config63/infra31 offline PASS.
- [x] Restore83tabel, rotasi key kedua alias, config-only rollback dan privasi/cleanup lokal PASS.
- [x] CI promosi/docs sesuai candidate PASS; empat PR main merged dan tree sama dengan source teruji.
- [x] Pengguna menerima CVE image untuk Phase1 dan mencatat dua kandidat evaluasi DHI.
- [x] Pengguna menerima penutupan dengan keamanan VM bertahap, backup/biaya dibahas manager dan target TTLRedis24jam.
- [x] Pilot nyata/peserta/PIC ditundaO-07; nama versi dan penutupan fase disetujui O-10.
- [ ] Tag Git/publikasi release v0.0.1; nama versi sudah disepakati, artefak Git belum dibuat.
- [ ] Deployment GCP, kontrol akses/TLS, snapshot aktif/uji restore dan TTL Redis terimplementasi: NOT_VERIFIED, tindak lanjut O-10.

Dua baris terakhir adalah catatan pelaksanaan lanjutan, bukan klaim menghalangi
penutupan yang telah disetujui. Phase2/3 tidak dimulai otomatis. Perubahan source,
image, cache atau jaringan dikerjakan sesuai task dan target yang diminta berikutnya.
