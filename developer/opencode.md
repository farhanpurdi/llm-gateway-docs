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

Perintah kedua hanya contoh acceptance berikutnya, **bukan klaim sudah lulus**.
Bukti tersimpan terbaru adalah fast basic response; API gateway kedua alias dan forced
tool calls memang lulus. Agent coding penuh—eksekusi tool dan penggunaan hasilnya—masih
perlu bukti terpisah. Jangan menyamakan tool call JSON dengan workflow coding selesai.

Jika model ditolak, tanyakan scope key/team ke operator. Jangan mencoba bypass dengan
master key atau mengganti model/provider. Lihat [incident](../operations/incident.md)
untuk 401/403,429 dan timeout; kirim request ID/error yang sudah disanitasi, bukan credential.
