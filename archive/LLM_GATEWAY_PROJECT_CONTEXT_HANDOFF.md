> **ARSIP — jangan gunakan sebagai current state atau instruksi bootstrap.**
> Mulai dari [README](../README.md) dan [master aktif](../MASTER_CONTEXT.md).
> Tautan dipindahkan sesuai lokasi baru; checksum historis merujuk snapshot sebelum relokasi.

> **Navigasi konsolidasi — 2026-10-10:** file ini adalah **arsip detail checkpoint H1–H10D**.
> Master aktif: [PROJECT_CONTEXT_MASTER.md](../MASTER_CONTEXT.md); status acceptance: [Phase 1](../architecture/phase-1.md).
> H10D selesai lokal **bukan** penutupan seluruh Phase 1 rancangan awal. Struktur staging dan hitungan tes lama yang masih terselip di bawah adalah riwayat.
> Baca [evaluasi drift](../adr/README.md) sebelum coding; usulan major belum disetujui. Tubuh arsip dipertahankan.

# LLM Gateway Project Context Handoff

> Gunakan file ini sebagai **single source of context** ketika melanjutkan project di chat baru.
> Tujuannya adalah meminimalkan *lost in the middle*, mencegah perubahan arsitektur yang tidak disengaja, dan menjaga assistant tetap mengikuti plan yang sudah disepakati.

## Checkpoint terbaru — 2026-10-10, H10D lokal selesai

- **Instruksi terbaru user mengalahkan rencana staging lama:** gunakan Docker existing port **4000**, jangan buat environment/container baru. Compose staging dan script/dokumentasinya dihapus. Tidak ada container staging; sisa data/secrets staging lama tidak digunakan dan tidak dihapus destruktif.
- **H10B–H10D implementasi/verifikasi lokal COMPLETE.** Release config nyata (timeout 180→181) dan rollback ke byte semula PASS; ID ketiga container/image sama. Runbook release, backup, lifecycle, incident, pilot dan checklist server selesai.
- **H1–H10 cross-check:** infra 7/7 (12 tes operasional), config 6/6, E2E 8/8; **22 unit + 3 smoke + 12 live = 37 PASS**, OpenCode PASS, backup/restore 83 tabel identik, outage/recovery Redis/PostgreSQL PASS.
- Bug/celah diperbaiki: readiness HTTP palsu saat dependency mati, izin `.env` 644→600, folder kosong bernama YAML, benturan `SCRIPT_DIR`, validasi argumen onboarding, guard/checksum restore, scan secret working tree. Ditambahkan tes tool calling kedua alias.
- **Security scan PASS sesuai baseline existing, bukan zero vulnerabilities:** LiteLLM 0 Critical/0 High, PostgreSQL 1 Critical/28 High, Redis 0 Critical/2 High. Baseline tidak dinaikkan. Review sebelum go-live. Gitleaks dan audit Python ketiga repo PASS.
- **H7 merge gate GitHub sudah dikonfirmasi user sebelumnya.** Commit/push perubahan ini dan CI remote belum dilakukan. Tidak ada deploy server.
- **Batasan tetap:** offboarding perlu freeze/serialisasi provisioning; tidak ada locking otomatis. Rollback teruji hanya config pada image/schema sama. Restore test DB di PostgreSQL existing, bukan boot gateway baru terhadap DB restore.
- Laporan utama: `reports/PHASE1_H1_H10_REPORT.md`; kode lengkap: `reports/PHASE1_CODE_APPENDIX.md`; bukti: `reports/phase1-evidence/`.
- NEXT: persiapan candidate commit/CI dan server berdasarkan checklist; TLS/firewall, backup terenkripsi luar host, PIC/budget dan review keamanan belum dipenuhi hanya oleh pengujian lokal ini.

---

# 1. Cara Melanjutkan Project Ini

## Gaya kerja yang diinginkan
- Bahasa: **Indonesia**
- Gaya: teknikal, langsung, step-by-step, incremental
- Jangan lompat beberapa fase sekaligus.
- Selalu berikan checkpoint/DoD sebelum lanjut.
- Jangan meminta user menempelkan secret.
- Jangan mengubah abstraction atau struktur yang sudah terbukti bekerja tanpa alasan kuat.
- Kalau ada kode existing, **ikuti interface existing**, jangan membuat layer baru hanya agar snippet assistant cocok.
- Utamakan test kecil → verifikasi → baru lanjut.
- Untuk perubahan yang berisiko, berikan negative test.
- Jangan menganggap suatu tahap selesai jika belum ada hasil test/output yang membuktikannya.

## Prinsip arsitektur E2E yang harus dipertahankan

```text
tests/client.py
    ↓
semua komunikasi HTTP / LiteLLM client behavior

tests/conftest.py
    ↓
fixture + provisioning + lifecycle + cleanup

tests/test_*.py
    ↓
behavior assertions
```

Jangan:
- membuat HTTP abstraction kedua,
- membuat `AdminLiteLLMClient`,
- memakai `requests.post()` langsung di test bila bisa lewat `LiteLLMClient`,
- menambah helper yang menduplikasi pola existing.

---

# 2. Tujuan Project

Membangun internal LLM gateway perusahaan:

```text
Developer
   │
   ▼
OpenCode
   │
   ▼
LiteLLM Proxy
   │
   ├── Virtual Keys
   ├── Team/User policy
   ├── Budget / RPM / TPM enforcement
   ├── PostgreSQL
   └── Redis
          │
          ▼
       OpenAI
```

Provider awal:
- OpenAI

Provider masa depan:
- Anthropic
- Google
- provider lain

Developer **tidak boleh** menggunakan provider API key secara langsung.

Developer menggunakan:
- LiteLLM Virtual Key
- logical model alias

Master key:
- hanya admin/provisioning

Provider secret:
- hanya server-side

---

# 3. Logical Model Alias

Current logical aliases:

```text
company-fast
  → openai/gpt-5.6-terra

company-coding
  → openai/gpt-5.6-sol
```

