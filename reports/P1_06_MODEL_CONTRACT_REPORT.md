# Laporan P1-06 — Kontrak model dan konsistensi konfigurasi

Tanggal: **2026-10-12, Asia/Jakarta**. Scope: **F-01/F-02**, paket pertama pada
[rencana penyelesaian Phase 1](../architecture/phase-1-completion-plan.md).
Status: **LOCAL_VERIFIED untuk validasi static/offline**. Commit/review/CI remote dan
eksekusi live assertion terbaru belum dilakukan; belum `DONE_VERIFIED` release.

## Hasil dalam bahasa sederhana

Config yang dipakai sekarang sudah benar. Masalahnya, pemeriksa sebelumnya juga
meloloskan config yang salah. Jika model/provider berubah tanpa sengaja atau alias
baru ditambahkan, kesalahan itu bisa lolos saat validasi.

Sekarang pemeriksa hanya menerima kontrak ini:

```python
PHASE1_MODELS = {
    "company-fast": "gpt-5.6-terra",
    "company-coding": "gpt-5.6-sol",
}
```

Upstream runtime harus memakai prefix `openai/`. Nilai yang disepakati datang dari
aturan validator, bukan diambil dari katalog yang dapat berubah. Mengubah runtime,
katalog model dan provider sekaligus ke model yang salah tetap ditolak.

## Penambahan dan pembaruan

| Bagian | Perubahan | Manfaat |
|---|---|---|
| Validator bersama | `scripts/ci/model_contract.py`, dipakai kedua CLI runtime/catalog | Satu aturan untuk runtime + model files + provider metadata pada repo config |
| Alias dan mapping | Tepat dua alias unik; exact upstream/provider/credential; identitas model dari filename | Alias tambahan/hilang/duplikat, upstream salah dan drift katalog gagal validasi |
| YAML/routing | Tolak YAML rusak/kunci duplikat, provider tambahan, route inactive dan override endpoint/fallback/alias yang belum disetujui | Salah struktur atau routing tersembunyi tidak lolos melalui jalur yang diperiksa |
| Entry point/CI config | Command lama mengarah ke CI lengkap; tambah tahap tes kontrak | Lokal dan CI menjalankan tujuh tahap yang sama |
| Release config | Guard `validate_config()` pada capture dan load/deploy/rollback diperketat | Mapping atau env reference salah ditolak, termasuk ketika checksum benar |
| E2E `/v1/models` | Dari dua alias harus ada, menjadi tepat dua alias tanpa duplikat | Alias tambahan yang ditampilkan gateway menggagalkan tes live berikutnya |
| Regresi offline | 63 tes config baru, 10 tambahan infra (total 22), 7 tambahan unit E2E (total 29) | Config benar diterima, config salah ditolak; timeout/urutan tetap dapat berubah |

Core guard alias:

```python
if len(names) != len(set(names)):
    raise ContractError(f"{location}: duplicate logical alias")
if set(names) != set(PHASE1_MODELS):
    raise ContractError(f"{location}: expected exactly company-fast and company-coding")
```

Core guard upstream:

```python
expected = f"openai/{PHASE1_MODELS[name]}"
if params.get("model") != expected:
    raise ContractError(f"{name}: upstream must be {expected}")
if params.get("api_key") != "os.environ/OPENAI_API_KEY":
    raise ContractError(f"{name}: credential must use os.environ/OPENAI_API_KEY")
```

Assertion model exposure:

```python
assert model_ids == {fast_model, coding_model}
assert len(data["data"]) == len(model_ids), "Duplicate logical models exposed"
```

**Kode lengkap sepuluh file implementasi/tes** ada pada
[P1_06_CODE_APPENDIX.md](P1_06_CODE_APPENDIX.md). Snapshot adalah kode saat laporan,
bukan file runtime baru. Source aktif tetap di repo komponen.

## Hasil pengujian aktual

Python memakai `.venv` existing. Tes memakai folder sementara, tidak membuat
environment/container baru dan tidak melakukan inference berbayar, provisioning,
outage, restart, capture/deploy/rollback atau pengubahan config aktif.
`docker compose config` pada validator infra hanya membaca/render config.

