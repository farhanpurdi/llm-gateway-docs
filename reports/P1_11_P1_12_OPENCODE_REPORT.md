# Laporan P1-11/P1-12 — Onboarding dan agent OpenCode

Tanggal: **2026-10-17, Asia/Jakarta**. User meminta melanjutkan setelah P1-09/P1-10.
Status: **P1-11 dan P1-12 LOCAL_VERIFIED** dalam skenario di bawah; Phase 1/release belum selesai.
Mengikuti `gateway-acceptance` dan `gateway-handover` pada project-local skills.

## P1-11 — Developer bisa mulai memakai kedua alias

Sebelumnya template kedua alias dan jawaban teks fast sudah ada, tetapi belum ada
bukti onboarding operator sampai key developer dipakai oleh agent pada kedua alias.

Yang ditambahkan:

1. Fixture membuat team disposable di gateway existing port4000 dari nilai
   [pilot.yaml](../../llm-gateway-config/policies/teams/pilot.yaml): kedua alias,
   team US$10, anggota US$2, RPM30 dan TPM100000, durasi30d.
2. Fixture menjalankan [script onboarding operator asli](../../llm-gateway-infra/scripts/onboard-developer.sh)
   untuk membuat internal_user, menambahkan anggota dan menerbitkan virtual key.
   Output script yang berisi key ditangkap privat, tidak dimasukkan ke log/laporan.
3. Assertion memeriksa user/team/key, model yang diizinkan, budget anggota dan tanggal
   reset tersimpan. Key developer dapat melihat tepat dua alias lewat `/v1/models`.
4. CLI menerima hanya virtual key developer. Master/provider key tidak diteruskan.
   Template dibaca dari repo config dan diadaptasi hanya pada fixture sementara;
   config pribadi, template bersama dan `pilot.yaml` tidak ditimpa.
5. Cleanup menemukan semua key milik user fixture, memblokir dan memeriksa ulang
   statusnya, lalu memblokir team fixture. User/team/key/spend dipertahankan untuk audit.

Hasil: **PASS** pada smoke onboarding dan penggunaan nyata oleh kedua agent.
Tidak mengubah script infra; perbaikan durasi anggota P1-09 tetap digunakan.

## P1-12 — Agent benar-benar bekerja dan memakai hasil tool

Tes lama hanya memeriksa API mengembalikan tool call. Tes baru menjalankan OpenCode
existing **2.0.18**, adapter `@opencode/ai/providers/openai-compatible`, dan virtual
key hasil onboarding di atas. Tiap alias mendapat proyek Python kecil yang sama:

```python
# Sebelum: salah menghitung jumlah elemen, bukan total harga.
def subtotal_cents(prices):
    return len(prices)

# Hasil aktual dari kedua alias:
def subtotal_cents(prices):
    return sum(prices)
```

Agent harus membaca file, mengeditnya, lalu menjalankan **`python3 verify.py`**.
Verifier asli menguji lima input: kosong, satu item, beberapa harga, angka negatif,
dan pengulangan. Setelah PASS, verifier mencetak receipt acak yang belum ada di prompt.
Agent harus menyebut receipt tersebut pada jawaban akhir. Assertion memeriksa urutan
read→edit→shell→jawaban dan kesesuaian receipt dengan output tool. Verifier tidak boleh
berubah; kode hasil juga dijalankan ulang secara independen oleh pytest.

| Bukti final | company-fast | company-coding |
|---|---|---|
| Tool selesai | read, edit, shell | read, edit, shell |
| Hasil tool dipakai pada jawaban | PASS | PASS |
| Langkah/request model tersimpan | 4 | 4 |
| Token input / output | 6.281 / 160 | 6.648 / 253 |
| Spend native gateway | US$0.0070963 | US$0.0161988 |
| Kode akhir | `return sum(prices)` | `return sum(prices)` |
| Verifikasi kode independen | PASS | PASS |

Riwayat gateway dicocokkan sampai jumlah request, hash identitas key, user, team,
alias logical dan upstream yang benar. Batas fixture: maksimal8langkah, 768token
output/request dan timeout proses180detik. Permission menolak akses luar direktori,
tool lain/subagent dan shell selain verifier; read/edit hanya untuk `calculator.py`.
Permission ini khusus fixture, bukan perubahan kebijakan semua client perusahaan.

Regresi API **streaming SSE sampai `[DONE]`** dan **structured tool calling** juga
lulus untuk **kedua alias**. Ini bukti streaming API terpisah; event JSON CLI sendiri
tidak dipakai sebagai bukti transport SSE.

## Perubahan kode dan perlindungan regresi

Delapan file source ditambah/diperbarui; isi lengkap ada di
[lampiran kode beserta SHA-256](P1_11_P1_12_CODE_APPENDIX.md).

| File pada repo E2E | Penambahan/pembaruan |
|---|---|
| `tests/conftest.py` | Fixture onboarding operator asli, proyek CLI sementara, cleanup partial failure + verifikasi ulang |
| `tests/opencode.py` | Adapter CLI, environment tanpa credential admin/provider, config fixture, verifier, assertion urutan/result |
| `tests/test_opencode.py` | Onboarding/policy dan agent kedua alias, hasil kode independen serta atribusi seluruh request |
| `tests/test_inference.py` | Streaming diparameterisasi untuk kedua alias; token request streaming dibatasi |
| `tests/unit/test_opencode.py` | 16 kasus offline untuk mencegah jawaban palsu/urutan salah/receipt salah/error CLI dianggap PASS |
| `tests/unit/test_suite_validator.py` | Dua kasus penghapusan pada salinan sementara untuk menjaga regresi baru |
| `scripts/ci/validate-suite.py` | Kini mewajibkan22fungsi gateway, termasuk onboarding/agent |
| `scripts/test-opencode.sh` | Mengganti smoke teks satu alias dengan launcher dua agent memakai live runner existing |