Tujuan:
- developer hanya tahu logical alias,
- provider/model backend bisa diganti tanpa mengubah client,
- future Anthropic/Google bisa dipasang di belakang alias yang sama.

---

# 4. Repository Layout

```text
company-ai-platform/
├── llm-gateway-infra/
├── llm-gateway-config/
└── llm-gateway-e2e/
```

## `llm-gateway-infra`

Relevant structure:

```text
llm-gateway-infra/
├── docker-compose.yml
├── docker-compose.dev.yml
├── .env
├── .env.example
├── .github/
│   ├── fixtures/
│   │   └── litellm_config.yaml
│   └── workflows/
├── scripts/
│   ├── requirements.txt
│   ├── up.sh
│   ├── reset.sh
│   ├── health/
│   │   ├── liveness.sh
│   │   ├── readiness.sh
│   │   ├── dependencies.sh
│   │   ├── functional.sh
│   │   └── check-all.sh
│   ├── backup/
│   │   ├── backup-postgres.sh
│   │   ├── verify-backup.sh
│   │   ├── restore-postgres-test.sh
│   │   ├── check-restore.sh
│   │   └── drill.sh
│   ├── ci/
│   │   ├── validate-compose.py
│   │   ├── validate-env-example.py
│   │   ├── validate-staging.py
│   │   └── validate.sh
│   ├── staging/
│   │   ├── init.sh
│   │   ├── compose.sh
│   │   └── verify.sh
│   └── security/
│       ├── scan-secrets.sh
│       ├── audit-python.sh
│       ├── scan-containers.sh
│       ├── container-high-baseline.json
│       └── check-all.sh
```

## `llm-gateway-config`

```text
llm-gateway-config/
├── config/
│   └── litellm_config.yaml
├── models/
│   ├── company-fast.yaml
│   └── company-coding.yaml
├── providers/
│   └── openai.yaml
├── policies/
│   └── teams/
│       ├── default.yaml
│       ├── engineering.yaml
│       └── healthcheck.yaml
├── clients/
│   └── opencode/
│       └── opencode.jsonc
├── docs/
│   ├── model-catalog.md
│   └── compatibility.md
├── scripts/
│   ├── ci/
│   └── security/
└── .github/
    └── workflows/
```

Important:
- file `models/*.yaml` **tidak memakai field `logical_name`**
- H6 validator sudah diperbaiki agar logical model ID berasal dari **filename stem**
- jangan reintroduce assumption `logical_name`

## `llm-gateway-e2e`

```text
llm-gateway-e2e/
├── requirements.txt
├── pytest.ini
├── scripts/
│   ├── run-smoke.sh
│   ├── run-unit.sh
│   ├── run-live.sh
│   ├── run-all.sh
│   ├── run-limits.sh
│   ├── test-opencode.sh
│   ├── ci/
│   │   ├── validate-suite.py
│   │   └── validate.sh
│   └── security/
│       ├── scan-secrets.sh
│       ├── audit-python.sh
│       └── check-all.sh
└── tests/
    ├── client.py
    ├── conftest.py
    ├── test_health.py
    ├── test_models.py
    ├── test_auth.py
    ├── test_inference.py
    ├── test_policy.py
    ├── test_spend.py
    ├── test_limits.py
    ├── test_lifecycle.py
    └── unit/
        ├── conftest.py
        ├── test_offboarding_client.py
        ├── test_history_retention.py
        └── test_suite_validator.py
```

---

# 5. Runtime LiteLLM Config

Current concept:

```yaml
model_list:
  - model_name: company-fast
    litellm_params:
      model: openai/gpt-5.6-terra
      api_key: os.environ/OPENAI_API_KEY
      timeout: 120

  - model_name: company-coding
    litellm_params:
      model: openai/gpt-5.6-sol
      api_key: os.environ/OPENAI_API_KEY
      timeout: 180

litellm_settings:
  num_retries: 2
  request_timeout: 180
  set_verbose: false
  json_logs: true

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
```

---

# 6. `.env.example`

Current variables:

```env
LITELLM_BASE_URL=http://localhost:4000
LITELLM_MASTER_KEY=
LITELLM_SALT_KEY=

POSTGRES_DB=litellm
POSTGRES_USER=litellm
POSTGRES_PASSWORD=
DATABASE_URL=

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

OPENAI_API_KEY=

LLM_GATEWAY_CONFIG_DIR=../llm-gateway-config
LITELLM_CONFIG_PATH=../llm-gateway-config/config/litellm_config.yaml

HEALTHCHECK_API_KEY=
```

Important:
- local `.env` real secrets tidak masuk Git
- permission local `.env` pernah diperketat
- jangan meminta user paste isi secret

---

# 7. OpenCode Integration

Working config concept:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "company-ai/company-coding",
  "providers": {
    "company-ai": {
      "name": "Company AI Gateway",
      "env": ["COMPANY_LLM_API_KEY"],
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "http://localhost:4000/v1"
      },
      "models": {
        "company-fast": {
          "name": "Company Fast",
          "modelID": "company-fast",
          "capabilities": {
            "tools": true,
            "input": ["text"],
            "output": ["text"]
          }
        },
        "company-coding": {
          "name": "Company Coding",
          "modelID": "company-coding",
          "capabilities": {
            "tools": true,
            "input": ["text"],
            "output": ["text"]
          }
        }
      }
    }
  }
}
```

Working behavior:
- chat via OpenCode works
- tool calling works
- developer uses `COMPANY_LLM_API_KEY`
- developer does not know `OPENAI_API_KEY`

---

# 8. Team Policies

## Engineering

```yaml
name: engineering
description: LLM policy for engineering and software development teams.

models:
  - company-fast
  - company-coding

limits:
  team:
    monthly_budget_usd: 100
    rpm: 60
    tpm: 200000

  member:
    monthly_budget_usd: 20
```

## Default

```yaml
name: default
description: Default policy for internal LLM users.

