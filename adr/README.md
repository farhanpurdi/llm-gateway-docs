# Keputusan, evaluasi kesesuaian, dan perubahan yang tertunda

Baca [master](../MASTER_CONTEXT.md). Evaluasi 2026-10-10 memakai baseline
awal → handoff → source/bukti. Ini dokumen keputusan dan temuan; **bukan izin eksekusi**.

## 1. Kesimpulan evaluasi

Arsitektur utama **sesuai rancangan**: LiteLLM Data Plane, OpenAI saja, mapping kedua
alias tetap, virtual key, PostgreSQL, tiga repo, OpenCode, tanpa custom Control Plane/UI.
Tidak ditemukan perubahan provider atau pembangunan Phase 2/3 yang mendahului roadmap.
Backup, security scan, lifecycle dan runbook lebih rinci daripada MVP minimal, tetapi
masih relevan dengan security minimum dan acceptance P1; bukan alasan membuang pekerjaan.

Perbedaan terpenting adalah **cakupan bukti dan definisi selesai**. Handoff menutup H1–H10
lokal, sedangkan baseline menuntut P1-00…18, commit/review, pilot, sign-off dan tag release.
Konsolidasi ini mengoreksi pembacaan status, **tidak mencabut hasil tes yang memang lulus**.
Phase 1 penuh belum selesai menurut exit gate awal.

## 2. ADR awal dipertahankan

| ID | Keputusan awal / status asli | Posisi setelah evaluasi |
|---|---|---|
| ADR-001 | LiteLLM Data Plane / CONFIRMED | Sesuai implementasi |
| ADR-002 | OpenAI-only Phase1 / CONFIRMED | Runtime sesuai; perlindungan validator belum kuat (F-01) |
| ADR-003 | fast→Terra / CONFIRMED | Runtime sesuai; jangan substitusi diam-diam |
| ADR-004 | coding→Sol / CONFIRMED | Runtime sesuai; jangan substitusi diam-diam |
| ADR-005 | OpenCode client awal / CONFIRMED | Sesuai; coverage workflow penuh masih sebagian |
| ADR-006 | Virtual key user/team, provider key server / BASELINE | Dipakai dan dites; bukan izin master key di client |
| ADR-007 | PostgreSQL sejak Phase1 / BASELINE | Terpasang, restore teruji |
| ADR-008 | Redis opsional saat bootstrap / BASELINE | Redis kini mandatory operasional; alasan aktivasi/kebutuhan perlu dicatat (M-02) |
| ADR-009 | Alias sebagai kontrak / BASELINE | Sesuai runtime; validator masih bisa menerima pelanggaran |
| ADR-010 | Control Plane terpisah mulai Phase2 / BASELINE | Belum dibangun; tetap tertunda |
| ADR-011 | Tiga repo; root/submodules bila root Git / BASELINE | Tiga repo sesuai, root bukan Git; docs dipusatkan di repo docs existing (O-04/M-03); belum commit/push migrasi |
| ADR-012 | Git desired config, satu writer policy / BASELINE | Manual Git→API pada P1; konsistensi katalog belum dijamin; reconciler tetap Phase2 |
| ADR-013 | Repo/image/dependency pinned saat deploy / BASELINE | Tag image spesifik + manifest lokal ada; Python range, dirty source, belum release lock/tag |
| ADR-014 | IdP SSO / OPEN | Tetap OPEN, tidak menebak vendor |
| ADR-015 | Hosting final / OPEN | Local existing4000 dipilih; hosting/server final tetap OPEN |
| ADR-016 | Budget/RPM/TPM/jumlah user / OPEN | Angka policy ada sebagai config existing, **bukan persetujuan budget corporate/pilot** |
| ADR-017 | Lisensi/fitur enterprise / OPEN | Belum ditemukan bukti matriks lisensi yang menutup keputusan |

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

Urutan roadmap masih Phase1→Phase2→Phase3. Pengecualian staging mengikuti O-01;
bila target acceptance server/CI perlu berubah, desain alternatif harus dibahas dahulu.

## 4. Register temuan yang dapat ditindaklanjuti