| Command dari repo terkait | Hasil aktual | Bukti |
|---|---|---|
| Config: `bash scripts/ci/validate.sh` | **7/7 PASS; 63 tes kontrak PASS** | [config-validation.txt](p1-06-evidence/config-validation.txt) |
| Infra: `bash scripts/ci/validate.sh` | **7/7 PASS; 22 tes operasi/release PASS** | [infra-validation.txt](p1-06-evidence/infra-validation.txt) |
| E2E: `bash scripts/ci/validate.sh` | **8/8 PASS; 29 unit PASS**, 15 smoke/live tidak dijalankan | [e2e-validation.txt](p1-06-evidence/e2e-validation.txt) |
| Dua CLI config + fungsi release pada enam salinan config | **PASS sesuai expected outcome** | [contract-matrix.json](p1-06-evidence/contract-matrix.json) |
| Source dibandingkan hash sebelum sesi | Config/model/provider/policy/client template identik; hanya source dalam scope berubah | [scope-verification.json](p1-06-evidence/scope-verification.json) |
| Validator docs + diff whitespace | **PASS: 56 Markdown, 419 tautan; 24 evidence lama identik**, diff check empat repo PASS | [docs-validation.txt](p1-06-evidence/docs-validation.txt) |

63 + 22 + 29 = **114 tes offline lulus**, tanpa menjumlahkan lagi tes yang sudah
dijalankan di dalam CI. Ini bukan hasil 114 tes live gateway.

Percobaan awal mempunyai dua subtest shell gagal karena Python sistem tidak memiliki
PyYAML. Harness diperbaiki agar subprocess shell memakai interpreter dari environment
tes yang sama. Seluruh 63 tes kemudian lulus; dependency/environment baru tidak dibuat.

## Reproduksi celah sebelum dan setelah

| Kasus | Sebelum (bukti review 10 Oktober) | Setelah (eksekusi 12 Oktober) |
|---|---|---|
| Config yang disepakati | Exit 0 | Exit 0, kedua CLI |
| Upstream/provider salah | Exit 0 | Exit 1, kedua CLI; release menolak |
| Alias tambahan | Exit 0 | Exit 1, kedua CLI; release menolak |
| Katalog model/provider berbeda | Belum ada cross-check lengkap | Exit 1, kedua CLI |
| Ketiga sumber diganti ke upstream salah | Belum diuji | Exit 1, kedua CLI; release menolak |

Bukti sebelum tetap di [context review](context-review/validator-contract-check.json),
tidak ditimpa. Matrix baru memeriksa release terhadap bytes config snapshot;
drift katalog deskriptif diperiksa kedua CLI config, bukan fungsi release standalone.
Pemisahan ini menjaga CI infra dapat berjalan tanpa checkout repo config.

## Batas hasil dan gate tersisa

- Static/offline mengunci file config yang diperiksa. Tidak membuktikan model dinamis
  dari database/API admin atau seluruh fitur router LiteLLM yang tidak digunakan.
- Katalog tetap deskriptif; tidak membangun generator, provider baru atau reconciler.
- Assertion `/v1/models` diuji dengan respons simulasi dalam unit test. Eksekusi live
  assertion terbaru dilakukan pada candidate akhir; bukti live lama tetap tanggal 10 Oktober.
- Endpoint/routing alternatif belum disetujui dalam kontrak existing. Perubahan sah
  di masa depan perlu ADR serta pembaruan validator dan tes.
- Guard config dan infra berada pada repo masing-masing agar CI standalone tetap bekerja.
  Mapping keduanya harus ikut direview bila keputusan ADR berubah.
- Tidak ada commit/push/review remote. Source dirty/untracked sebelum sesi dipertahankan.
- Gitleaks/Trivy/audit dependency tidak diulang. Git safety validator bukan pengganti
  pemeriksaan keamanan candidate akhir.

Tidak ada perubahan major pada routing aktif, image, jaringan, dependency atau data.
P1-06 terverifikasi lokal dalam scope tersebut; **Phase 1 gate masih terbuka**.

## Langkah berikutnya

Paket teknis berikutnya **P1-09/P1-10**: limits, token dan biaya. Nilai budget/RPM/TPM
pilot final tetap perlu keputusan owner M-05. Paket ini belum dikerjakan dalam sesi
P1-06; M-01/M-02/M-04/M-05 tetap terbuka.
