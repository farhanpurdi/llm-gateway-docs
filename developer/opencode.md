# OpenCode dengan Company AI Gateway

[Model catalog](model-catalog.md) · [API](api.md) · [batas bukti](../architecture/phase-1.md).

## Persiapan

Dapatkan virtual key milik Anda dari operator melalui jalur privat dan pastikan scope
model yang diberikan. Jangan meminta atau memakai OpenAI provider key maupun master key.
Gunakan OpenCode yang kompatibel dengan [matriks versi](compatibility.md).

Template yang benar-benar ada:
[clients/opencode/opencode.jsonc](../../llm-gateway-config/clients/opencode/opencode.jsonc).
Salin/adaptasikan menjadi config proyek OpenCode Anda sesuai versi terpasang. Template
existing memakai `providers`, package `@opencode/ai/providers/openai-compatible`,
provider ID `company-ai`, dan default `company-ai/company-coding`.
Jangan menimpa config pribadi tanpa memeriksa isinya.

## Endpoint dan credential

Sediakan `COMPANY_LLM_API_KEY` lewat environment lokal/secret tooling yang disetujui.
Contoh berikut hanya placeholder, bukan key nyata:

```bash
export COMPANY_LLM_API_KEY="<virtual-key-dari-operator>"
export COMPANY_LLM_BASE_URL="http://localhost:4000/v1"
```

**Catatan template:** `settings.baseURL` pada JSONC existing masih literal
`http://localhost:4000/v1`; mengubah `COMPANY_LLM_BASE_URL` saja **tidak** mengubah endpoint
OpenCode. Cocokkan nilai `settings.baseURL` dengan target yang memang disetujui.
Saat ini tetap existing4000; HTTPS/domain server belum dikonfigurasi oleh dokumentasi ini.
Jangan commit key atau memasukkannya sebagai literal ke template bersama.

## Pemeriksaan client

Jalankan dari proyek client yang telah memuat config tersebut:

```bash
opencode run --standalone --model company-ai/company-fast "Reply exactly with OPENCODE_E2E_OK"
opencode run --standalone --model company-ai/company-coding "Reply exactly with OPENCODE_CODING_OK"
```

Kedua alias kini mempunyai bukti workflow agent pada OpenCode **2.0.18**, diuji
17 Oktober 2026. Operator onboarding menjalankan script asli dengan policy `pilot`;
CLI hanya menerima virtual key developer. Di fixture kode aman, masing-masing alias
membaca file, mengedit fungsi, menjalankan pemeriksa, lalu memakai receipt acak dari
output tool dalam jawaban akhirnya. Kode hasil juga diperiksa ulang secara independen.
Streaming SSE dan structured tool call API kedua alias lulus pada sesi yang sama.

Untuk mengulang acceptance dari repo `llm-gateway-e2e` dengan `.venv` existing aktif:

```bash
./scripts/run-smoke.sh
./scripts/test-opencode.sh --tb=short -s
```

Perintah pertama membuktikan onboarding/policy tanpa inference. Perintah kedua
mengirim request provider berbayar: dua agent pada fixture, maksimal 8 langkah dan
768 token output per request. Fixture menggunakan data/config CLI sementara dan
permission sempit: read/edit hanya file contoh, shell hanya `python3 verify.py`,
akses direktori luar ditolak. Jangan menyalin permission fixture sebagai kebijakan
semua proyek developer. Key/team tes diblokir setelah pengujian, audit dipertahankan.

[Laporan P1-11/P1-12 dan kode](../reports/P1_11_P1_12_OPENCODE_REPORT.md) menjelaskan
hasil dan batas bukti. Ini tugas Python kecil pada adapter Chat Completions yang
dipakai template; belum bukti proyek besar, seluruh tool, Responses parity, UI
interaktif atau pilot developer nyata. Contoh response teks di atas saja tidak
membuktikan workflow agent lengkap.

Jika model ditolak, tanyakan scope key/team ke operator. Jangan mencoba bypass dengan
master key atau mengganti model/provider. Lihat [incident](../operations/incident.md)
untuk 401/403,429 dan timeout; kirim request ID/error yang sudah disanitasi, bukan credential.
