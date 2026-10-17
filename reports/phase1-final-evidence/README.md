# Evidence penutupan Phase 1 — aktif

Eksekusi2026-10-17, Asia/Jakarta; [laporan aktif](../PHASE1_FINAL_CROSSCHECK_REPORT.md).
Artifact awal dan attempt gagal dipertahankan. File bernama final pada subtes bukan
klaim seluruh proyek selesai. Goal closure dan audit acceptance masih berjalan.

| Artifact | Isi |
|---|---|
| [source-before](source-before.json) / [remotes](remotes.json) |HEAD/branch/dirty awal dan identitas empat repo; bukancandidate commit baru |
| [full regression pertama](full-regression-attempt-1.txt) |85unit/5smoke/28live PASS dan13native scenarios PASS; live517,07s |
| [config CI](llm-gateway-config-validation.txt) / [infra CI](llm-gateway-infra-validation.txt) / [E2E CI](e2e-validation.txt) |Output komponen; lihat angka collection vs eksekusi aktual |
| [unit cleanup](unit-cleanup-final.txt) / [unit maintenance](unit-maintenance.txt) |Kasus cleanup/recovery offline; bukan runtime outage |
| [isolated E2E](isolated-e2e-unit.txt) |85unit PASS tanpa config sibling checkout |
| [fault guard](fault-guard-final.txt) / [initial wrong expectation](faults-attempt-1.txt) |400guard +200recovery; percobaan awal salah mengharapkan429 |
| [native faults](native-faults-final.txt) / [attempt1](native-faults-attempt-1.txt) / [attempt2](native-faults-attempt-2.txt) |13kasus final; metadata harness awal diperbaiki; tidak sengaja membanjiri provider |
| [container scan](container-scan-initial.txt) / [PG findings](postgres-findings.json) |Baseline PASS;1C/28H PG tetap ada |
| [secret infra](secrets-llm-gateway-infra.txt) / [config](secrets-llm-gateway-config.txt) / [E2E](secrets-llm-gateway-e2e.txt) |NativeGitleaks history/current PASS |
| [docs scan awal](secrets-docs.txt) / [final](secrets-docs-final.txt) / [verification](docs-secret-findings-verification.json) / [canary](docs-scanner-canary.json) |Dua hash ID native blocked ditangani dengan allowlist nilai persis; canary lain tetap terdeteksi |
| [lock config](lock-llm-gateway-config.txt) / [infra](lock-llm-gateway-infra.txt) / [E2E](lock-llm-gateway-e2e.txt) |Dry-run hash locked dependency; tidak menginstal aplikasi |
| [audit lock config](locked-audit-llm-gateway-config.txt) / [infra](locked-audit-llm-gateway-infra.txt) / [E2E](locked-audit-llm-gateway-e2e.txt) |Audit pin aktual PASS |
| [privacy/traffic](privacy-traffic-audit-initial.jsonl) / [runtime logs](runtime-log-privacy-initial.json) |Hanya aggregate; tidak menyimpan isi pesan/log mentah |
| [backup drill](backup-restore-drill.txt) / [health after restore](health-after-restore.txt) |83tabel identik dan layanan pulih; backup/dump/environment privat tidak masuk Git |
| [quiet window](maintenance-quiet-window.json) / [outage attempt](dependency-outage-attempt-1.txt) |Bukti window dan progres drill; periksa completion aktual sebelum menyebut PASS |
| [outage final terfokus](dependency-outage-final.txt) |2PASS179,39s; PG/Redis denial/recovery/spend retained |
| [rotasi attempt](key-rotation-attempt-1.txt) / [final](key-rotation-final.txt) |Asumsi flush counter awal diperbaiki;2PASS24,80s, keduaalias |
| [config drill source](config-drill.py) / [output](config-release-rollback.txt) |180→181→180,5smoke tiapapply, byte/inode/ID/image sama |
| [CI infra final](llm-gateway-infra-validation-final.txt) / [config](llm-gateway-config-validation-final.txt) / [E2E](e2e-validation-final.txt) |23infra/63config/97unitPASS, tiapvalidator lengkap |
| [isolated E2E final](isolated-e2e-unit-final.txt) |97unitPASS tanpa sibling checkout; venv existing dipakai |
| [GitHub oldHEAD CI](github-head-ci.json) |PR-triggered firstpage success padaHEADlama; bukan dirty candidate CI |
| [source under test](source-under-test.json) / [code manifest](code-manifest.json) |Hashsource/lock/workflow actual; README dokumentasi dapat diperbarui setelah capture |
| [full regression akhir](full-regression-final.txt) |Output proses run-all --include-outage; periksa akhir log, bukan collection atau nama final |
| [audit final source](audit-final.py) / [docs checkpoint](docs-validation-checkpoint.txt) |Kode audit read-only aggregate dan hasil validator docs sementara; bukan raw logs |
| [protected assets](protected-assets-final.json) |Sembilan runtime/model/provider/policy/template tetap byte-identik sejak awalgoal; hanya metadata izin.env |
| [integritas checkpoint](code-integrity-final.json) |27hash cocok sebelum finalisasiO-08/fixCompose; snapshot checkpoint, bukan manifestcandidate terakhir |
| [secret infra akhir](secrets-infra-final.txt) / [config](secrets-config-final.txt) / [E2E](secrets-e2e-final.txt) |History/current dan canary nativePASS setelah source stabil |
| [hasil fullrun](full-test-result-final.json) / [audit penutup](privacy-cleanup-runtime-final.json) / [exit audit](privacy-cleanup-audit-final.txt) |134pytest+13nativePASS exit0;261rowprivasi,296key/97teamblocked,IDs/image sama |
| [candidate source](candidate-source-manifest.json) / [refs](component-candidates.json) / [draftPR](candidate-pull-requests.json) |Hashsource current terikat keSHA; runtime/test sama denganfullrun, perubahanCI/README terpisah |
| [candidateCI](candidate-ci-final.json) |Validate/security enamjob padaSHA tiga komponenPASS; bukan statusHEADlama |
| [ComposeCI gagal](ci-infra-compose-failure.txt) / [fix lokal](infra-validation-compose-fix.txt) / [scanfix](infra-secrets-compose-fix.txt) |False JSON hilang diCI;8regresi baruPASS, explicitfalseYAML tetapwajib |
| [main audit](remote-main-audit.json) / [validasi docs](docs-validation-final.txt) / [standalone](docs-standalone-final.txt) |Historymain terpisah; tautan/roadmap/evidence diuji lokal dan modecheckout tunggal |

Tool native gitleaks8.28.0/trivy0.74.0 diverifikasi checksum rilis resmi dan disimpan
di `/tmp/phase1-tools`; pip-audit2.10.1 memakai interpreter `.venv` existing dengan
paket tool sementara. Tidak membuat venv/container scanner. Bukti yang tersimpan
tidak mencantumkan secret `.env`, dump, salt, atau raw key.