models:
  - company-fast

limits:
  team:
    monthly_budget_usd: 10
    rpm: 30
    tpm: 100000

  member:
    monthly_budget_usd: 2
```

## Healthcheck

```yaml
name: healthcheck
description: Service account policy for gateway health checks.

models:
  - company-fast
  - company-coding

limits:
  team:
    monthly_budget_usd: 1
    rpm: 10
    tpm: 10000

  member:
    monthly_budget_usd: 1
```

---

# 9. Provisioning Principles

User creation:

```json
{
  "auto_create_key": false
}
```

Virtual keys:
- models = `["all-team-models"]`
- team policy menentukan model access / budget / RPM / TPM
- key tidak perlu rotate ketika team policy berubah

Working behavior yang sudah dibuktikan:

```text
same key
  ↓
company-coding allowed
  ↓
team policy changed
  ↓
company-coding → 403
  ↓
policy restored
  ↓
company-coding → 200
```

---

# 10. E2E Client Architecture

Current `tests/client.py`:

```python
from __future__ import annotations

from typing import Any

import requests


class LiteLLMClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 60,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        stream: bool = False,
    ) -> requests.Response:
        return requests.post(
            f"{self.base_url}{path}",
            headers=self.headers,
            json=json,
            stream=stream,
            timeout=self.timeout,
        )

    def expect_json(
        self,
        response: requests.Response,
        expected_status: int = 200,
    ) -> dict[str, Any]:
        if response.status_code != expected_status:
            raise AssertionError(
                f"Expected HTTP {expected_status}, "
                f"got {response.status_code}\n"
                f"Response: {response.text}"
            )

        return response.json()
```

`create_team()` sudah ditambahkan sebagai method pada object yang sama.

Current intended form:

```python
def create_team(
    self,
    *,
    team_alias: str,
    models: list[str],
    rpm_limit: int | None = None,
    tpm_limit: int | None = None,
    max_budget: float | None = None,
    budget_duration: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "team_alias": team_alias,
        "models": models,
    }

    if rpm_limit is not None:
        payload["rpm_limit"] = rpm_limit

    if tpm_limit is not None:
        payload["tpm_limit"] = tpm_limit

    if max_budget is not None:
        payload["max_budget"] = max_budget

    if budget_duration is not None:
        payload["budget_duration"] = budget_duration

    response = self.post(
        "/team/new",
        json=payload,
    )

    data = self.expect_json(
        response,
        expected_status=200,
    )

    team_id = data.get("team_id")

    if not team_id:
        raise AssertionError(
            "LiteLLM /team/new response "
            "does not contain team_id.\n"
            f"Response: {data}"
        )

    if rpm_limit is not None:
        actual_rpm = data.get("rpm_limit")

        if actual_rpm != rpm_limit:
            raise AssertionError(
                "Team rpm_limit was not persisted. "
                f"requested={rpm_limit}, "
                f"actual={actual_rpm}"
            )

    if tpm_limit is not None:
        actual_tpm = data.get("tpm_limit")

        if actual_tpm != tpm_limit:
            raise AssertionError(
                "Team tpm_limit was not persisted. "
                f"requested={tpm_limit}, "
                f"actual={actual_tpm}"
            )

    return data
```

Important:
- jangan menambah `admin_post()`
- jangan menambah `admin_headers`
- privilege berasal dari `api_key` pada instance

Example:

```python
admin_client = LiteLLMClient(
    base_url=base_url,
    api_key=master_key,
)
```

User key:

```python
user_client = LiteLLMClient(
    base_url=base_url,
    api_key=virtual_key,
)
```

---

# 11. E2E Fixture Architecture

Current `tests/conftest.py` concept:

```python
@pytest.fixture(scope="session")
def base_url() -> str:
    ...

@pytest.fixture(scope="session")
def master_key() -> str:
    ...

@pytest.fixture(scope="session")
def fast_model() -> str:
    ...

@pytest.fixture(scope="session")
def coding_model() -> str:
    ...

@pytest.fixture(scope="session")
def admin_client(
    base_url: str,
    master_key: str,
) -> LiteLLMClient:
    return LiteLLMClient(
        base_url=base_url,
        api_key=master_key,
    )
```

## Existing `e2e_identity`

Flow:

```text
create user
  ↓
create team
  ↓
add membership
  ↓
create virtual key
  ↓
yield context
  ↓
block key
  ↓
block team
```

Important current fields:

```text
user_id
team_id
team_alias
key_alias
virtual_key
```

Cleanup:
- key diblock
- team dibuat inert/blocked
- jangan print virtual key

## Existing `user_client`

```python
@pytest.fixture()
def user_client(
    base_url: str,
    e2e_identity: dict,
) -> LiteLLMClient:
    return LiteLLMClient(
        base_url=base_url,
        api_key=e2e_identity["virtual_key"],
    )
```

## H8 fixtures

Sudah dibuat:

```text
rpm_limited_identity
rpm_user_client

budget_limited_identity
budget_user_client
```

`rpm_limited_identity`:
- disposable user
- disposable team
- `rpm_limit = 2`
- `tpm_limit = 50000`
- key tidak memiliki RPM/TPM override
- key models = `["all-team-models"]`
- cleanup key/team

`budget_limited_identity`:
- disposable user
- disposable team
- team budget lebih besar
- disposable virtual key dengan tiny budget
- budget test hanya mengisolasi key budget
- cleanup key/team

---

## H9 fixtures dan client methods

Sudah ditambahkan pada arsitektur existing:
- `multi_key_identity`: satu disposable user, satu team, dan dua key untuk `developer-laptop` / `developer-ci`.
- `multi_key_clients`: satu instance `LiteLLMClient` untuk setiap virtual key.
- `LiteLLMClient.list_user_keys_page()` dan `list_user_keys()` untuk discovery dengan pagination dan validasi hasil.
- `LiteLLMClient.offboard_user_keys()` untuk block seluruh key yang ditemukan, dengan pelaporan kegagalan parsial.
- `LiteLLMClient.list_user_spend_logs_page()` untuk satu halaman histori `/spend/logs/v2` dalam rentang waktu tertentu.

Detail implementasi dan review ada di bagian 16.

---

# 12. Current E2E Tests

Current total:

- **19 fungsi tes → 37 kasus pytest** setelah H10: 22 unit, 3 smoke, 12 live; termasuk tool calling kedua alias.
- **22 unit, 3 smoke, 10 live**, termasuk 2 tes lifecycle.
- Marker `unit` memisahkan tes offline; smoke dipilih dengan `not live and not unit`.
- Daftar di bawah memuat 13 fungsi tes gateway. Lima fungsi unit berada di `tests/unit/` dan menghasilkan 22 kasus.

```text
tests/test_auth.py
  test_invalid_key_is_rejected

