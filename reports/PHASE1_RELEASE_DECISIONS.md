# Keputusan sebelum penutupan release Phase 1

Status17Oktober2026: **opsiA disetujuiO-08 dan diterapkan**; usulan lain tetapOPEN/PROPOSED. [Hasil teknis aktif](PHASE1_FINAL_CROSSCHECK_REPORT.md)
dan [register M-01/M-04/M-05](../adr/README.md) menjadi dasarnya. Workflow live staging dihapus sesuaiO-08. Image, jaringan, secrets dan runner/environment
tetap existing; tidak membuat target baru.
Pilot nyata/peserta/PIC ditundaO-07 dan tidak ditanyakan ulang di sini.

## 1. Target live CI tanpa staging — M-01

Masalah konkret: `e2e/.github/workflows/live.yml` memakai environment `staging`,
`STAGING_*`, hosted runner dan checkout satu repo. Laptop4000 tidak dapat dijangkau
runner tersebut; acceptance terbaru juga memerlukan sibling repos, OpenCode dan
Docker existing. Mengganti nama secret tidak menyelesaikannya.

**OpsiA — APPROVED_OVERRIDE O-08:** pertahankan hosted GitHubCI untuk validasi offline/secret/dependency
scan. Hapus workflow live staging yang usang dan tetapkan live sebagai gate manual
lokal4000:run-all --include-outage, sourceSHA+hash, image digest, output tersensor,
cleanup/recovery, lalu reviewer memeriksa bukti pada PR/release. Tidak menciptakan
joblive berstatus hijau dari upload/collection. Tes live harus benar-benar berjalan.

Perubahan yang diterapkan:hapus `llm-gateway-e2e/.github/workflows/live.yml`,
selaraskanREADME/runbook/ADR-015, simpan manifest bukti pada laporan candidate.
Required hosted validate/security tetap ada. Risiko:maintenance/live membutuhkan
operator; otomatisasi remote ditunda. Rollback:restore workflow dariGit hanya setelah
targetnya bisa dijangkau dan secrets/runner disetujui, bukan menghidupkan staging lama.

**OpsiB:** runner self-hosted khusus pada host existing, workflow_dispatch saja dan
guard exact refs/clean tree/local4000. Memerlukan pemasangan/pengelolaan runner,
isolasi akses repository/secrets dan koordinasi maintenance. Belum disiapkan atau
dianggap diizinkan oleh larangan membuat environment baru.

## 2. Temuan image — M-04

Scan native terbaru lulus baseline yang sudah ada, tetapi temuan fixable tetap
LiteLLM0Critical/0High, PostgreSQL1Critical/28High, Redis0Critical/2High.
Baseline tidak dinaikkan dan hasil bukan risk acceptance produksi.

CriticalPG berada di binary`usr/local/bin/gosu`, Go stdlibv1.24.6:
**CVE-2025-68121**. [Laporan resmi Go](https://pkg.go.dev/vuln/GO-2026-4337)
menjelaskan masalahTLS session resumption dan versi perbaikan1.24.13/1.25.7.
[Hasil scanner](phase1-final-evidence/postgres-findings.json) membuktikan paket/versi,
bukan reachability/exploitability pada deployment ini. Tidak menyamakannya dengan
bugTLS pada daemonPostgreSQL atau menyatakan tidak berisiko tanpa analisis.

**Usulan:** tahan deploy server dan siapkan kandidat image patch beserta digest,
kompatibilitas PG/schema, backup/restore dan rollback setelah persetujuan. Pengujian
lokal source dapat dituntaskan dengan imageexisting; mengganti image/container
bertentangan dengan constraint saat ini sehingga tidak dilakukan diam-diam.
Opsi penerimaan risiko hanya bisa ditetapkan pemilik dengan scope/expiry/mitigasi;
assistant tidak menandatanganinya atas nama perusahaan.

## 3. Server, data dan publikasi candidate

Target host/domain/TLS/admin boundary dan backup terenkripsi luar host belum tersedia.
LocalHTTP4000 tidak dapat membuktikan gate tersebut. [Checklist](../operations/phase1-checklist.md)
tetap terpisah dari hasil tes lokal; jangan membuat server/proxy/container baru untuk
menutupnya tanpa target/persetujuan. Rotasi virtual key disposable sudah diuji;
master/provider/salt produksi memerlukan koordinasi distribusi credential/recovery.

Empat repoGitHub telah dikonfirmasi private. CI padaHEAD lama infra/config/E2E
berhasil, tetapi source awal dirty kini disimpan pada candidate commit; [snapshotCI](phase1-final-evidence/github-head-ci.json)
tidak mengesahkan candidate yang belum dipublikasikan. Laporan akhir harus menyertakan
hash source yang benar-benar diuji; commit/PR/requiredCI kandidat dan sign-off tetap
dicatat terpisah. Branch candidate tiga komponen sudahdipush untuk draftPR kedevelop existing;
belum merge, deploy/tag atau promosi main.

[Inventaris lisensi](../operations/license-inventory.md) tersedia. Billing/cap provider,
penerimaan lisensi dan aturan data/backup perusahaan belum menjadiPASS hanya karena
tes lokal berhasil atau pilot ditunda. Tidak perlu mengubah roadmap Phase2/3.
