# API gateway untuk developer

Kontrak fase sekarang: OpenAI-compatible Chat Completions di gateway, dengan virtual
key scoped. Endpoint lokal: `http://localhost:4000/v1`. Hanya gunakan target yang disetujui
operator. Target desain shared endpoint memakai TLS; O-10 menerima HTTP awal/keamanan
bertahap untuk arah VM GCP. HTTP internet belum mengenkripsi credential dan pesan.
[Panduan sederhana](panduan-penggunaan.md) mengikuti source existing dan tidak menjanjikan
seluruh OpenAI API/Responses parity atau deployment VM yang belum diuji.

## Model dan autentikasi

- `company-fast` dan `company-coding` adalah nama model client; lihat [katalog](model-catalog.md).
- Header: `Authorization: Bearer <virtual-key>`. Provider/master key hanya server/operator.
- Hanya model yang diizinkan policy key/team boleh digunakan. `company-coding` tidak
  otomatis tersedia bagi setiap user.

Credential sudah harus tersedia aman di environment; contoh ini tidak membuat key:

```bash
: "${COMPANY_LLM_API_KEY:?virtual key belum tersedia}"
: "${COMPANY_LLM_BASE_URL:?base URL harus mencakup /v1}"
curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 120 \
  "${COMPANY_LLM_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer ${COMPANY_LLM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"company-fast","messages":[{"role":"user","content":"Reply with OK"}]}'
```

Jangan menjalankan `set -x` atau membagikan output yang mengandung secret/prompt sensitif.
Request inference memakai biaya provider. Untuk daftar model, endpoint client adalah
`GET /v1/models`; alias yang tampil bukan pengganti uji authorization.

## Kemampuan dan batas hasil tes

| Kemampuan | Bukti sekarang |
|---|---|
| Chat kedua alias | API live PASS |
| Streaming | API company-fast PASS, SSE sampai `[DONE]` |
| Function/tool calling | Forced function call kedua alias PASS; contoh di source test |
| Penolakan akses | Invalid/blocked key401/403; coding403 ketika policy team fast-only |
| Rate/budget | Team RPM429 dan key budget422 pada versi yang diuji |
| Spend/audit | Spend positif dan retensi identitas/history; akurasi billing belum direkonsiliasi |
| Responses API, seluruh adapter parity, provider failure | Belum dinyatakan teruji lengkap |

Source contoh request/assertion:
[test_inference.py](../../llm-gateway-e2e/tests/test_inference.py),
[test_policy.py](../../llm-gateway-e2e/tests/test_policy.py),
[test_limits.py](../../llm-gateway-e2e/tests/test_limits.py).
Status/error bisa berubah pada versi berbeda; jangan hardcode retry semua error sebagai
masalah provider. Endpoint admin provisioning tidak untuk developer dan tidak dijelaskan
sebagai API publik client; lihat [lifecycle operator](../operations/lifecycle.md).