tests/test_health.py
  test_litellm_is_alive

tests/test_inference.py
  test_company_fast_inference
  test_company_coding_inference
  test_streaming

tests/test_limits.py
  test_team_rpm_limit_is_enforced
  test_key_budget_is_enforced
  test_blocked_key_is_rejected

tests/test_models.py
  test_user_can_see_expected_models

tests/test_lifecycle.py
  test_multiple_user_keys_work_before_offboarding
  test_user_offboarding_blocks_all_keys

tests/test_policy.py
  test_team_policy_changes_without_key_rotation

tests/test_spend.py
  test_spend_is_attributed_to_user
```

---

# 13. E2E Results dan Sumber Bukti

## H10D — hasil final terbaru, 2026-10-10

37 kasus PASS (22 unit + 3 smoke + 12 live), OpenCode PASS, 12 tes operasi infra PASS.
Tool calling pada kedua alias ditambahkan. Bukti lengkap ada di
`reports/phase1-evidence/full-regression-final.txt` dan laporan utama. Hasil H9E di bawah
adalah riwayat checkpoint sebelum penambahan kedua kasus tool calling.


## H9E — Hasil aktual terbaru, 2026-10-10

Environment: gateway lokal `localhost:4000`, Python 3.12.15, pytest 9.0.3, virtual environment bersama workspace. Runner memuat file environment existing tanpa mencetak secret.

| Perintah dari `llm-gateway-e2e` | Hasil aktual |
|---|---|
| `./scripts/run-unit.sh` | 22 passed, 13 deselected |
| `./scripts/ci/validate.sh` | 8/8 tahap PASS; 35 kasus dikoleksi; unit 22 passed |
| `./scripts/run-live.sh tests/test_lifecycle.py --tb=short` | 2 passed in 14.99s |
| `./scripts/run-smoke.sh` | 3 passed, 32 deselected in 0.45s |
| `./scripts/run-live.sh --tb=short` | 10 passed, 25 deselected in 35.95s |

Tes lifecycle lulus sendiri dan saat full live regression. Tidak ada error teardown; fixture menyelesaikan cleanup tanpa melaporkan kegagalan block key/team. `git diff --check` juga PASS.

Percobaan lifecycle pertama di sandbox gagal saat koneksi `/user/new` diblokir (`Operation not permitted`). Setelah izin akses gateway diberikan, lifecycle dijalankan ulang dan PASS. Ini kegagalan akses sandbox, bukan assertion aplikasi yang disembunyikan.

`run-all.sh` kini merangkai unit → smoke → live. Masing-masing runner sudah dijalankan di atas; wrapper tidak dijalankan ulang agar tidak mengulang inference berbayar tanpa kebutuhan baru. Workflow staging remote belum dijalankan.

## Riwayat review sebelum implementasi H9E

Review 2026-10-10:

- `scripts/ci/validate.sh`: seluruh 7 tahap PASS, termasuk ShellCheck, Python syntax, dependency health, suite structure, collection, dan Git safety.
- Pytest collection: **13 tests collected**. Collection tidak menjalankan test behavior atau fixture provisioning.
- 13 skenario simulasi lokal terhadap client: PASS, mencakup pagination normal, penolakan data discovery tidak valid, block sukses, dan penanganan kegagalan parsial.
- Dua batasan direproduksi secara lokal: key yang dibuat setelah discovery dapat terlewat, dan validator masih PASS ketika file lifecycle tidak disertakan. Detail di bagian 16.
- Simulasi bersifat ad hoc selama review, bukan regression test yang disimpan ke repository.
- Pada sesi review awal belum ada request gateway/provider. Kekurangan bukti live tersebut sudah ditutup oleh hasil aktual H9E di atas.

Hasil enforcement, smoke, live, dan validator berikut berasal dari checkpoint **H8 sebelum penambahan H9** dan dipertahankan sebagai riwayat.

## Enforcement

```text
3 passed, 8 deselected

test_team_rpm_limit_is_enforced    PASSED
test_key_budget_is_enforced        PASSED
test_blocked_key_is_rejected       PASSED
```

## Smoke

```text
3 passed, 8 deselected

test_invalid_key_is_rejected       PASSED
test_litellm_is_alive              PASSED
test_user_can_see_expected_models  PASSED
```

## Live

```text
8 passed, 3 deselected

test_company_fast_inference                        PASSED
test_company_coding_inference                      PASSED
test_streaming                                     PASSED
test_team_rpm_limit_is_enforced                    PASSED
test_key_budget_is_enforced                        PASSED
test_blocked_key_is_rejected                       PASSED
test_team_policy_changes_without_key_rotation      PASSED
test_spend_is_attributed_to_user                   PASSED
```

## E2E validator

```text
[1/7] Bash syntax                   PASS
[2/7] ShellCheck                   PASS
[3/7] Python syntax                PASS
[4/7] Python dependency health     PASS
[5/7] Regression suite structure   PASS
[6/7] Pytest collection            PASS
[7/7] Git safety                   PASS