| ID | Kategori / perbandingan baseline dengan fakta | Dampak dan tindak lanjut |
|---|---|---|
| F-01 | **Gap enforcement kontrak:** validator runtime hanya memastikan alias wajib ada, string model terisi, dan env key benar | Salinan wrong upstream dan extra alias tetap exit0. Kunci exact model/provider/alias dan uji negatif. Config aktif saat ini benar; bukan temuan routing provider lain aktif |
| F-02 | **Gap konsistensi config:** katalog/provider YAML terpisah dari runtime; validator katalog terutama memeriksa filename | Bandingkan routing katalog/provider/runtime atau tentukan generated artifact; jangan menganggap edit katalog mengubah gateway |
| F-03 | **Drift operasional:** Redis opsional desain awal, tetapi Compose depends_on dan readiness/release kini membutuhkan Redis | Kebutuhan/rationale belum terbukti; jangan menghapus container. M-02 diperlukan sebelum perubahan dependensi |
| F-04 | **Drift exposure:** baseline local-private, aktual publish4000 ke semua interface | Kebutuhan akses LAN belum dikonfirmasi; host policy tidak diasumsikan. TLS/admin isolation target belum diverifikasi. Bahas bersama M-01 |
| F-05 | **Gap coverage limits/cost:** team RPM dan key budget teruji, spend>0 dan retensi teruji | Bukan bukti TPM/member-team budget interaction, akurasi harga/token/provider reconciliation. Lengkapi P1-09/10 |
| F-06 | **Gap OpenCode acceptance:** fast basic response terbukti, API tools kedua alias terbukti | Dokumen compatibility lama menyebut tool calling, tetapi bukti langkah agent coding lengkap belum ada di evidence sekarang; bukan kesimpulan fitur gagal |
| F-07 | **Gap failure semantics:** dependency detector pulih, unit offboarding mensimulasikan HTTP500 | Ini bukan test upstream provider429/5xx/timeout, bukan auth/budget fail-closed saat DB down. Lengkapi P1-13 |
| F-08 | **Release scope lebih sempit:** rollback config in-place dan same IDs/image teruji | Baseline memerlukan compatible image+config refs. Dirty manifest, Python ranges, belum tag/review/server deploy. Jangan mempromosikan klaim config-only menjadi recovery lintas versi |
| F-09 | **Workflow tertinggal:** `e2e/.github/workflows/live.yml` masih memakai environment `staging` dan `STAGING_*` | File masih ada; bukan bukti staging hidup. Hosted runner tidak mengakses localhost laptop. Target runner/secret/release harus diputuskan, jangan sekadar mengganti nama |
| F-10 | **Bukti security terbatas:** secret scan/verbosefalse/jsonlogs true bukan content privacy audit | Belum validasi raw prompt/response/PII pada logs/spend storage, retention dan akses admin. Existing baseline menerima CVE; risk acceptance production tetap diperlukan |
| F-11 | **Dokumen saling menimpa:** master awal PLANNING; handoff H10D COMPLETE; struktur staging/count lama masih terselip | Diselesaikan untuk navigasi dengan master aktif + status per-P1 + banner arsip. Jangan menjalankan ulang bootstrap dari snapshot awal |
| F-12 | **Governance/pilot belum tertutup:** migrasi docs kini di repo docs, commit/review belum; owner/budget/license dan pilot/tag belum ada bukti | Pertahankan OPEN/PARTIAL; tidak menandai Phase1 selesai atau lompat Phase2 |

### Bukti F-01 yang baru dihasilkan

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
Release validator memeriksa himpunan alias tetapi belum exact upstream mapping; satu
validator tidak boleh dianggap menutup celah validator lainnya.

## 5. Perubahan major: beri tahu dan minta keputusan sebelum implementasi

**M-01/M-02/M-04/M-05 PROPOSED/OPEN. M-03 penempatan docs diselesaikan atas instruksi user terbaru; commit/push belum.** Pilihan di bawah adalah bahan
keputusan, bukan roadmap baru yang diam-diam disetujui.