HTTP E2E tetap melalui satu `LiteLLMClient`; helper OpenCode menjalankan CLI dan
memeriksa event, bukan client admin HTTP kedua. Script operator tetap memakai jalur
native infra yang sudah ada. Tidak menambah dependency, instalasi CLI atau `.venv`.
README E2E serta panduan OpenCode/compatibility/status/handover juga diperbarui.

Contoh guard yang mencegah klaim sukses hanya dari teks:

```python
assert read_index < edit_index < shell_index < final_index
# shell_index hanya terisi bila command verifier selesai dan output memuat receipt.
# final_index hanya terisi bila agent mengembalikan receipt yang sama sesudahnya.
```

## Pengujian yang benar-benar dijalankan

| Pemeriksaan | Hasil final |
|---|---|
| E2E CI existing | 8/8 tahap PASS; 79 unit PASS, exit0 |
| Collection | 106 kasus:79unit/5smoke/22live; 42fungsi; collection bukan eksekusi live |
| Smoke gateway | 5 PASS, exit0, 1,13detik |
| Live terfokus | 6 PASS, exit0, 31,03detik:2agent +2streaming +2toolcall |
| Health akhir | Liveness/readiness/dependencies/authenticated model catalog PASS |
| Cleanup namespace onboarding | 4team/4key;0unblocked, query PostgreSQL read-only |
| Dokumentasi | PASS:63Markdown/529tautan, roadmap/ADR valid;24evidence historis validator identik |
| Scope/source | PASS:8snapshot kode cocok;9asset aktif dan66laporan/evidence lama identik; diff4repo PASS |

Output aktual dan batas tiap artifact tersedia pada [indeks evidence](p1-11-12-evidence/README.md).

Enam belas kasus live lainnya tidak dijalankan pada sesi ini. CI infra/config, security
scan, reset budget 10menit dan seluruh H1–H10 tidak diulang; source/config terkait tidak
diubah. Hasil sesi lama tetap bukti bertanggal, bukan tes baru pada17Oktober.

Command utama dari repo E2E, memakai `.venv` workspace existing:

```bash
bash scripts/ci/validate.sh
bash scripts/run-smoke.sh
bash scripts/run-live.sh tests/test_opencode.py tests/test_inference.py -k 'opencode_agent or streaming or tool_calling' --tb=short -x -s
```

Percobaan awal agent juga **2 PASS** sebelum assertion jumlah request/key/upstream
diperketat, lalu kedua agent diulang dalam6teslive final. Unit awal63PASS sebelum16kasus
baru ditambahkan; final79PASS. Smoke awal5PASS dan final5PASS. Tidak ada kegagalan
acceptance yang disembunyikan; error saat discovery/menyalakan layanan dicatat berikutnya.

## Keadaan layanan, biaya dan batas bukti

Docker Desktop awalnya mati. Pemeriksaan sandbox juga sempat ditolak akses socket/log
home, lalu diperiksa dengan akses yang diizinkan. `docker desktop start --timeout 60`
menyalakan Docker Desktop existing; tiga container berjalan kembali dengan ID/image
yang sama: gateway `9c77da1dea53`, PostgreSQL `2abff28af371`, Redis `04c48e8f579d`.
Tidak menjalankan Compose up/recreate, membuat staging/container/environment, mengubah
mapping/provider/image/schema/port, commit/push atau deployment server.

Discovery schema URL mendapat HTTP403; dokumentasi V2 resmi, help CLI terpasang dan
debug config fixture dipakai sebagai acuan. Probe credential placeholder menghasilkan
401 yang diharapkan, tanpa inference provider. File config pribadi tidak digunakan.

Total spend native namespace baru `e2e-p1112-*` untuk **dua putaran agent**:
16request, US$0.046622 (Terra8request US$0.0142506; Sol8request US$0.0323714).
Angka ini berasal dari query PG, bukan invoice atau perhitungan tarif baru. Empat
request regresi streaming/tool API memakai fixture legacy dan tidak termasuk total ini.
Biaya final dua agent saja US$0.0232951; limit pilot adalah batas, bukan target belanja.

Bukti agent berlaku untuk tugas Python kecil pada adapter Chat Completions existing.
Belum menguji repo besar, semua tool/MCP, UI interaktif, Responses parity, multi-user
concurrency atau pilot2–5developer nyata. Tidak menetapkan permission perusahaan,
migrasi anggota lama, PIC/billing/cap provider, security sign-off atau kesiapan server.
Tidak ada perubahan major terhadap rancangan/roadmap pada sesi ini.

**Berikutnya P1-13/F-07:** provider429/5xx/timeout dan akses/budget saat dependency
terganggu. Siapkan skenario, recovery dan koordinasi terlebih dahulu; rekomendasi ini
tidak otomatis memulai outage atau deployment. Gate release/P1-18 tetap terbuka.

Acuan OpenCode resmi: [CLI V2](https://opencode.ai/v2/docs/cli),
[config](https://opencode.ai/v2/docs/config), [providers](https://opencode.ai/v2/docs/providers),
[permissions](https://opencode.ai/v2/docs/permissions), [agents](https://opencode.ai/v2/docs/agents).
Perilaku runtime yang diklaim tetap berdasarkan hasil CLI2.0.18 dan evidence lokal,
bukan mengasumsikan semua dokumentasi versi terbaru sama dengan binary terpasang.