E2E VALIDATION: PASSED
```

---

# 14. H1–H8 Master Status

## H1 — Version Pinning

Completed:
- runtime/container versions pinned
- Python dependencies controlled
- scanner versions pinned
- LiteLLM stable `v1.104.0`

Status:

```text
H1 COMPLETE ✅
```

---

## H2 — Secrets Hardening

Completed:
- real `.env` not committed
- `.env.example` only placeholders
- OpenAI provider key not committed
- master key not committed
- salt key preserved
- verbose disabled
- JSON logs enabled
- local secret file permission tightened
- developer never receives provider secret

Status:

```text
H2 COMPLETE ✅
```

---

## H3 — Network Exposure

Completed:
- PostgreSQL base Compose uses `expose`, not public host port
- Redis base Compose uses `expose`
- internal network `llm-backend`
- dev override binds DB/Redis only to `127.0.0.1`
- LiteLLM remains exposed on port 4000

Status:

```text
H3 COMPLETE ✅
```

---

## H4 — Health & Failure Testing

Scripts:

```text
scripts/health/
├── liveness.sh
├── readiness.sh
├── dependencies.sh
├── functional.sh
└── check-all.sh
```

Completed:
- liveness
- readiness
- dependency checks
- functional inference
- dependency outage/recovery behavior

Status:

```text
H4 COMPLETE ✅
```

---

## H5 — Backup & Restore

Scripts:

```text
scripts/backup/
├── backup-postgres.sh
├── verify-backup.sh
├── restore-postgres-test.sh
├── check-restore.sh
└── drill.sh
```

Completed:
- `pg_dump` custom format
- backup directory protected
- dumps protected
- backup ignored by Git
- `pg_restore --list`
- restore test DB
- table verification
- full drill
- ShellCheck

Status:

```text
H5 COMPLETE ✅
```

---

## H6 — CI / Static Validation

### Config
Completed:
- runtime config validation
- model catalog validation
- logical model derived from filename
- policy validation
- provider validation
- Git safety
- workflow

### Infra
Completed:
- Compose validation
- dev/base Compose validation
- `.env.example`
- ShellCheck
- Git safety
- workflow

### E2E
Completed:
- Bash syntax
- ShellCheck
- Python syntax
- dependency health
- required regression tests
- pytest collection
- marker validation
- Git safety
- workflow

Status:

```text
H6 COMPLETE ✅
```

---

## H7 — Security Scanning

### H7A Secret Scanning
Completed on all three repos:
- Gitleaks `v8.28.0`
- self-test canary
- full Git history
- redaction

Important approach:

```bash
git log -p --all --full-history --no-renames \
 | docker run --rm -i --network=none \
   ghcr.io/gitleaks/gitleaks:v8.28.0 \
   --redact --verbose stdin
```

### H7B Python Dependency Audit
Completed on all three repos:
- temporary venv
- pinned `pip-audit`
- requirements audit
- E2E pytest was upgraded because older version was vulnerable

Current E2E pytest range:

```text
pytest>=9.0.3,<9.1
```

### H7C Container Scanning
Infra only:
- Trivy `0.74.0`
- scan all Compose runtime images
- scanner loop continues across images instead of stopping at first failure
- LiteLLM RC image previously had fixable HIGH/CRITICAL vulnerabilities
- moved to stable `v1.104.0`

Current policy:
- per-image baseline
- not global threshold
- HIGH baseline per image
- CRITICAL baseline per image
- unknown image/tag fails until reviewed
- improved count generates notice
- security posture should not silently worsen

PostgreSQL:
- official images cannot realistically reach zero CRITICAL in current context
- approved per-image CRITICAL baseline may be `2`
- **do not interpret this as global CRITICAL <= 2**

Example conceptual baseline:

```json
{
  "litellm-image": {
    "critical": 0,
    "high": 0
  },
  "postgres:16.15": {
    "critical": 2,
    "high": "<actual-reviewed-value>"
  },
  "redis-image": {
    "critical": "<actual-reviewed-value>",
    "high": "<actual-reviewed-value>"
  }
}
```

Always use actual output from current Trivy CI scan, not Docker Hub badge numbers.

### Important H7 incident
There was an error:

```text
IsADirectoryError: [Errno 21] Is a directory: '/app/config.yaml'
```

Root cause:
- wrong `LITELLM_CONFIG_PATH` in local `.env`

Resolved by fixing:

```env
LITELLM_CONFIG_PATH=../llm-gateway-config/config/litellm_config.yaml
```

Compose hardening berikut sudah diterapkan dan diverifikasi pada H10A:

```yaml
volumes:
  - type: bind
    source: ${LITELLM_CONFIG_PATH:-../llm-gateway-config/config/litellm_config.yaml}
    target: /app/config.yaml
    read_only: true
    bind:
      create_host_path: false
```

This prevents Docker Compose from silently creating a directory when source path is missing.

### H7 GitHub status
Technical scanning implementation is complete.

Pada 2026-10-10, user mengonfirmasi merge gate GitHub sudah diverifikasi dan berjalan. Checkpoint verifikasi manual H7 ditutup berdasarkan konfirmasi user; assistant tidak menjalankan ulang pemeriksaan GitHub pada sesi review ini.

Status:

```text
H7 SECURITY IMPLEMENTATION COMPLETE ✅
H7 GITHUB MERGE GATE VERIFIED BY USER ✅
H7 COMPLETE ✅
```

---

## H8 — Enforcement Testing

### H8A Blocked Key

Test:

```text
test_blocked_key_is_rejected
```

Behavior:

```text
same virtual key
    ↓
request before block → 200
    ↓
/key/block
    ↓