| ID | Keputusan yang dibutuhkan | Usulan yang dibahas dan trade-off | Batas tindakan saat ini |
|---|---|---|---|
| M-01 | Target verifikasi/release/server tanpa staging; ADR-015/P1-14..16 | Rancang prosedur maintenance pada target yang diizinkan, compatible refs, CI reachability, TLS/network/admin boundary. Reproducibility lebih kuat dari config-only, tetapi dapat perlu perubahan container/jaringan/downtime | Tidak deploy, membuat environment, membuka akses, atau mengubah workflow secrets sebelum keputusan |
| M-02 | Peran Redis; ADR-008 | Catat alasan mempertahankan Redis dan buktikan pemakaiannya; jika hendak kembali opsional, analisis cache/rate-limit/health/release semantics dulu | Pertahankan existing; tidak menghapus/menonaktifkan Redis atau menjanjikan distributed enforcement |
| M-03 | Penempatan/versioning context; ADR-011 | **Penempatan selesai:** user memilih `llm-gateway-docs` existing untuk docs/report/context; tidak perlu parent Git/submodules untuk pemindahan ini | Migrasi lokal belum commit/push. Tidak membuat remote/parent repo atau mengubah tiga repo komponen menjadi monorepo |
| M-04 | Penanganan CVE/image; ADR-013/security | Evaluasi image patch/upgrade dengan exact digests dan kompatibilitas, atau risk acceptance terbatas oleh pemilik keamanan. Perubahan image bisa memengaruhi DB/rollback | Tidak upgrade/downgrade, recreate, atau menaikkan baseline agar lolos |
| M-05 | Ownership/approval data dan biaya pilot; ADR-016/017/P1-09/10/15/17 | Tetapkan PIC, batas biaya, retensi/logging privacy, license matrix dan kelompok pilot. Pembatasan konten bisa memengaruhi audit/cost troubleshooting | Tidak menetapkan nominal sebagai kebijakan final, membuang histori, mengubah retention atau mengaktifkan commercial feature |

Memperkuat validator F-01/F-02 dan menambah tes acceptance pada kontrak yang sama adalah
penutupan gap Phase1, **bukan rewrite arsitektur**. Tetap belum dikerjakan pada sesi ini.
Pembatalan staging sudah diizinkan O-01; tidak perlu meminta ulang izin yang sama.
Penghapusan gate pilot/security atau penerimaan keterbatasan besar juga keputusan major.

## 6. Risiko awal yang tidak boleh hilang saat pindah context

| Risiko awal | Status konsolidasi |
|---|---|
| R-01 model access | Kedua model via gateway teruji; ownership/billing/direct account validation masih sebagian |
| R-02 OpenCode parity | API tools/stream + fast smoke ada; full agent/Responses parity tidak otomatis terbukti |
| R-03 cost | Spend tercatat; akurasi, corporate cap/alert dan pilot budget masih terbuka |
| R-04 DB outage semantics | Detector/recovery teruji; request auth/budget saat outage belum terbukti |
| R-05 budget precedence | Key budget/team RPM ada; inheritance/interaksi lengkap belum teruji |
| R-06 dua writer policy | Manual Git/API sekarang; ownership per domain dan reconciler Phase2 wajib |
| R-07 disable SSO vs key | SSO belum ada; snapshot offboarding manual bukan deprovision end-to-end |
| R-08 licensing | OPEN; jangan mengasumsikan enterprise capability termasuk lisensi |
| R-09 ownership | PIC platform/security/billing/reviewer belum disahkan dalam bukti |
| R-10 hosting/domain/IdP/data region | Local4000 dipilih, keputusan server/identity/governance tetap OPEN |

## 7. Cara mencatat ADR berikutnya

Sebut ID, keadaan sebelum, masalah, opsi, pilihan, backward compatibility, dampak
security/cost/data, rencana test/migrasi/rollback, **siapa menyetujui dan kapan**, serta
PR/commit implementasi. Jika belum ada persetujuan, tulis PROPOSED. Jangan mengubah
CONFIRMED atau menutup exception hanya atas dasar rekomendasi model.
