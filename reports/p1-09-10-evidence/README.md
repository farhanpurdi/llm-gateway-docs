# Evidence aktual P1-09/P1-10

Eksekusi 2026-10-13, Asia/Jakarta, pada Docker existing4000 / LiteLLM1.104.0.
Penutupan dokumentasi dan pemeriksaan source dilakukan 2026-10-14, Asia/Jakarta.
Baca [laporan per milestone](../P1_09_P1_10_LIMITS_COST_REPORT.md),
[kode lengkap](../P1_09_P1_10_CODE_APPENDIX.md) dan [status fase](../../architecture/phase-1.md).
Output lama tidak diganti dengan hasil baru. Credential pada attempt1 disensor;
tidak mencantumkan prompt/response provider atau secret environment.

| Artifact | Bukti / batas |
|---|---|
| [config-validation](config-validation.txt) | 7 tahap PASS, 63 tes kontrak; offline |
| [infra-validation](infra-validation.txt) | 7 tahap PASS, 23 tes operasional; compose hanya config, bukan up/recreate |
| [e2e-validation](e2e-validation.txt) | 8 tahap PASS; 84 collection, 61 unit PASS, 23 gateway/live deselected |
| [smoke-final](smoke-final.txt) | 4 PASS: health, invalid credential, exact dua model, policy persistence |
| [live-final](live-final.txt) | 11 PASS termasuk kedua alias cost, shared RPM/TPM/recovery, budgets, auto-reset, regresi limits existing; 676,73 detik |
| [before-fix](member-before-fix.json) / [after-fix](member-after-fix.json) | Script add-member asli: US$2 tanpa durasi/reset → durasi30d/reset1November2026UTC; tidak inference |
| [prices](prices.json) | Field publik model-info cocok dengan harga standar resmi yang diverifikasi; bukan invoice billing |
| [cleanup/accounting](cleanup-accounting.jsonl) | Query PostgreSQL read-only setelah seluruh tes:22team/80key blocked;33row namespaceP109 spend positif US$0.002816; legacy fixture/invoice di luar aggregate |
| [runtime-final](runtime-final.txt) | Tiga ID/image/port sama dengan inspeksi awal; tidak restart/recreate |
| [scope](scope-verification.json) | Sebelas kode/test/dependency +README E2E dalam scope;9asset aktif identik;11hash appendix cocok; source awal already dirty |
| [attempt1](live-attempt-1-redacted.txt) / [attempt2](live-attempt-2.txt) | Kegagalan harness sebelum diperbaiki; raw credential attempt1 diganti REDACTED_KEY |
| [attempt summaries](attempt-summaries.json) | Ringkasan hasil yang benar-benar diamati; bukan rekonstruksi stdout unit/smoke awal |
| [docs-validation](docs-validation.txt) | Validasi tautan/roadmap/ADR dan24fileevidencehistoris; hasil final sesi |
| [diff-checks](diff-checks.txt) | `git diff --check` empat repo PASS, exit 0 |

Command utama dijalankan dari repo masing-masing, memakai `PATH` yang mengarah ke
`.venv` workspace existing. Tidak menginstal package atau membuat environment.

```bash
# llm-gateway-config
bash scripts/ci/validate.sh
# llm-gateway-infra
bash scripts/ci/validate.sh
# llm-gateway-e2e
bash scripts/ci/validate.sh
bash scripts/run-smoke.sh --tb=short
bash scripts/run-live.sh tests/test_spend.py tests/test_pilot_limits.py tests/test_limits.py --tb=short -x -s
# llm-gateway-docs
python3 scripts/validate-docs.py --workspace
```

Statik berjalan terpisah dari live. Satu smoke awal sempat berjalan saat attempt1
biaya masih polling; team berbeda dan tidak berbagi counter. Setelah itu pengulangan
smoke/live dijalankan serial; tidak mengklaim pembuktian concurrency/distributed limits.
Tiga raw log CI/unit berisi hasil final, bukan seluruh riwayat setiap pengulangan.
