# Evidence P1-11/P1-12

Eksekusi2026-10-17, Asia/Jakarta. [Laporan sederhana](../P1_11_P1_12_OPENCODE_REPORT.md),
[kode lengkap](../P1_11_P1_12_CODE_APPENDIX.md), [status acceptance](../../architecture/phase-1.md).
Layanan existing4000, OpenCode2.0.18 dan `.venv` existing; semua tes gateway serial.
CI offline dapat berjalan bersamaan dengan live karena tidak mengakses layanan/provider.

| Artifact | Bukti dan batas |
|---|---|
| [e2e-validation](e2e-validation.txt) | 8tahap PASS; collection106;79unit PASS; bukan22live PASS |
| [smoke-final](smoke-final.txt) | 5PASS termasuk onboarding operator asli dan persistence policy pilot |
| [live-final](live-final.txt) | 6PASS:dua agent lengkap, SSE kedua alias dan structured tool API kedua alias |
| [agent-attempt-1](agent-attempt-1.txt) | Dua agent PASS sebelum pengetatan jumlah request/key/upstream; bukan attempt gagal |
| [smoke-attempt-1](smoke-attempt-1.txt) | Lima smoke PASS; collection saat itu90 sebelum16unit baru |
| [health-final](health-final.txt) | Liveness/readiness/dependencies/model catalog PASS setelah pengujian |
| [runtime-final](runtime-final.txt) | Tiga container existing dengan ID/image/port sama; Docker Desktop semula mati lalu dinyalakan |
| [cleanup/accounting](cleanup-accounting.jsonl) | Query PG read-only:4team/4key0unblocked;16request agent dua putaran US$0.046622; regresi API legacy/invoice di luar total |
| [scope](scope-verification.json) | HEAD/dirty awal; perubahan source sesi; config/policy/template dan evidence lama identik |
| [docs-validation](docs-validation.txt) | Hasil final validator Markdown/roadmap/ADR/link dan historical evidence |
| [diff-checks](diff-checks.txt) | `git diff --check` empat repo |

Command E2E aktual:

```bash
bash scripts/ci/validate.sh
bash scripts/run-smoke.sh
bash scripts/run-live.sh tests/test_opencode.py --tb=short -x -s
bash scripts/run-live.sh tests/test_opencode.py tests/test_inference.py -k 'opencode_agent or streaming or tool_calling' --tb=short -x -s
```

Runner mengisi environment dari `.env` infra tanpa mencetak nilainya. Output CLI
agent ditangkap privat, lalu evidence hanya mencatat jenis event/status tool dan
ringkasan hasil fixture aman. Tidak menyimpan raw key, prompt/response privat atau
data session/database CLI dalam repo. Kode contoh yang dicetak pada log adalah
fixture publik yang sengaja dibuat untuk acceptance ini.

`scope-verification.json` menyimpan ref/hash source, bukan clean release manifest.
Source sudah dirty/untracked sebelum sesi ini. Tidak mengklaim commit/PR/CI remote,
semua22live, security scan, invoice, pilot nyata atau deployment berhasil.
