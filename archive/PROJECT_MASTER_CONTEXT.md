> **ARSIP — jangan gunakan sebagai current state atau instruksi bootstrap.**
> Mulai dari [README](../README.md) dan [master aktif](../MASTER_CONTEXT.md).
> Tautan dipindahkan sesuai lokasi baru; checksum historis merujuk snapshot sebelum relokasi.

> **Navigasi konsolidasi — 2026-10-10:** file ini dipertahankan sebagai **baseline rancangan awal**.
> Mulai chat baru dari [PROJECT_CONTEXT_MASTER.md](../MASTER_CONTEXT.md), lalu dokumen fase dan register keputusan yang ditautkan.
> Label PLANNING/TODO/kanonik di tubuh dokumen adalah snapshot asli; jangan menggunakannya untuk mengulang bootstrap atau menimpa status terbaru.
> Keputusan desain asli tetap berlaku kecuali ada override user/ADR yang tercatat. Tidak ada perubahan arsitektur melalui banner ini.

# LLM Gateway — Project Master Context & Execution Playbook

> **Dokumen kanonik lintas chat, model, dan developer — simpan di root `company-ai-platform/`**  
> Project: **Internal Company LLM Gateway berbasis LiteLLM**  
> Baseline dokumen: **2026-10-10** | Versi konteks: **v1.0.0** | Bahasa: Indonesia  
> Lokasi Git yang dituju: `company-ai-platform/PROJECT_MASTER_CONTEXT.md` (**root folder proyek**)  
> Status proyek: **PLANNING — belum ada implementasi, deploy, atau pengujian yang dikonfirmasi dalam percakapan ini.**

---

## 0. BACA INI DULU — Konteks 60 detik

**Tujuan:** menyediakan satu endpoint internal OpenAI-compatible untuk anggota tim yang memakai **OpenCode** (client awal), melalui **LiteLLM Proxy**, sehingga akses model, virtual API key, kuota, budget, serta penggunaan dapat diatur **per user dan/atau team**. Provider API key tidak boleh terlihat oleh developer. Arsitektur jangka panjang dipisah menjadi **Data Plane** (LiteLLM untuk request inferensi) dan **Control Plane** (administrasi organisasi, policy, key, audit, dan portal).

**KEPUTUSAN PROVIDER PHASE 1 (FINAL dalam baseline ini):** **HANYA OpenAI API**. Jangan menambahkan atau mengaktifkan Gemini, DeepSeek, Huawei/GLM, Anthropic, dll. sampai ada perubahan scope/ADR yang disetujui. Meski hanya OpenAI sekarang, konfigurasi dan nama logical model wajib tetap **multi-provider ready**.

| Logical model (yang terlihat oleh user) | Provider | Target upstream model ID | Status |
|---|---|---|---|
| `company-fast` | OpenAI API | `gpt-5.6-terra` | **Dipilih; akses API key belum diuji** |
| `company-coding` | OpenAI API | `gpt-5.6-sol` | **Dipilih; akses API key belum diuji** |

Kedua model ID tercantum pada dokumentasi resmi OpenAI per 2026-10-10. Namun keberadaannya di dokumentasi **bukan bukti** bahwa API key/proyek/akun perusahaan memiliki akses. Buktikan lewat API dan end-to-end call. ChatGPT plan/subscription **tidak sama dengan** OpenAI API access/billing.

**Urutan utama:**
1. **Phase 1 — MVP gateway:** Docker + LiteLLM + PostgreSQL, 2 alias OpenAI, virtual key per pengguna, model restriction, basic budget/rate limit, usage/cost, OpenCode, tests.
2. **Phase 2 — Control Plane:** SSO, users/teams, service API, RBAC, model catalog, key management/self-service, admin portal, audit, rekonsiliasi policy.
3. **Phase 3 — Enterprise readiness:** hardening jaringan/secrets, observability, HA, backup/DR, guardrails, performance & security testing.

**Batas penting:** Jangan membangun UI custom pada Phase 1. Jangan membuat fitur yang sudah disediakan LiteLLM tanpa kebutuhan terukur. Jangan menganggap Redis wajib pada boot pertama; nilai kebutuhannya sesudah MVP, sambil menyiapkan desain untuk rate limiting/distributed cache jika diperlukan.

**Sumber kebenaran progres:** bagian **14. Current State** dan **15. Work Log & Handoff** harus diperbarui *setelah* pekerjaan dan pengujian benar-benar selesai. Bagian rencana **bukan bukti implementasi**.

---

## 1. Cara menggunakan dokumen di chat/model baru (ANTI-LOST-IN-THE-MIDDLE)

**Instruksi wajib untuk AI/engineer yang melanjutkan proyek:**

1. Baca **§0**, **§2**, **§3**, **§5**, **§14**, dan **§15** terlebih dahulu; baru baca bagian yang relevan dengan tugas.
2. Sebelum mengubah kode, cek isi repository aktual (files, commits, tags, config) dan cocokkan dengan **§14**. Jika belum dapat akses repository, **jangan mengklaim** pekerjaan telah dilakukan.
3. Patuhi semua keputusan **CONFIRMED**. Jangan memasukkan provider selain OpenAI pada Phase 1 tanpa approval tercatat.
4. Kerjakan **satu work item kecil** dari checklist; cantumkan ID tugas, file yang berubah, command pengujian, hasil nyata, risiko, dan next step.
5. Setelah test lolos dan commit tersedia, update **§14 (status)** dan **§15 (log)**. Update rencana/ADR kalau keputusan berubah. Jangan menghapus catatan kegagalan penting.
6. Jika konteks sempit, prioritaskan §0 → §2 → §14 → §15 → item aktif di §8/9/10; jangan mengganti rancangan berdasarkan asumsi.
7. Bila ada ketidaksesuaian antara dokumen dan kode, laporkan sebagai **DRIFT**, tentukan fakta lewat verifikasi, dan usulkan sinkronisasi. Jangan diam-diam mengubah keputusan.

**Template prompt di chat baru (copy-paste):**