request after block → 401/403
```

Status:

```text
H8A COMPLETE ✅
```

### H8B RPM Limit

Disposable team:

```text
rpm_limit = 2
tpm_limit = 50000
```

Key:
- no key-level RPM/TPM override
- uses `all-team-models`

Observed output:

```text
request #1 → 200
request #2 → 200
request #3 → 429
```

Status:

```text
H8B COMPLETE ✅
```

### H8C Budget Enforcement

Disposable virtual key:
- tiny key budget
- team/member budget higher so only key budget is being tested

Flow:

```text
first request → 200
spend asynchronously persisted
poll /key/info
spend >= key max_budget
next request → rejected
```

Observed:

```text
test_key_budget_is_enforced PASSED
```

Status:

```text
H8C COMPLETE ✅
```

### H8D Regression

Runner:

```text
scripts/run-limits.sh
```

Latest:

```text
3 enforcement tests PASS
3 smoke tests PASS
8 live tests PASS
E2E validation PASS
```

Status:

```text
H8 COMPLETE ✅
```

---

# 15. Current Milestone Summary

```text
H1 Version pinning                PASS (image/container existing)
H2 Secret hardening               PASS (env 600, scan)
H3 Network isolation              PASS lokal; gateway server perlu firewall/TLS
H4 Health/failure recovery        PASS; readiness diperbaiki
H5 Backup/restore                 PASS; 83 tabel identik
H6 CI/config validation           PASS lokal tiga repo
H7 Security scan + merge gate     PASS baseline; temuan keamanan tetap dicatat
H8 Enforcement + tool calling    PASS
H9A–H9E Lifecycle/regression      PASS lokal; freeze provisioning wajib
H10A Existing Docker port 4000    PASS; staging dibatalkan/dihapus
H10B Config release verification  PASS
H10C Config rollback + restore    PASS dalam batas image/schema sama
H10D Runbooks/pilot checklist     COMPLETE lokal; go-live server bersyarat
```

---

# 16. H9 — Lifecycle dan Regression Selesai Lokal

H9 goal:

```text
one user
 ├── virtual key A
 └── virtual key B
      │
      ▼
    offboard
      │
      ├── key A rejected
      └── key B rejected