```text
Anda adalah lead system architect + implementer untuk proyek Internal LLM Gateway.
Baca file PROJECT_MASTER_CONTEXT.md ini sepenuhnya, terutama §0, §2, §3,
§14, §15. Anggap sebagai baseline keputusan dan prosedur kerja.
Phase 1 HANYA OpenAI API dengan alias company-fast → gpt-5.6-terra dan
company-coding → gpt-5.6-sol. Jangan menambah provider tanpa persetujuan.
Sebelum coding, verifikasi status aktual di Git/files dan identifikasi 1 task
prioritas berikutnya dari roadmap. Kerjakan task itu, jalankan validasi,
kemudian beri laporan: perubahan file, test+hasil, risiko/blocker, commit SHA
(jika tersedia), update status dan next action. Jika status belum diketahui,
tandai UNKNOWN — jangan mengarang progres.
```

**Urutan prioritas bila ada konflik:** (1) permintaan terbaru eksplisit dari pemilik proyek → (2) ADR terbaru yang disetujui → (3) dokumen ini → (4) kode + hasil tes sebagai bukti *kondisi terpasang* → (5) rekomendasi lama. Bedakan **keputusan target** vs **kondisi real**; kedua hal bisa berbeda saat migrasi.

---

## 2. Architecture Decision Registry

Status: `CONFIRMED` = ditetapkan dari percakapan ini; `BASELINE` = rekomendasi desain yang dijadikan arah kerja dan dapat diubah lewat ADR; `OPEN` = perlu keputusan/validasi.

| ID | Keputusan | Status | Keterangan |
|---|---|---|---|
| ADR-001 | LiteLLM Proxy sebagai LLM gateway/data plane | CONFIRMED | Central OpenAI-compatible endpoint |
| ADR-002 | Phase 1 provider **OpenAI saja** | CONFIRMED | Ekspansi provider ditunda, bukan dilarang selamanya |
| ADR-003 | `company-fast` → `openai/gpt-5.6-terra` (bentuk LiteLLM) | CONFIRMED | Upstream ID `gpt-5.6-terra` |
| ADR-004 | `company-coding` → `openai/gpt-5.6-sol` (bentuk LiteLLM) | CONFIRMED | Upstream ID `gpt-5.6-sol` |
| ADR-005 | OpenCode sebagai client pertama | CONFIRMED | Client lain dapat ditambah kemudian |
| ADR-006 | Virtual key user/team; provider key hanya di server | BASELINE | Master key tidak boleh dipakai di client |
| ADR-007 | PostgreSQL mulai Phase 1 | BASELINE | Diperlukan untuk virtual key & budget/spend persisten |
| ADR-008 | Redis dipersiapkan namun **opsional di bootstrap** | BASELINE | Aktifkan saat kebutuhan cache/rate limit terdistribusi dibuktikan |
| ADR-009 | Logical model alias sebagai API contract client | BASELINE | Hindari hardcode vendor di OpenCode |
| ADR-010 | Control Plane terpisah dari Data Plane | BASELINE | Bangun custom backend/UI mulai Phase 2 |
| ADR-011 | Phase 1 memakai 3 repo komponen: infra, config, e2e; master context berada di root `company-ai-platform/` | BASELINE | Jika root juga Git repo, tautkan repo komponen sebagai submodule (bukan nested repo biasa); backend/frontend saat Phase 2 |
| ADR-012 | GitOps untuk desired config, tidak ada 2 penulis policy | BASELINE | Phase 2 perlu mekanisme rekonsiliasi yang eksplisit |
| ADR-013 | Repo, image, dependency **version pinned** saat deploy | BASELINE | Jangan pakai `latest` untuk deployment terulang |
| ADR-014 | SSO provider (Entra ID/Google/dll.) | OPEN | Pilih sesuai identity corporate saat Phase 2 |
| ADR-015 | Hosting (VM, Kubernetes, cloud, on-prem) | OPEN | MVP memakai Docker Compose dev/staging, production infra menyusul |
| ADR-016 | Budget nominal, RPM/TPM, jumlah user | OPEN | Jangan mengarang angka sebagai kebijakan final |
| ADR-017 | Lisensi LiteLLM dan fitur enterprise | OPEN | Audit fitur yang tersedia pada versi/lisensi yang dipakai |

**Aturan mengubah ADR:** perubahan harus menyebut nomor ADR, alasan, trade-off, dampak backward compatibility, dampak security/cost, pihak yang menyetujui, tanggal, dan PR/commit yang mengimplementasikan. Tidak cukup mengubah diagram tanpa log.

---

## 3. Scope dan kontrak teknis

### 3.1 Di dalam scope Phase 1

- Endpoint LiteLLM (lokal/dev/staging) yang kompatibel dengan OpenAI API.
- Dua logical model alias **persis** `company-fast` dan `company-coding`.
- OpenAI API sebagai satu-satunya provider upstream; tidak ada cross-provider fallback sekarang.
- PostgreSQL untuk key management, user/team metadata minimal, spend/budget.
- Virtual key unik per developer (atau workload/service account), dapat dicabut, scoped model.
- Basic user/team access control, cost tracking, budget/rate limit yang benar-benar dites.
- Client OpenCode menggunakan virtual key; streaming dan tool calling diuji khusus workload coding.
- Secrets handling, local security baseline, CI, smoke/integration/E2E tests, runbook minimum.

### 3.2 Di luar scope Phase 1

- Custom Admin Portal, bespoke auth, custom billing engine, SSO automation.
- Gemini/DeepSeek/Huawei/Anthropic, multiple provider router/fallback, guardrail kompleks.
- Kubernetes, multi-region, HA, auto-scaling, advanced WAF — kecuali diwajibkan kebijakan infrastruktur untuk deployment awal.
- Fitur enterprise LiteLLM berlisensi tanpa validasi lisensi/biaya terlebih dahulu.

### 3.3 Model contract

| Properti | `company-fast` | `company-coding` |
|---|---|---|
| Nama di request client | `company-fast` | `company-coding` |
| Provider saat ini | `openai` | `openai` |
| LiteLLM upstream model | `openai/gpt-5.6-terra` | `openai/gpt-5.6-sol` |
| Tujuan workload | General/fast/cost-conscious | Development/coding/tool use |
| Fallback di Phase 1 | **Tidak dikonfigurasi** | **Tidak dikonfigurasi** |
| Status verifikasi akun | NOT TESTED | NOT TESTED |

Jika model/model permission gagal di akun OpenAI yang digunakan: **blokir acceptance**, catat error dan diskusikan penggantian lewat ADR; jangan secara diam-diam mengarahkannya ke model lain. Uji support parameter, tools, streaming, dan route `/v1/chat/completions` secara nyata pada pinned LiteLLM release (model OpenAI juga mendukung Responses API; client adapter harus diuji).

### 3.4 Target arsitektur

```text
[Developer / OpenCode / future clients]
        |  Virtual Key + model="company-fast"|"company-coding"
        v
[Internal TLS endpoint / reverse proxy (jika perlu)]
        v
[LiteLLM Proxy = DATA PLANE]
   | auth / model ACL / spend / budget / rate limit / routing
   +---- PostgreSQL (persistent identity/key/spend records)
   +---- Redis (optional Phase 1; expanded Phase 2/3)
   |
   +---- OpenAI API
          |-- gpt-5.6-terra
          `-- gpt-5.6-sol

[Phase 2 Admin Portal] --> [Control Plane API]
                                    |
                          [approved policy changes]
                                    v
                              [LiteLLM APIs/config]

[Phase 3: API Gateway/WAF, secrets manager, observability, HA, DR, guardrails]
```

**Boundary:** Control Plane memutuskan *siapa/boleh apa* dan lifecycle provisioning; LiteLLM menegakkan policy saat runtime dan meneruskan inferensi. Control Plane tidak perlu mengimplementasikan LLM inference ulang. Jangan izinkan frontend mengakses LiteLLM master key atau provider API key.

---

## 4. Struktur Git/repository dan kepemilikan

Folder induk yang disepakati adalah **`company-ai-platform/`**. File **`PROJECT_MASTER_CONTEXT.md` wajib langsung berada di root folder ini**, bukan di `llm-gateway-config/`. Lokasi Git hosting/organization belum diputuskan. Rencana **tiga repository komponen** tetap dipertahankan; bila `company-ai-platform/` juga merupakan repository Git, kelola repo komponen sebagai **Git submodule** agar tidak terjadi nested repository yang tidak terlacak. Alternatif mengubahnya menjadi monorepo harus melalui ADR tersendiri, bukan perubahan diam-diam.

### 4.1 Buat sekarang — Phase 1

```text
company-ai-platform/
├── PROJECT_MASTER_CONTEXT.md                # DOKUMEN KANONIK — ROOT FOLDER
├── .gitmodules                              # jika tiga repo komponen dipasang sebagai submodule
├── llm-gateway-infra/                    # Compose, network, deploy env, operations
│   ├── README.md
│   ├── docker/compose.dev.yml
│   ├── docker/compose.staging.yml        # saat staging siap
│   ├── environments/dev/.env.example
│   ├── environments/staging/.env.example
│   ├── scripts/bootstrap.sh
│   ├── scripts/healthcheck.sh
│   ├── scripts/backup-postgres.sh        # validasi saat memakai data real
│   ├── release/versions.lock             # versi image + ref config/e2e yang cocok
│   ├── .github/workflows/ci.yml
│   └── .gitignore
│
├── llm-gateway-config/                   # Konfigurasi runtime dan kontrak model
│   ├── README.md
│   ├── config/litellm.dev.yaml
│   ├── config/litellm.staging.yaml       # ditambahkan saat staging
│   ├── config/litellm.production.yaml    # saat siap production
│   ├── catalog/model-catalog.md
│   ├── policies/access-matrix.md
│   ├── examples/opencode.json.example
│   ├── examples/env.client.example
│   ├── scripts/validate-config.sh
│   ├── .github/workflows/ci.yml
│   └── .gitignore
│
└── llm-gateway-e2e/                      # Black-box automated tests
    ├── README.md
    ├── pyproject.toml                    # bila memilih pytest
    ├── tests/test_health.py
    ├── tests/test_models.py
    ├── tests/test_auth.py
    ├── tests/test_model_acl.py
    ├── tests/test_chat_streaming.py
    ├── tests/test_tool_calls.py
    ├── tests/test_rate_budget.py
    ├── tests/test_spend.py
    ├── scripts/smoke.sh
    ├── .github/workflows/ci.yml
    └── .gitignore