historical spend remains
historical attribution remains
```

Status setelah implementasi H9E dan verifikasi gateway lokal pada 2026-10-10:

```text
H9A Multiple-key fixture                 COMPLETE / LIVE PASS
H9B Offboard all discovered user keys     COMPLETE / LIVE PASS
H9C Verify every old key rejected         COMPLETE / LIVE PASS
H9D Verify spend/history retained         COMPLETE / LIVE PASS
H9E Regression + runner                  COMPLETE / LOCAL PASS
```

H9 ditutup untuk implementasi dan pengujian lokal dengan bukti bagian 13. Ini bukan klaim bahwa perubahan sudah di-commit/push, CI remote sudah lulus, atau staging H10 sudah siap.

## H9A — Multiple-key fixture

- `tests/conftest.py`: fixture `multi_key_identity` dan `multi_key_clients` sudah ada.
- Satu user dan team memiliki dua key berbeda untuk `developer-laptop` / `developer-ci`, dengan `auto_create_key=False` dan `models=["all-team-models"]`.
- `test_multiple_user_keys_work_before_offboarding` memeriksa key berbeda, atribusi user/team, HTTP 200, dan respons inference tidak kosong untuk kedua key.
- `try/finally` mencakup provisioning dan test. Cleanup mencoba semua key yang sudah tercatat dan pemblokiran team, mengumpulkan error, lalu menggagalkan teardown jika ada kegagalan.
- Cleanup memakai block/inert, tanpa hard delete.

## H9B — Offboard semua key yang ditemukan

- Helper ditambahkan pada `LiteLLMClient` existing tanpa abstraction HTTP baru.
- Discovery berdasarkan `user_id`, bukan daftar raw virtual key dari fixture.
- Tes memakai `page_size=1` untuk dua key sehingga pagination benar-benar diperlukan.
- Guard menolak key user lain, token kosong/duplikat, halaman salah, perubahan jumlah record, dan discovery tidak lengkap.
- Block memakai token identifier dari API. Respons diperiksa terhadap identitas key/user dan `blocked=True`.
- Kegagalan satu key tidak menghentikan percobaan key berikutnya; operasi akhirnya gagal jika ada key yang belum terkonfirmasi diblokir.

## H9C — Verifikasi key lama ditolak

- Tes membaca ulang key dan memastikan record yang sama masih ada serta `blocked=True`.
- Kedua credential lama dipakai kembali untuk inference; masing-masing harus menghasilkan HTTP 401/403.
- Assertion berjalan sebelum teardown memblokir team, sehingga penolakan tidak bergantung pada pemblokiran team saat cleanup.

## H9D — Retensi spend dan histori

- Kedua key menghasilkan spend sebelum offboarding; polling menunggu persistensi spend key/user.
- Baseline histori berisi request berbayar dengan `request_id` dan mencakup kedua token.
- Setelah offboarding, record key/user tetap tersedia; atribusi key ke user/team tetap sama; spend kumulatif key/user tidak berkurang.
- Seluruh request baseline harus tetap ada berdasarkan `request_id`, dengan `api_key`, `user`, `team_id`, dan nilai spend yang sama.
- Histori dibatasi satu halaman untuk fixture kecil. Assertion `total == len(data)` dan `total_is_capped` mencegah halaman tambahan terlewat diam-diam; ini belum mendukung histori arbitrer dengan banyak halaman.
- Polling spend dan histori masing-masing berjendela 20 detik; persistensi runtime yang lebih lambat dapat menyebabkan timeout.

## Hasil review dan tindak lanjut

Arsitektur mengikuti handoff. Alur fixture terisolasi dua key sudah lulus pengujian lifecycle dan full live regression H9E pada gateway lokal. Catatan review awal beserta resolusinya:

1. **[P2, batasan operasional] Discovery bukan operasi atomik dengan pemblokiran.** `offboard_user_keys()` mengambil snapshot sekali lalu memblokir snapshot tersebut. Simulasi membuat key ketiga saat block berlangsung: helper tetap mengembalikan `discovered_count=2` / `blocked_count=2`, sementara key ketiga masih aktif. Ini tidak memengaruhi fixture H9 yang tidak melakukan provisioning bersamaan, tetapi helper belum menjamin semua akses user tertutup jika provisioning masih berlangsung. Sebelum dipakai sebagai prosedur operasional, tetapkan penghentian/serialisasi provisioning selama offboarding dan verifikasi akhir key aktif. Reread saja tidak menutup race tanpa koordinasi provisioning. Jangan memblokir shared team sebagai jalan pintas. Helper juga belum menonaktifkan kemampuan penerbitan key baru.

2. **[RESOLVED H9E] Dua tes lifecycle menjadi required regression tests.** `scripts/ci/validate-suite.py` kini mewajibkan 13 nama tes gateway. Tes permanen menjalankan validator pada salinan sementara: suite lengkap PASS, masing-masing fungsi lifecycle yang dihilangkan menghasilkan kegagalan dan nama tes yang hilang. File asli tidak diubah.

3. **[RESOLVED H9E] Coverage negatif permanen.** `tests/unit/` memuat 22 kasus: pagination sebelum block, tujuh bentuk discovery tidak valid yang tidak boleh memblokir key apa pun, lima bentuk kegagalan block parsial, tiga kasus validator, serta enam kasus histori. Kasus histori menjalankan assertion H9D existing terhadap respons simulasi dan membuktikan request hilang/atribusi berubah/spend berubah ditolak. Fixture unit melarang HTTP; tidak ada client HTTP baru.

Status Git saat review awal (sebelum H9E):
- Modified: `tests/client.py`, `tests/conftest.py`.
- Untracked: `tests/test_lifecycle.py`; pastikan ikut commit bersama perubahan H9 agar tersedia di CI.
- Tidak ada kode implementasi yang diubah reviewer.

## H9E — Implementasi dan DoD

1. **PASS — Required regression:** dua tes lifecycle masuk validator; negative check kehilangan setiap tes dijalankan dalam unit suite.
2. **PASS — Runner:** `run-unit.sh` baru untuk offline; `run-live.sh` menerima argumen pytest agar file lifecycle dapat dipilih; `run-all.sh` merangkai unit → smoke → live. Smoke lokal dan workflow staging memakai `not live and not unit`.
3. **PASS — CI:** `scripts/ci/validate.sh` bertambah menjadi 8 tahap dan mengeksekusi unit tests. Workflow validasi existing otomatis memakai tahap baru ini.
4. **PASS — Regression:** 22 unit, 2 lifecycle tersendiri, 3 smoke, dan 10 full live lulus; tidak ada error teardown. Bukti lengkap ada di bagian 13.
5. **PASS — Dokumentasi:** README E2E memuat persiapan, perintah, cakupan marker, cleanup, dan batasan snapshot/concurrency. Koordinasi provisioning menjadi prasyarat operasional sebelum memakai helper untuk offboarding nyata.

**H9E COMPLETE (lokal).** Seluruh DoD teknis lokal terpenuhi. Langkah publikasi yang belum dilakukan: commit/push seluruh perubahan H9 termasuk `tests/test_lifecycle.py`, `tests/unit/`, dan `scripts/run-unit.sh`, kemudian verifikasi CI remote. Root handoff berada di luar tiga repository Git, sehingga tidak otomatis ikut commit E2E.

Checkpoint setelah H9E adalah H10; H10A–D kini selesai lokal pada Docker existing (lihat bagian 17). Jangan menganggap dokumentasi prasyarat provisioning sebagai implementasi locking/revocation penerbitan key baru.

---

# 17. H10 — Operational Readiness, selesai lokal 2026-10-10

## H10A — Docker existing port 4000

Pilihan staging terpisah port 4001 pada checkpoint terdahulu **dibatalkan oleh instruksi
terbaru user**. `docker-compose.staging.yml`, `scripts/staging/`, validator staging,
dan dokumen staging dihapus; README diperbarui. Tidak ada container staging.
Sisa `.env.staging`, config snapshot, dan volume staging lama tidak dipakai dan boleh
tersimpan sebagai arsip sensitif. Tidak ada container/network/volume baru pada H10B–D.

ID runtime tetap:
- gateway `9c77da1dea53`, LiteLLM 1.104.0, port 4000;
- PostgreSQL `2abff28af371`, 16.15, tidak dipublikasikan;
- Redis `04c48e8f579d`, 7.4.11-alpine, tidak dipublikasikan.

## H10B — Release config COMPLETE / LIVE PASS

`scripts/release/release.sh capture|deploy|rollback` memanggil `manage.py`.
Capture mencatat snapshot/checksum config, commit/status dirty/checksum source tiga
repo, ID container/image, path mount dan waktu. Deploy memvalidasi manifest/runtime,
backup database+environment, mempertahankan inode bind mount, restart container
existing, memverifikasi mount, readiness, dependency/catalog dan smoke. File lock
mencegah dua operasi release bersamaan. Folder `releases/` ignored dan privat.

Uji nyata: timeout request 180→181; isi mount diverifikasi, health PASS dan smoke
3/3 PASS. Tidak mengubah image atau membuat container. Manifest dapat dirty; belum
menjadi bukti publikasi source atau CI remote.

## H10C — Rollback/recovery COMPLETE dalam scope lokal

Rollback mengembalikan config persis byte semula; health dan smoke 3/3 PASS, ID image/
container sama. Deploy menyimpan recovery config sebelum perubahan, mengusahakan
pemulihan otomatis jika verifikasi gagal, dan tetap exit gagal. Tes negatif offline
membuktikan alur failure/recovery serta guard checksum/identity/alias/credential.
Image/schema berbeda ditolak; downgrade image/migrasi belum diuji.

Backup: custom dump + metadata checksum + `.env` privat untuk salt/recovery.
Restore hanya ke `<POSTGRES_DB>_restore_test`, menolak main DB/nama lain/nama lebih
63 karakter. Wrapper lama mengikuti guard ini. Drill `--quiesce` menghentikan gateway
sebentar, membandingkan **83 tabel** (jumlah baris/fingerprint sama), dan menyalakan
container existing. Database test dibuat di PostgreSQL existing; bukan container baru.
Belum boot aplikasi terhadap database restore. Jangan lakukan write/provisioning lain
selama drill; jangan restore main DB untuk memperbaiki config.

## H10D — Runbooks/pilot readiness COMPLETE lokal

Dokumen infra:
- `docs/release.md`
- `docs/backup-restore.md`
- `docs/operations.md`
- `docs/phase1-checklist.md`

Mencakup release, rollback, backup/salt, onboarding, offboarding, incident, pilot dan
checklist server. Offboarding tetap wajib freeze provisioning serta verifikasi akhir
semua halaman key; helper snapshot bukan locking atomik atau pencabutan akses SSO.

## Hasil cross-check H1–H10

- Infra 7 tahap PASS, termasuk **12 tes operasional**.
- Config 6 tahap PASS; folder kosong YAML dibersihkan dan validator diperjelas.
- E2E 8 tahap PASS; **37 kasus: 22 unit + 3 smoke + 12 live**, termasuk tool calling
  kedua alias yang baru ditambahkan. OpenCode existing PASS.
- Outage Redis/PostgreSQL satu per satu: ditemukan HTTP readiness cached 200; script
  diperkuat dengan dependency check dan diuji ulang, gagal saat outage dan pulih sehat.
- Gitleaks 8.28.0 history+working tree dan pip-audit 2.10.1 ketiga repo PASS.
- Trivy 0.74.0 PASS baseline: LiteLLM 0/0, PostgreSQL **1/28**, Redis **0/2** C/H.
  Critical terdeteksi `CVE-2025-68121` pada stdlib Go v1.24.6 image PostgreSQL.
  Baseline 0/0, 2/28, 0/4 tidak diubah. Review risiko/image sebelum go-live.
- `.env` kini 600, backup baru 600, secret env cocok dengan container (tanpa dicetak).
- Scanner dijalankan native; tidak membuat container scanner baru.

Lihat laporan per milestone, lampiran kode lengkap, dan evidence di `reports/`.

---

# 18. Phase 1 Definition of Done

Implementasi dan pengujian **lokal** sampai H10D selesai. Keputusan go-live server
**bersyarat**, bukan otomatis lulus karena lokal hijau.

```text
versions / aliases / virtual keys       PASS
team policy / enforcement / spend       PASS
OpenCode / streaming / tool calling     PASS
lifecycle + retention + unit regression PASS (freeze provisioning wajib)
backup + restore data comparison        PASS (83 tabel, database test existing)
health / dependency failure recovery    PASS
config release / rollback               PASS (image/schema sama)
local CI validators / security policy   PASS (CVE tersisa terdokumentasi)
runbooks / pilot checklist              COMPLETE
commit/push candidate / CI remote       BELUM DIJALANKAN
server TLS/firewall/storage/alarms       BELUM DIVERIFIKASI
server deploy / image-schema downgrade BELUM DILAKUKAN
```

Prometheus/Grafana, HA/Kubernetes/multi-region dan advanced guardrails tetap fase
lanjutan. Jadwal backup luar host, PIC, budget pilot dan target recovery perlu
konfigurasi/keputusan operator sesuai checklist server.

---

# 19. Important "Do Not Break" Rules

1. **Do not bypass logical aliases**
   - developer uses `company-fast` / `company-coding`

2. **Do not expose provider secrets**
   - developer gets LiteLLM virtual key only

3. **Do not use master key from developer client**

4. **Do not make `models/*.yaml` depend on `logical_name`**
   - logical ID comes from filename

5. **Do not create another HTTP client abstraction for E2E**
   - use existing `LiteLLMClient`

6. **Do not add `admin_post()` unless the architecture is explicitly changed**
   - current `LiteLLMClient.post()` uses whichever API key the instance owns

7. **Do not call raw `requests` directly in tests if `LiteLLMClient` can be used**
   - raw `requests` belongs inside `tests/client.py`

8. **Do not hard-delete disposable records if historical spend/audit is needed**
   - block/inert is preferred

9. **Do not globally allow `CRITICAL <= 2`**
   - vulnerability tolerance is per-image reviewed baseline

10. **Do not silently increase vulnerability baseline**
    - increase requires explicit security review

11. **Do not trust Docker Hub count as CI baseline**
    - use the same Trivy command/database/policy used by CI

12. **Do not reintroduce RC LiteLLM image that failed vulnerability scan**

13. **Pertahankan required GitHub merge gate H7**
    - Sudah diverifikasi dan dikonfirmasi user pada 2026-10-10; jangan membuka ulang checkpoint ini tanpa perubahan konfigurasi atau bukti regresi.

---

# 20. Recommended First Prompt in New Chat

```text
Baca LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md dan reports/PHASE1_H1_H10_REPORT.md.
H1–H10D implementasi/verifikasi lokal selesai, hanya Docker existing port 4000.
Jangan buat staging atau container/environment baru. Compose staging sudah dihapus.
37 E2E/unit + 12 operasi PASS, OpenCode PASS, restore 83 tabel identik,
release/rollback config PASS. Temuan Critical/High tetap ada sesuai baseline.
H7 merge gate GitHub sudah dikonfirmasi user; perubahan lokal belum commit/push/CI.
Ikuti docs/phase1-checklist.md sebelum persiapan deploy server. Jangan menyimpulkan
server siap hanya dari hasil lokal. Pertahankan arsitektur LiteLLMClient dan
koordinasi provisioning saat offboarding. Jangan hard-delete audit atau menaikkan
baseline keamanan tanpa review. Laporan kode lengkap tersedia di reports/.
```

---

# 21. Current Project Position

**H10D lokal selesai.** Tidak ada deploy server. Langkah berikut: candidate yang
tercatat di Git/CI, review keamanan image, dan pemenuhan checklist target server.
Laporan dan handoff berada di luar tiga repository Git; salin/arsipkan sebagai
dokumen project bila ingin ikut publikasi, tanpa menyertakan file secret/backup.