```

**Perhatian implementasi:** file `.yaml` katalog kebijakan bukan otomatis bisa dibaca LiteLLM. Untuk Phase 1, cukup gunakan **native LiteLLM config + API virtual key/team**. Jika memecah config ke beberapa file, buat generator/validator yang benar-benar menghasilkan config aktif; jangan membuat folder `models/*.yaml` yang tidak pernah di-load. Dokumen `model-catalog.md` hanyalah kontrak manusia sampai sinkronisasi dibuat.

### 4.2 Ditambahkan mulai Phase 2

```text
llm-control-plane/           # Backend service, provisioning/reconciliation, DB migrations
llm-admin-portal/            # UI management
llm-gateway-docs/            # Opsional: publikasi documentation portal
```

Rancangan awal `llm-control-plane/src/`: `auth/`, `users/`, `teams/`, `model_catalog/`, `policy/`, `api_keys/`, `budgets/`, `usage/`, `audit/`, `litellm_adapter/`, `reconciliation/`, `tests/`.  
Rancangan awal `llm-admin-portal/src/`: `login/`, `dashboard/`, `users/`, `teams/`, `models/`, `keys/`, `policies/`, `budget/`, `usage/`, `audit/`.

Stack usulan **bukan keputusan final**: backend FastAPI + SQLAlchemy/Alembic, frontend Next.js/React, sesuai kompetensi tim. Kebutuhan sebenarnya: API punya OpenAPI contract, migration, tests, dan RBAC teruji. Jika docs repo muncul, tetap simpan **satu** canonical project context di **`company-ai-platform/PROJECT_MASTER_CONTEXT.md`**; docs lain hanya menautkannya (hindari duplikasi yang drift).

### 4.3 Git workflow dan rilis

- Repo private, protected `main`, mandatory PR review dan CI. Untuk tim kecil, pakai **short-lived feature branches → PR → main**; tambah `develop` hanya jika sungguh ada kebutuhan staging/integration branch terpisah. Jangan mencampur kebijakan branching tanpa keputusan.
- Nama branch: `feat/p1-04-openai-models`, `fix/p1-10-budget-enforcement`, `docs/context-checkpoint`.
- Commit menjelaskan ID pekerjaan: `feat(config): [P1-04] add OpenAI model aliases`.
- Jangan meletakkan live provider keys, master key, virtual keys, `.env`, database dump, token trace, raw prompt sensitif dalam Git atau CI log.
- Pin versi LiteLLM **ke versi spesifik/digest** yang telah diuji, bukan `:latest`. Catat versi Docker/Compose, schema/migration dan SHA config/e2e di `release/versions.lock`/release notes.
- Perubahan config dirilis bersama perubahan infra yang kompatibel; lint, smoke, dan negative authorization tests wajib sebelum promote ke staging.

---

## 5. Konfigurasi referensi minimum (Phase 1)

### 5.1 Template LiteLLM (`llm-gateway-config/config/litellm.dev.yaml`)

> **Template perencanaan, belum dieksekusi.** Cocokkan sintaks dengan dokumentasi versi LiteLLM yang dipin; lakukan boot + functional tests. ENV berikut harus disuplai dengan mekanisme lokal yang aman.

```yaml
model_list:
  - model_name: company-fast
    litellm_params:
      model: openai/gpt-5.6-terra
      api_key: os.environ/OPENAI_API_KEY

  - model_name: company-coding
    litellm_params:
      model: openai/gpt-5.6-sol
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
```

- `OPENAI_API_KEY`: upstream provider key, hanya berada pada runtime gateway.
- `LITELLM_MASTER_KEY`: credential admin gateway; **tidak boleh diberikan ke OpenCode/user**. Gunakan nilai aman yang memenuhi persyaratan versi LiteLLM (format `sk-...`).
- `DATABASE_URL`: PostgreSQL yang terpisah/terisolasi; jangan taruh password literal dalam YAML.
- Bila versi LiteLLM mensyaratkan `LITELLM_SALT_KEY`, siapkan secret ini dan pertahankan konsistensinya antar restart/replica. Verifikasi prasyarat release yang dipakai.
- **Jangan aktifkan** `set_verbose` atau logging prompt mentah sebagai default shared environment.
- Nama upstream dalam LiteLLM memakai prefix provider `openai/`; client tetap hanya melihat logical alias.

### 5.2 `.env.example` server — tanpa credential nyata

```dotenv
# HANYA CONTOH NAMA VARIABLE; ISI NILAI ASLI DI SECRET STORE / .env LOKAL
OPENAI_API_KEY=<set-securely>
LITELLM_MASTER_KEY=<sk-long-random-admin-key>
LITELLM_SALT_KEY=<set-if-required-by-pinned-release>
DATABASE_URL=postgresql://<user>:<password>@postgres:5432/<db>
```

Commit `.env.example`, **jangan commit** `.env`; jalankan secret scanning di CI. Pada laptop, batasi bind PostgreSQL dan LiteLLM ke `127.0.0.1` bila tidak perlu diakses jaringan. Di staging/shared network, wajib HTTPS/TLS, private networking, firewall, dan autentikasi. Reverse proxy TLS minimum **boleh hadir sebelum Phase 3** jika service diakses tim; Phase 3 mengembangkan enterprise gateway/WAF, bukan menunda keamanan dasar.

### 5.3 OpenCode custom provider (`examples/opencode.json.example`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "company-llm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Company LLM Gateway",
      "options": {
        "baseURL": "http://127.0.0.1:4000/v1",
        "apiKey": "{env:LITELLM_VIRTUAL_KEY}"
      },
      "models": {
        "company-fast": { "name": "Company Fast" },
        "company-coding": { "name": "Company Coding" }
      }
    }
  }
}
```

- Endpoint `127.0.0.1` hanya untuk mesin development; ganti `https://llm.<domain-internal>/v1` untuk pemakaian team.
- `LITELLM_VIRTUAL_KEY` adalah virtual key milik developer, **bukan** OpenAI key atau master key.
- Konfigurasi di atas menggunakan adapter **chat completions** OpenCode; jika tool calling/streaming/agent workflow membutuhkan **Responses API** atau perilaku lain, lakukan tes dan sesuaikan adapter `@ai-sdk/openai` sesuai dokumentasi versi OpenCode. Jangan menganggap parity tanpa bukti.
- Tidak mencantumkan ukuran context/output token secara hardcode sebelum memverifikasi model + adapter saat implementasi.

### 5.4 Alur akses dan provisioning user (Phase 1)

```text
Admin menyimpan OpenAI API key secara aman
   -> LiteLLM terhubung ke PostgreSQL
   -> admin membuat user/team minimal & virtual key dengan model ACL
   -> tiap developer menerima virtual key secara aman
   -> OpenCode memakai company-fast / company-coding
   -> LiteLLM memeriksa key, model ACL, budget & rate limit
   -> meneruskan ke OpenAI; usage/cost tercatat
```

**Pengujian menggunakan master key hanya di sisi operator** saat membuat key; request client selalu menggunakan virtual key. Untuk key pribadi, kaitkan `user_id` secara eksplisit; pada key untuk team, pertimbangkan inheritance dan semantics budget team pada versi LiteLLM. Hindari key generik bersama banyak orang bila ingin per-user attribution.

### 5.5 Contoh API smoke test (setelah gateway berjalan)

```bash
# Jangan jalankan tanpa env yang aman.
# 1. Operator: cek dua ID terhadap credential OpenAI yang akan dipakai.
curl -fsS https://api.openai.com/v1/models/gpt-5.6-terra \
  -H "Authorization: Bearer $OPENAI_API_KEY"
curl -fsS https://api.openai.com/v1/models/gpt-5.6-sol \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# 2. Operator: cek gateway, bukan bukti provider/DB fully working.
curl -fsS http://127.0.0.1:4000/health/readiness

# 3. Developer: uji alias hanya dengan VIRTUAL KEY yang scoped.
curl -fsS http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_VIRTUAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"company-fast","messages":[{"role":"user","content":"Reply with OK"}]}'
```

**Catatan pengamanan:** jangan menyetel `set -x`, jangan menampilkan credential dalam output terminal/demo/log, batasi history, dan verifikasi bahwa test `model not allowed`, invalid/revoked key, serta budget benar-benar menghasilkan penolakan. HTTP readiness saja tidak membuktikan enforcement budget atau kesehatan provider.

---

## 6. Security, privacy, financial controls: default non-negotiable

1. **Secrets:** separate secrets `OPENAI_API_KEY`, `LITELLM_MASTER_KEY`, virtual keys per user, DB credentials; jangan tersimpan di repository atau user-facing config. Rotasi/revokasi dengan prosedur audit.
2. **Isolation:** bind DB private, tidak expose DB/Redis ke publik, HTTPS untuk akses lintas mesin, admin API/UI hanya admin/private access, minimize network egress/ingress.
3. **ACL:** default deny. Key user dapat akses tepat model yang diizinkan; tidak ada master key untuk client. Uji key `company-fast` tidak bisa memanggil `company-coding`.
4. **Budget:** budget LiteLLM membutuhkan PostgreSQL agar enforced. Konfigurasi budget tidak sama dengan proof: uji limit tercapai dan diblok; catat penanganan outage DB / fail-open/fail-closed menurut versi, cache, dan konfigurasi; set **provider-side project spend cap** sebagai lapisan batas tambahan bila tersedia.
5. **Costs:** jangan menganggap cost tracking akurat sebelum model pricing/version mapping divalidasi; periksa token usage dan perbandingan dengan OpenAI usage/billing. Tetapkan budget user/team setelah pilot usage terukur.
6. **Logs:** default tidak menyimpan raw prompt/response, source code, secret, atau PII. Jika observability membutuhkan content capture, minta approval data governance, retention, redaction, access control dan lokasi data.
7. **SSO:** saat Phase 2, disable akun SSO **tidak otomatis** mencabut virtual key lama; harus ada provisioning/deprovisioning/revocation dan uji end-to-end.
8. **Licensing:** cek LiteLLM fitur vs OSS/enterprise dan license; jangan membangun roadmap yang bertumpu pada fitur berlisensi tanpa review.
9. **Continuity:** back up database berisi key metadata/spend, lakukan restore drill sebelum production. Jangan menyalin secret/dump mentah ke dokumen chat.
10. **Provider additions:** penambahan provider wajib mengevaluasi security/data residency, contractual handling, harga, compatibility, fallback behavior, token accounting, dan risiko per user/team.

---

## 7. Definition of Done dan prinsip test

Task hanya **DONE** bila: code/config ada di commit/PR; review selesai sesuai policy; test relevan dapat diulang; hasil aktual dicatat (timestamp, environment, command, outcome); docs/progress diupdate. Tidak boleh menandai DONE hanya karena file dibuat atau contoh command ditulis.

**Lapisan pengujian:**
- **Static:** format YAML/JSON, lint, schema sanity, secret scan, license/dependency scan.
- **Integration:** Compose ↔ LiteLLM ↔ PostgreSQL ↔ OpenAI API dengan test credential yang aman.
- **Functional:** kedua alias, response, streaming, tools, latensi, usage/cost, negative tests.
- **Security:** invalid/revoked key, wrong-model deny, no master key in client, no leaked secrets, team budget scope.
- **Operasional:** restart persistence, graceful provider failure, restore/rollback pada staging.

Untuk tes biaya, gunakan prompt kecil dan budget pilot rendah; tes deny/limit sebaiknya tidak menghabiskan biaya besar. Untuk automatic CI tanpa akses OpenAI, jalankan mock contract tests, lalu pisahkan smoke live terkontrol bercredential tersimpan aman.

---

## 8. Roadmap Phase 1 — Urutan pengerjaan yang harus diikuti

**Goal:** developer bisa menjalankan OpenCode memakai dua logical model secara aman, terkontrol per pengguna, dan tercatat pemakaiannya.

| ID | Urutan & deliverable | Repo | Acceptance minimal | Status |
|---|---|---|---|---|
| **P1-00** | Konfirmasi environment, repo private, owner, API project/billing OpenAI, akses model | docs/config | 2 model ID bisa di-call dengan akun API; keputusan unresolved dicatat | TODO |
| **P1-01** | Siapkan root `company-ai-platform/`, simpan master context di root, inisialisasi 3 repo komponen beserta README, `.gitignore`, PR template/branch protection; gunakan submodule bila root juga Git repo | root + ketiga repo | Root context terlacak di Git yang tepat; repo & CI skeleton tersedia | TODO |
| **P1-02** | Setup Docker Compose: PostgreSQL + LiteLLM; network/volumes | infra | Service start; DB persisted; port tidak public by default | TODO |
| **P1-03** | Secrets & env bootstrap, pin release LiteLLM, health probes | infra | Secret tidak tercetak/ter-commit; readiness test | TODO |
| **P1-04** | Konfigurasi `company-fast` → Terra | config | Live inference via gateway dengan credential operator | TODO |
| **P1-05** | Konfigurasi `company-coding` → Sol | config | Live inference; response benar dengan alias | TODO |
| **P1-06** | Model catalog/ACL contract & config validation | config | Hanya 2 alias diekspos; config tervalidasi | TODO |
| **P1-07** | Setup users/teams minimum & virtual keys unik per developer | config/infra | Minimal 2 user/test keys, identity attribution | TODO |
| **P1-08** | Uji model allow/deny, key revocation | e2e | Fast-only key ditolak saat mencoba coding; revoked key 401/deny | TODO |
| **P1-09** | Tetapkan pilot RPM/TPM + budget/duration | config | Limit terdokumentasi & diuji menggunakan Postgres | TODO |
| **P1-10** | Uji spend/cost/token tracking | e2e | Usage per user/key/alias terbaca & diperiksa | TODO |
| **P1-11** | Konfigurasi OpenCode custom provider + onboarding guide | config | Developer menjalankan kedua alias melalui virtual key | TODO |
| **P1-12** | Test streaming + tool calling + coding workflow | e2e | Agent coding workflow jalan; kegagalan tercatat jelas | TODO |
| **P1-13** | Negative tests: invalid key, denied model, budget exceeded, provider 429/5xx | e2e | Auth/ACL fail closed sesuai ekspektasi; error jelas | TODO |
| **P1-14** | CI lint/scan/tests, smoke staging dan version lock | ketiganya | PR checks hijau; staging reproducible | TODO |
| **P1-15** | Security baseline, logging minimization, restart persistence | infra/config/e2e | TLS untuk shared access; secrets aman; DB persist | TODO |
| **P1-16** | Runbook: deploy, rollback, rotate key, incident, backup awal | infra/config | Engineer lain bisa re-deploy dari README | TODO |
| **P1-17** | Pilot 2–5 developer + usage/cost feedback | docs/e2e | Bukti pemakaian, budget and access tests, issues logged | TODO |
| **P1-18** | Review Phase 1 gate dan tag release | semua | Checklist release terpenuhi, owners menyetujui | TODO |

**Dependencies:** `P1-00 → P1-01 → P1-02/P1-03 → P1-04/P1-05 → P1-07 → P1-08/P1-09/P1-10 → P1-11/P1-12/P1-13 → P1-14..18`. Boleh menulis tests lebih awal; urutan di atas adalah prioritas penyelesaian, bukan larangan kerja paralel.

**Phase 1 EXIT GATE:**

- [ ] OpenAI API access Terra dan Sol terbukti dengan credential yang akan digunakan.
- [ ] Gateway berjalan dengan PostgreSQL persisten dan secret terisolasi.
- [ ] `/v1/chat/completions` sukses untuk **kedua** alias menggunakan virtual key.
- [ ] OpenCode bekerja untuk basic chat, streaming, tool call/coding (atau keterbatasan terdokumentasi dan disetujui).
- [ ] Per-user attribution, allowed models, revocation, rate limit, budget, spend tercatat dan diuji termasuk negative cases.
- [ ] Tidak ada plaintext secret di Git/log; TLS untuk tim; staging + runbook + smoke CI tersedia.
- [ ] Release tag + daftar image/config refs + bukti pengujian + sign-off.

---

## 9. Roadmap Phase 2 — Control Plane

**Goal:** admin/team lead mengelola akses tanpa mengedit konfigurasi manual, dengan konsistensi policy dan audit yang bisa diperiksa.

| ID | Task | Output + syarat acceptance | Status |
|---|---|---|---|
| P2-00 | Finalisasi stack, IdP SSO, RBAC, schema, licensing | ADR + API contract + desain lifecycle | TODO |
| P2-01 | Bootstrap `llm-control-plane` + migrasi DB milik app | API skeleton, health/test/CI, DB terpisah secara logis dari schema internal LiteLLM | TODO |
| P2-02 | SSO/OIDC + session/token auth admin | Login/logout, authorization backend, role tests | TODO |
| P2-03 | Users/teams + membership sync dari IdP | Mapping stable identifiers, lifecycle join/leave | TODO |
| P2-04 | Model catalog logical + upstream deployments | CRUD/approval + alias tetap; no direct provider key exposure | TODO |
| P2-05 | Policy model ACL + rule precedence & default deny | Enforcement end-to-end di LiteLLM, negative tests | TODO |
| P2-06 | Key create/revoke/self-service + scoped permission | Raw key shown securely once; no plaintext DB storage | TODO |
| P2-07 | Budget & RPM/TPM management, user vs team semantics | Enforcement tested; admin controls | TODO |
| P2-08 | Usage/cost API + data reconciliation | Per-user/team/model rollup, source-of-truth semantics | TODO |
| P2-09 | Admin portal workflow (users, teams, models, keys, costs) | No master key in browser; accessible UI | TODO |
| P2-10 | Audit logs immutable-ish/access restricted | Actor/action/time/old-new/ref; sensitive values redacted | TODO |
| P2-11 | Reconciler drift detection + retry/idempotency | Control Plane desired policy → LiteLLM actual policy, clear ownership | TODO |
| P2-12 | Deprovisioning and operations acceptance | Disable IdP → revoke all relevant keys and deny traffic, rollback & tests | TODO |

**Aturan data ownership:**
- Phase 1: konfigurasi Git + LiteLLM DB/APIs adalah source of truth *operasional*.
- Phase 2: tetapkan satu **desired state owner** per domain (contoh: catalog/config Git atau Control Plane DB — **pilih salah satu sebagai writer**). Control Plane mengeksekusi via adapter LiteLLM APIs; jangan edit tabel internal LiteLLM secara langsung.
- Data user/team app dan audit punya schema yang dikelola app, bukan memodifikasi tabel milik LiteLLM secara manual.
- Buat rekonsiliasi idempotent, deteksi drift, version/approval workflow, rollback, serta aturan migrasi policy tanpa downtime.

**Phase 2 EXIT GATE:** end user self-service key scoped; admin bisa mengatur user/team/model/budget; disable user efektif menghilangkan akses; audit dan reconciliation dapat diuji; tidak ada privilege escalation via UI/backend.

---

## 10. Roadmap Phase 3 — Production/Enterprise

Prioritas dikendalikan risiko dan beban aktual, **bukan** sekadar daftar tool.

| ID | Task | Acceptance | Status |
|---|---|---|---|
| P3-00 | Threat model & security review | Threats, mitigation owner, data handling & risk register | TODO |
| P3-01 | API gateway/WAF/network policy, private endpoints | Auth path aman, TLS, IP policy, admin isolation | TODO |
| P3-02 | Secret manager + rotation policy | No manual key copy, rotation tested | TODO |
| P3-03 | Metrics, structured logs, traces/usage dashboard | SLO dashboards latency/error/cost; prompt contents protected | TODO |
| P3-04 | HA LiteLLM replicas + Postgres/Redis strategy | Failover test, consistent auth/budget policy; documented caveats | TODO |
| P3-05 | Backups, restore drills, incident runbook & DR | RPO/RTO agreed and tested; secrets lifecycle included | TODO |
| P3-06 | Guardrails/data classification/redaction | Policy-specific tests, latency and false positive review | TODO |
| P3-07 | Load/performance & chaos tests | Defined SLO under load; provider 429/backoff behavior | TODO |
| P3-08 | Provider expansion mechanism (*if approved*) | Adapter, contract, pricing, data governance, tests, ADR | TODO |
| P3-09 | Production readiness/sign-off | Operational handover, SLO, on-call, rollback, costs | TODO |

**Bila menambah provider di masa depan:** tambahkan deployment di belakang logical alias atau buat alias baru setelah approval. Verifikasi per-model kompatibilitas tools/streaming/context/pricing. Jangan fallback otomatis ke provider lain yang berbeda kebijakan data residency atau keamanan. Ketika tidak ada provider cadangan, **fail transparently** alih-alih klaim high availability yang tidak nyata.

---

## 11. Operating procedures minimum

### 11.1 Deploy

1. Ambil commit SHA/tag yang kompatibel dari `release/versions.lock`.
2. Pastikan secrets berasal dari secret store/local secure env dan tersedia untuk target service.
3. Jalankan config validation dan compose lint; cek DB backup/migration kompatibilitas.
4. Deploy ke dev/staging dengan image pinned, jalankan health lalu live smoke dengan scoped test key.
5. Tes negative ACL, budget, 2 model aliases, streaming/tools, spend records.
6. Promote dengan approval; catat operator, waktu, version, hasil, rollback ref.

### 11.2 Rollback

1. Hentikan promote, catat symptom dan blast radius.
2. Rollback image + config **sebagai pasangan** memakai compatible refs; evaluasi backward compatibility DB migration sebelum melakukan rollback schema.
3. Ulangi health, auth negative tests, dan model smoke.
4. Catat incident/ADR bila memengaruhi keputusan desain.

### 11.3 Key lifecycle

Issue → securely deliver → scoped models/budget → monitor spend → rotate/revoke → audit. Master key dipakai hanya oleh operator/admin/Control Plane service dengan akses aman, bukan user workstation. Simpan cara revokasi saat IdP user disable.

### 11.4 Minimal observability schema

`request_id`, `timestamp`, `user_id/pseudonym`, `team_id`, `key_id/hash`, `requested_alias`, `actual_upstream_model`, `provider`, `input_tokens`, `output_tokens`, `cost_estimate`, `duration_ms`, `status_code`, `error_type`, `trace_id`. Jangan kirim secret/raw user prompt ke logs default. Validasi ketersediaan field aktual dari LiteLLM callback/version.

---

## 12. Risiko, asumsi, dan open questions

| ID | Risiko/pertanyaan | Penanganan atau pemilik keputusan | Status |
|---|---|---|---|
| R-01 | API key perusahaan tidak memiliki akses ke Terra/Sol | P1-00: direct OpenAI API test & call; jangan silent substitute | OPEN |
| R-02 | Chat Completions/OpenCode tools tidak kompatibel penuh | P1-12: test tool/stream; adapt Responses route bila perlu | OPEN |
| R-03 | Biaya melonjak karena penggunaan model coding | P1-09/P1-10: budget + rate limit + OpenAI-side cap/alerts | OPEN |
| R-04 | DB outage menyebabkan key/budget behavior tak sesuai harapan | P1-13/P3-04: verify outage semantics on pinned version; defense in depth | OPEN |
| R-05 | Per-user dan per-team budget saling bertabrakan | P1-07/P1-09: verifikasi LiteLLM ownership/inheritance | OPEN |
| R-06 | Config Git dan Admin UI/API berlomba menjadi source of truth | P2-11: ownership + reconciliation design | OPEN |
| R-07 | SSO disable tidak revoke API key lama | P2-12: deprovision job + revocation E2E | OPEN |
| R-08 | LiteLLM OSS/enterprise feature mismatch | P1-00/P2-00: license matrix dan biaya | OPEN |
| R-09 | Siapa owner Git, platform, security, OpenAI billing? | Project sponsor menunjuk PIC | OPEN |
| R-10 | Infrastruktur final, domain, IdP, region, compliance? | Decision di P1-00/P2-00/P3-00 | OPEN |

**Data untuk dikonfirmasi tanpa menghambat pemahaman dokumen:** nama domain internal; target Docker VM/K8s/cloud; jumlah user; tim/role; anggaran pilot; lokasi data; identity provider; security posture; ownership cost center. Semua **UNDECIDED** dan tidak boleh ditebak sebagai fakta.

---

## 13. Referensi resmi dan kebijakan verifikasi

Periksa ulang saat implementasi karena detail dan fitur bisa berubah sesuai versi:

- OpenAI GPT-5.6 Terra: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- OpenAI GPT-5.6 Sol: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- OpenAI API model migration/guidance: https://developers.openai.com/api/docs/guides/latest-model
- LiteLLM Docker quickstart: https://docs.litellm.ai/docs/proxy/docker_quick_start
- LiteLLM Virtual Keys: https://docs.litellm.ai/docs/proxy/virtual_keys
- LiteLLM Budgets & Rate Limits: https://docs.litellm.ai/docs/proxy/users
- LiteLLM production deploy: https://docs.litellm.ai/docs/proxy/deploy
- OpenCode custom provider: https://opencode.ai/docs/providers/

**Fakta yang sudah diverifikasi dari dokumentasi publik per baseline:** Terra dan Sol adalah model IDs API OpenAI; LiteLLM memakai `model_list`, `model_name`, `litellm_params`, env secret, PostgreSQL untuk virtual keys/budget; OpenCode mendukung custom OpenAI-compatible provider. **Belum diverifikasi:** project-level OpenAI API permission, aktual LiteLLM version/config/runtime, dan hasil tes per-user.

---

## 14. CURRENT STATE — HARUS DIPERBARUI SETIAP SESI

> **Snapshot awal 2026-10-10. Semua status di bawah berasal dari percakapan perencanaan, bukan dari inspeksi Git/infra nyata.**

```yaml
project_name: internal-llm-gateway
canonical_document: company-ai-platform/PROJECT_MASTER_CONTEXT.md
context_version: 1.0.0
last_context_update: 2026-10-10
phase: 1
execution_state: PLANNING
last_completed_task: null
active_task: P1-00
next_action: "Konfirmasi environment dan akses dua model OpenAI API; lalu bootstrap tiga repo."
provider_scope_phase_1: [openai]
model_aliases:
  company-fast: openai/gpt-5.6-terra
  company-coding: openai/gpt-5.6-sol
repositories:
  llm-gateway-infra: NOT_CREATED_OR_NOT_VERIFIED
  llm-gateway-config: NOT_CREATED_OR_NOT_VERIFIED
  llm-gateway-e2e: NOT_CREATED_OR_NOT_VERIFIED
  llm-control-plane: FUTURE_PHASE_2
  llm-admin-portal: FUTURE_PHASE_2
runtime:
  litellm_version: UNKNOWN
  litellm_deployed: NOT_VERIFIED
  postgres_deployed: NOT_VERIFIED
  redis_deployed: NOT_VERIFIED
  opencode_connected: NOT_VERIFIED
api_access:
  gpt-5.6-terra: NOT_TESTED
  gpt-5.6-sol: NOT_TESTED
ci_e2e: NOT_VERIFIED
blocking_issues: []
latest_commit_refs: {}
```

**Enum rekomendasi status:** `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE_VERIFIED`, `SKIPPED_APPROVED`; jangan gunakan `DONE` tanpa bukti. Saat memperbarui, ganti status task terkait di §8/9/10, dan tambahkan baris log baru di §15. Jika bukti status tidak ada setelah pindah chat, tulis `NOT_VERIFIED` dan inspeksi Git/CI.

---

## 15. WORK LOG & HANDOFF — TUMBUH SEIRING PENGERJAAN

> Entri pertama adalah baseline konteks, **bukan** hasil coding.

| Tanggal | Task ID | Aksi / hasil | Bukti (PR/commit/test) | Status | Next |
|---|---|---|---|---|---|
| 2026-10-10 | BASELINE | Rancangan Phase 1–3 dan provider OpenAI-only dengan 2 alias disepakati; master context dibuat | Percakapan perencanaan, belum ada Git/tes | PLAN_ONLY | P1-00 |
| 2026-10-10 | DOC-LOCATION | Lokasi kanonik master context disesuaikan menjadi `company-ai-platform/PROJECT_MASTER_CONTEXT.md` | File Markdown disiapkan pada path tersebut; status Git remote/commit belum diverifikasi | DOCUMENT_UPDATED | P1-00 |

### Template log setiap sesi (copy & isi)

```text
Date/time & timezone:
Agent/model or engineer:
Task ID:
Before (commit/ref, environment):
Files changed:
Actual work performed:
Commands/tests executed:
Actual outcomes (pass/fail + logs location; no secrets):
Artifacts / PR / commit SHA:
Decision/ADR changed? (yes/no + link):
Known failures/blockers:
Current status (TODO / IN_PROGRESS / BLOCKED / DONE_VERIFIED):
Exact next action (single task):
```

### Handoff ke sesi baru

1. Lampirkan file ini **versi terbaru dari Git** ke chat/model baru.
2. Sertakan URL repository/branch dan commit SHA terbaru (root `company-ai-platform` serta repo komponen terkait) jika punya akses.
3. Minta agent membaca §0, §2, §14, §15 lalu verifikasi kode aktual sebelum melanjutkan.
4. Agent menyelesaikan satu task prioritas dan mengirim hasil **yang bisa direproduksi**.
5. Commit pembaruan status ke dokumen kanonik pada **root `company-ai-platform/PROJECT_MASTER_CONTEXT.md`**. Jika repo komponen terpisah, tautkan PR/commit komponen pada PR root atau work log; jangan membuat versi alternatif master context di file lain.

### Stop conditions — kapan agent harus bertanya, bukan menebak

- Perubahan provider Phase 1, logical alias, atau target upstream model.
- Credential akses OpenAI tidak tersedia / model API denied / quota/billing failure.
- Perlu menggunakan master key di client, menyimpan secret di Git, atau mematikan ACL/budget demi mempercepat demo.
- Keputusan lisensi/commercial upgrade, procurement, domain publik, data residency, compliance.
- Perubahan yang bisa menimbulkan kehilangan data atau memerlukan migrasi irreversibel.
- Konflik serius antara progres dokumen dan fakta repository/staging.

---

## 16. Checklist sebelum memulai coding sesi pertama

- [ ] Project owner menyetujui scope **OpenAI-only Phase 1** dan kedua mapping model.
- [ ] Orang yang berwenang menyediakan OpenAI API project/key/billing **tanpa mengirim key ke chat**.
- [ ] Validasi direct API kedua model (status code, biaya kecil, kemampuan tools jika dibutuhkan).
- [ ] Tentukan Git hosting/organization, akses reviewer, dan cara root `company-ai-platform/` melacak subrepo (disarankan Git submodules bila root adalah Git repo).
- [ ] Tentukan tempat development pertama (local Docker / VM) dan batas network security.
- [ ] Letakkan dokumen ini sebagai `company-ai-platform/PROJECT_MASTER_CONTEXT.md` (**langsung di root**, bukan di folder config).
- [ ] Pilih versi LiteLLM stabil lalu pin; validasi sintaks config dan capabilities nyata.
- [ ] Mulai task `P1-00`, catat hasil aktual di §14 dan §15.

**Prinsip akhir:** *Keep client contract stable; keep provider replaceable; keep permissions testable; keep secrets out of Git; keep project state explicit.*
