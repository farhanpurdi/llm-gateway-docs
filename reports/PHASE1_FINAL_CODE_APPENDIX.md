# Kode penutupan teknis Phase 1

Snapshot17Oktober2026. [Laporan sederhana](PHASE1_FINAL_CROSSCHECK_REPORT.md) menjelaskan alasan/hasil; [manifest hash](phase1-final-evidence/code-manifest.json) memeriksa integritas. Baca bagian yang terkait.

File yang sudah memiliki perubahan lokal disalin lengkap untuk review; bukan klaim seluruh isinya baru ditulis. Tambahan validator Compose/8regresi memperbaiki perbedaan JSONCI; runtimeYAML tetap sama. Workflow live staging dihapus sesuaiO-08, tidak dicantumkan sebagai file aktif. Secret/dump tidak disertakan.

| No. | Source | SHA-256 |
|---|---|---|
| 1 | [llm-gateway-e2e/tests/client.py](../../llm-gateway-e2e/tests/client.py) | `7450a7e1aeedf410f6bba6e93f0acdf229a83a8bb12536c72d475cbd29059cad` |
| 2 | [llm-gateway-e2e/tests/conftest.py](../../llm-gateway-e2e/tests/conftest.py) | `b815d1bf001eb1478dd9c5f94587d174ec833385cd4ea81f29880a020b5dbd69` |
| 3 | [llm-gateway-e2e/tests/test_limits.py](../../llm-gateway-e2e/tests/test_limits.py) | `a2806fb8a669f3d024ab06f87e58a2546c6d793f4392640544725293daccaf63` |
| 4 | [llm-gateway-e2e/tests/test_failure_semantics.py](../../llm-gateway-e2e/tests/test_failure_semantics.py) | `d7a8cae32977f254579309db37868a65d5429351be5ea626188965823740aa4d` |
| 5 | [llm-gateway-e2e/tests/native_failure_probe.py](../../llm-gateway-e2e/tests/native_failure_probe.py) | `875fe8aef7d4a356628be79090d85a13a523e110c16a8bd92892ddddd59e246e` |
| 6 | [llm-gateway-e2e/tests/maintenance.py](../../llm-gateway-e2e/tests/maintenance.py) | `2f1205c7220ac0c8be25ac0ae3be4fb448dc211e880942c1330c9f53bb93f26e` |
| 7 | [llm-gateway-e2e/tests/test_dependency_outage.py](../../llm-gateway-e2e/tests/test_dependency_outage.py) | `a13a7e731a974113dad21e31153563aa4d0e3dce7b66b1a0ac3c7b01f926577c` |
| 8 | [llm-gateway-e2e/tests/test_key_rotation.py](../../llm-gateway-e2e/tests/test_key_rotation.py) | `d8981aafad6fa0409814a2ac06ba2da679ad9abb5a54f9f11d8431d6a7a140ce` |
| 9 | [llm-gateway-e2e/tests/unit/test_fixture_cleanup.py](../../llm-gateway-e2e/tests/unit/test_fixture_cleanup.py) | `e75e65f577095f34e94c52d297568c4e7ab0d335f4f0bc01889f5e4066ea6f1f` |
| 10 | [llm-gateway-e2e/tests/unit/test_transport_privacy.py](../../llm-gateway-e2e/tests/unit/test_transport_privacy.py) | `7cdc23828b76ee86ee854bcfcf89858bd732450311f9148006b50cbcd143b5b1` |
| 11 | [llm-gateway-e2e/tests/unit/test_maintenance.py](../../llm-gateway-e2e/tests/unit/test_maintenance.py) | `b0936db1915cc811cb833bc5cba1ce95a84a256081348554c09917b8e1775db3` |
| 12 | [llm-gateway-e2e/tests/unit/test_opencode.py](../../llm-gateway-e2e/tests/unit/test_opencode.py) | `e29908e576b2741f235fb29eb5a1ef1ed689cda11090c22b2360a5e9fbffee76` |
| 13 | [llm-gateway-e2e/tests/unit/test_suite_validator.py](../../llm-gateway-e2e/tests/unit/test_suite_validator.py) | `4857ee10684b70477331931558d3f76bdf318eebd9e3c62209d958bc611870c4` |
| 14 | [llm-gateway-e2e/scripts/ci/validate-suite.py](../../llm-gateway-e2e/scripts/ci/validate-suite.py) | `1acd2d497e5fff34907b08e70e9771d70572a3c38994e98d8858140e76bedd00` |
| 15 | [llm-gateway-e2e/scripts/run-native.sh](../../llm-gateway-e2e/scripts/run-native.sh) | `51eb333afb31a72f17843c849b5fd928582dd4bcdf177f4622ded54ecb1a2601` |
| 16 | [llm-gateway-e2e/scripts/run-outage.sh](../../llm-gateway-e2e/scripts/run-outage.sh) | `bc7449481c2dad02ecb85f14bac3a22db080fd0d2e15aa744dfb74908fdc657d` |
| 17 | [llm-gateway-e2e/scripts/run-all.sh](../../llm-gateway-e2e/scripts/run-all.sh) | `212089e105c43d4b40fbe15a46683b8f06929d735fb7ec0c5f46b9ceccf423a7` |
| 18 | [llm-gateway-e2e/scripts/run-live.sh](../../llm-gateway-e2e/scripts/run-live.sh) | `dd6decb2ffb02a07b5ea96010a624700cf749c5abcc5fec16d4aa5bdfbb6b3ed` |
| 19 | [llm-gateway-e2e/pytest.ini](../../llm-gateway-e2e/pytest.ini) | `78250e6bb8bfc186a2fc6ea9cd69c357005c22a626dab0b0dbdf75bf4d120a67` |
| 20 | [llm-gateway-e2e/.github/workflows/validate.yml](../../llm-gateway-e2e/.github/workflows/validate.yml) | `0f46d999ec11abae4a7c3c599abc030ac7ab6ac968a8e73364b0972b8bda1b08` |
| 21 | [llm-gateway-infra/.github/workflows/validate.yml](../../llm-gateway-infra/.github/workflows/validate.yml) | `9f0cdd8817878118eaf686a464001d3904fa54c8e4690acdccb3aca9ff1bd905` |
| 22 | [llm-gateway-config/.github/workflows/validate.yml](../../llm-gateway-config/.github/workflows/validate.yml) | `77f34be3701200920a19736bdbaa4e41e3da47c0e3b11937702623c5a646f792` |
| 23 | [llm-gateway-config/scripts/ci/requirements.lock](../../llm-gateway-config/scripts/ci/requirements.lock) | `c9202ee0b7d35153154ac1cc5ae2a58891736f68dcea2fe766b74206ce6d6b7f` |
| 24 | [llm-gateway-infra/scripts/requirements.lock](../../llm-gateway-infra/scripts/requirements.lock) | `bb1ddcc99e410fba8ab5a332aded0549b2cf214bb4bb63b8a1c83478a9573b7a` |
| 25 | [llm-gateway-e2e/requirements.lock](../../llm-gateway-e2e/requirements.lock) | `b568b242bba5c1d3fc407fb47e0a5fa1ca1f91dd9274a00692e37d3f388f690a` |
| 26 | [llm-gateway-docs/.gitleaks.toml](../.gitleaks.toml) | `69af8bd59bb687e5ddc5d15941026286ebea05944a53b17dc260e46a5b215912` |
| 27 | [llm-gateway-docs/reports/phase1-final-evidence/config-drill.py](phase1-final-evidence/config-drill.py) | `92fc9809e9f382bd06c2693ba3fb531fb8346d27af28869b4d368da176765b8c` |
| 28 | [llm-gateway-infra/scripts/ci/validate-compose.py](../../llm-gateway-infra/scripts/ci/validate-compose.py) | `d56a79b316d382550e22946ca9ef2f28a43f752553045056558d4ba624f6eeb4` |
| 29 | [llm-gateway-infra/scripts/ci/test-compose-contract.py](../../llm-gateway-infra/scripts/ci/test-compose-contract.py) | `d91ff54edf9b88f5e0a2621b74b0264d13b78f0276b939c43817be981d77a1fb` |
| 30 | [llm-gateway-infra/scripts/ci/validate.sh](../../llm-gateway-infra/scripts/ci/validate.sh) | `bc3665772531a23b155e306bec00ba7b6bfcb46853bee685488f4f3f5cc907b5` |
| 31 | [llm-gateway-docs/.github/workflows/validate.yml](../.github/workflows/validate.yml) | `2dee530289e73947074daf91a458a4ea9806fa66e479b56e783256a9bbe67ad1` |
| 32 | [llm-gateway-docs/reports/phase1-final-evidence/audit-final.py](phase1-final-evidence/audit-final.py) | `43c9b3aa06ce65cf7e27e3a08619b6cf75bed3251fcabc9a6054e5133a8b5d37` |

## 1. llm-gateway-e2e/tests/client.py

SHA-256: `7450a7e1aeedf410f6bba6e93f0acdf229a83a8bb12536c72d475cbd29059cad`

```python
from __future__ import annotations

from typing import Any

import requests


class RedactedKey(str):
    """Keep HTTP behavior while hiding credentials in pytest/container reprs."""
    def __repr__(self):
        return '<redacted credential>'


class GatewayTransportError(RuntimeError):
    """Transport diagnostics must never echo credential-bearing URLs or bodies."""


class LiteLLMClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 60,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = RedactedKey(api_key)
        self.timeout = timeout

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": RedactedKey(f"Bearer {self.api_key}"),
            "Content-Type": "application/json",
        }

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        try:
            return requests.get(
                f"{self.base_url}{path}",
                headers=self.headers,
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise GatewayTransportError(
                f"Gateway GET transport failed: {type(error).__name__}; details suppressed"
            ) from None

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        stream: bool = False,
    ) -> requests.Response:
        try:
            return requests.post(
                f"{self.base_url}{path}",
                headers=self.headers,
                json=json,
                stream=stream,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise GatewayTransportError(
                f"Gateway POST transport failed: {type(error).__name__}; details suppressed"
            ) from None

    def expect_json(
        self,
        response: requests.Response,
        expected_status: int = 200,
    ) -> dict[str, Any]:
        if response.status_code != expected_status:
            raise AssertionError(
                f"Expected HTTP {expected_status}, "
                f"got {response.status_code}; response body suppressed"
            )

        return response.json()

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
                "does not contain team_id."
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

    def team_info(self, team_id: str) -> dict[str, Any]:
        return self.expect_json(self.get('/team/info', params={'team_id': team_id}))

    def member_info(self, team_id: str, user_id: str) -> dict[str, Any]:
        matches = [row for row in self.team_info(team_id)['team_memberships']
                   if row.get('user_id') == user_id]
        if len(matches) != 1:
            raise AssertionError('Expected exactly one matching team membership')
        return matches[0]

    def key_info(self, virtual_key: str) -> dict[str, Any]:
        return self.expect_json(self.get('/key/info', params={'key': virtual_key}))['info']

    def model_prices(self) -> dict[str, dict[str, Any]]:
        """Return only public pricing fields; /model/info can contain credentials."""
        data = self.expect_json(self.get('/model/info'))
        result = {}
        for entry in data['data']:
            name = entry.get('model_name')
            if name not in {'company-fast', 'company-coding'}:
                continue
            info = entry.get('model_info') or {}
            result[name] = {
                'upstream': entry.get('litellm_params', {}).get('model'),
                **{field: info.get(field) for field in (
                    'input_cost_per_token', 'output_cost_per_token',
                    'cache_read_input_token_cost')},
            }
        return result

    def list_user_keys_page(
        self,
        *,
        user_id: str,
        page: int = 1,
        size: int = 100,
    ) -> dict[str, Any]:
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty")

        if page < 1:
            raise ValueError("page must be >= 1")

        if not 1 <= size <= 100:
            raise ValueError("size must be between 1 and 100")

        response = self.get(
            "/key/list",
            params={
                "user_id": user_id,
                "page": page,
                "size": size,
                "return_full_object": "true",
                "include_team_keys": "false",
                "include_created_by_keys": "false",
            },
        )

        if response.status_code != 200:
            raise AssertionError(
                "Cannot list user keys: "
                f"HTTP {response.status_code}"
            )

        return response.json()

    def list_user_keys(
        self,
        *,
        user_id: str,
        page_size: int = 100,
    ) -> list[dict[str, Any]]:
        results = []
        seen_tokens = set()

        page = 1
        expected_total = None
        expected_pages = None

        while True:
            data = self.list_user_keys_page(
                user_id=user_id,
                page=page,
                size=page_size,
            )

            total_count = data["total_count"]
            total_pages = data["total_pages"]

            if data["current_page"] != page:
                raise AssertionError("Unexpected key-list page")

            if expected_total is None:
                expected_total = total_count
                expected_pages = total_pages
            elif (
                total_count != expected_total
                or total_pages != expected_pages
            ):
                raise AssertionError(
                    "Key count changed during pagination; "
                    "retry discovery before offboarding"
                )

            for item in data["keys"]:
                if item.get("user_id") != user_id:
                    raise AssertionError(
                        "Key discovery returned another user's key"
                    )

                token = item.get("token")

                if not isinstance(token, str) or not token:
                    raise AssertionError(
                        "Key discovery returned no token identifier"
                    )

                if token in seen_tokens:
                    raise AssertionError(
                        "Duplicate key encountered during pagination"
                    )

                seen_tokens.add(token)
                results.append(item)

            if page >= total_pages:
                break

            if not data["keys"]:
                raise AssertionError(
                    "Empty page before the end of key discovery"
                )

            page += 1

        if len(results) != expected_total:
            raise AssertionError(
                "Incomplete key discovery: "
                f"expected={expected_total}, "
                f"received={len(results)}"
            )

        return results

    def offboard_user_keys(
        self,
        *,
        user_id: str,
        page_size: int = 100,
    ) -> dict[str, Any]:
        keys = self.list_user_keys(
            user_id=user_id,
            page_size=page_size,
        )

        blocked_count = 0
        errors = []

        for index, item in enumerate(keys, start=1):
            label = f"key #{index}"

            try:
                response = self.post(
                    "/key/block",
                    json={
                        "key": item["token"],
                    },
                )

                if response.status_code != 200:
                    errors.append(
                        f"{label}: HTTP {response.status_code}"
                    )
                    continue

                data = response.json()

                if (
                    data.get("token") != item["token"]
                    or data.get("user_id") != user_id
                ):
                    errors.append(
                        f"{label}: unexpected key identity in response"
                    )
                    continue

                if data.get("blocked") is not True:
                    errors.append(
                        f"{label}: blocked status was not confirmed"
                    )
                    continue

                blocked_count += 1

            except Exception as exc:
                errors.append(
                    f"{label}: {type(exc).__name__}"
                )

        if errors:
            raise AssertionError(
                "Offboarding incomplete: "
                f"confirmed={blocked_count}/{len(keys)}. "
                + "; ".join(errors)
            )

        return {
            "user_id": user_id,
            "discovered_count": len(keys),
            "blocked_count": blocked_count,
        }

    def list_user_spend_logs_page(
        self,
        *,
        user_id: str,
        start_date: str,
        end_date: str,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty")

        if page < 1:
            raise ValueError("page must be >= 1")

        if not 1 <= page_size <= 1000:
            raise ValueError("page_size must be between 1 and 1000")

        response = self.get(
            "/spend/logs/v2",
            params={
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date,
                "page": page,
                "page_size": page_size,
            },
        )

        if response.status_code != 200:
            raise AssertionError(
                "Cannot read user spend history: "
                f"HTTP {response.status_code}"
            )

        return response.json()
```

## 2. llm-gateway-e2e/tests/conftest.py

SHA-256: `b815d1bf001eb1478dd9c5f94587d174ec833385cd4ea81f29880a020b5dbd69`

```python
from __future__ import annotations

import os
import json
import re
import shutil
import subprocess
import uuid
from pathlib import Path

import yaml

import pytest

from tests.client import LiteLLMClient, RedactedKey
from tests.opencode import cli_environment, prepare_project
from tests.maintenance import stopped_dependency


@pytest.fixture()
def dependency_outage(base_url):
    """Mechanical stop/recovery is paired even when a request assertion fails."""
    return lambda dependency: stopped_dependency(dependency, base_url)


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable is missing: {name}"
        )

    return value


@pytest.fixture(scope="session")
def base_url() -> str:
    return required_env("LITELLM_BASE_URL")


@pytest.fixture(scope="session")
def master_key() -> str:
    return required_env("LITELLM_MASTER_KEY")


@pytest.fixture(scope="session")
def fast_model() -> str:
    return os.getenv(
        "E2E_FAST_MODEL",
        "company-fast",
    )


@pytest.fixture(scope="session")
def coding_model() -> str:
    return os.getenv(
        "E2E_CODING_MODEL",
        "company-coding",
    )


@pytest.fixture(scope="session")
def admin_client(
    base_url: str,
    master_key: str,
) -> LiteLLMClient:
    return LiteLLMClient(
        base_url=base_url,
        api_key=master_key,
    )


@pytest.fixture()
def identity_cleanup(admin_client):
    """Register immediately after team creation; teardown also covers failed setup."""
    registered = []
    yield lambda team_id, user_id: registered.append((team_id, user_id))
    errors = []
    for team_id, user_id in registered:
        try:
            admin_client.offboard_user_keys(user_id=user_id)
            if any(item.get("blocked") is not True for item in admin_client.list_user_keys(user_id=user_id)):
                errors.append("unblocked fixture key remains")
        except Exception as error:
            errors.append("key cleanup: " + type(error).__name__)
        try:
            admin_client.expect_json(admin_client.post(
                "/team/update", json={"team_id": team_id, "blocked": True}))
            if admin_client.team_info(team_id)["team_info"].get("blocked") is not True:
                errors.append("team cleanup not confirmed")
        except Exception as error:
            errors.append("team cleanup: " + type(error).__name__)
    if errors:
        pytest.fail("Fixture cleanup failed: " + "; ".join(errors), pytrace=False)


@pytest.fixture()
def e2e_identity(
    admin_client: LiteLLMClient,
    fast_model: str,
    coding_model: str,
    identity_cleanup,
):
    suffix = uuid.uuid4().hex[:8]

    user_id = f"e2e-user-{suffix}"
    team_alias = f"e2e-team-{suffix}"
    key_alias = f"e2e-key-{suffix}"

    #
    # 1. User
    #

    response = admin_client.post(
        "/user/new",
        json={
            "user_id": user_id,
            "user_role": "internal_user",
            "auto_create_key": False,
        },
    )

    admin_client.expect_json(response)

    #
    # 2. Team
    #

    response = admin_client.post(
        "/team/new",
        json={
            "team_alias": team_alias,
            "models": [
                fast_model,
                coding_model,
            ],
            "max_budget": 1,
            "budget_duration": "30d",
            "rpm_limit": 30,
            "tpm_limit": 50000,
            "metadata": {
                "environment": "e2e",
                "managed_by": "pytest",
            },
        },
    )

    team_data = admin_client.expect_json(response)

    team_id = team_data["team_id"]
    identity_cleanup(team_id, user_id)

    #
    # 3. Membership
    #

    response = admin_client.post(
        "/team/member_add",
        json={
            "team_id": team_id,
            "max_budget_in_team": 0.50,
            "member": {
                "role": "user",
                "user_id": user_id,
            },
        },
    )

    admin_client.expect_json(response)

    #
    # 4. Virtual Key
    #

    response = admin_client.post(
        "/key/generate",
        json={
            "user_id": user_id,
            "team_id": team_id,
            "key_alias": key_alias,
            "models": [
                "all-team-models",
            ],
            "metadata": {
                "environment": "e2e",
                "purpose": "automated-test",
            },
        },
    )

    key_data = admin_client.expect_json(response)

    virtual_key = RedactedKey(key_data["key"])

    context = {
        "user_id": user_id,
        "team_id": team_id,
        "team_alias": team_alias,
        "key_alias": key_alias,
        "virtual_key": virtual_key,
    }

    yield context


@pytest.fixture()
def user_client(
    base_url: str,
    e2e_identity: dict,
) -> LiteLLMClient:
    return LiteLLMClient(
        base_url=base_url,
        api_key=e2e_identity["virtual_key"],
    )


@pytest.fixture()
def rpm_limited_identity(
    admin_client: LiteLLMClient,
    fast_model: str,
    identity_cleanup,
):
    suffix = uuid.uuid4().hex[:8]

    user_id = f"e2e-rpm-user-{suffix}"
    team_alias = f"e2e-rpm-team-{suffix}"
    key_alias = f"e2e-rpm-key-{suffix}"

    #
    # 1. User
    #

    response = admin_client.post(
        "/user/new",
        json={
            "user_id": user_id,
            "user_role": "internal_user",
            "auto_create_key": False,
        },
    )

    admin_client.expect_json(response)

    #
    # 2. RPM-limited Team
    #

    team_data = admin_client.create_team(
        team_alias=team_alias,
        models=[
            fast_model,
        ],
        rpm_limit=2,
        tpm_limit=50000,
    )

    team_id = team_data["team_id"]
    identity_cleanup(team_id, user_id)

    #
    # 3. Membership
    #

    response = admin_client.post(
        "/team/member_add",
        json={
            "team_id": team_id,
            "max_budget_in_team": 0.50,
            "member": {
                "role": "user",
                "user_id": user_id,
            },
        },
    )

    admin_client.expect_json(response)

    #
    # 4. Virtual Key
    #
    # Penting:
    # jangan set rpm_limit/tpm_limit pada key.
    # Kita ingin membuktikan TEAM limit yang bekerja.
    #

    response = admin_client.post(
        "/key/generate",
        json={
            "user_id": user_id,
            "team_id": team_id,
            "key_alias": key_alias,
            "models": [
                "all-team-models",
            ],
            "metadata": {
                "environment": "e2e",
                "purpose": "rpm-enforcement-test",
            },
        },
    )

    key_data = admin_client.expect_json(response)

    virtual_key = RedactedKey(key_data["key"])

    context = {
        "user_id": user_id,
        "team_id": team_id,
        "team_alias": team_alias,
        "key_alias": key_alias,
        "virtual_key": virtual_key,
        "rpm_limit": 2,
        "tpm_limit": 50000,
    }

    #
    # Test berjalan di sini.
    #

    yield context


@pytest.fixture()
def rpm_user_client(
    base_url: str,
    rpm_limited_identity: dict,
) -> LiteLLMClient:
    return LiteLLMClient(
        base_url=base_url,
        api_key=rpm_limited_identity["virtual_key"],
    )


@pytest.fixture()
def budget_limited_identity(
    admin_client: LiteLLMClient,
    fast_model: str,
    identity_cleanup,
):
    suffix = uuid.uuid4().hex[:8]

    user_id = f"e2e-budget-user-{suffix}"
    team_alias = f"e2e-budget-team-{suffix}"
    key_alias = f"e2e-budget-key-{suffix}"

    key_max_budget = 0.000001

    #
    # 1. User
    #

    response = admin_client.post(
        "/user/new",
        json={
            "user_id": user_id,
            "user_role": "internal_user",
            "auto_create_key": False,
        },
    )

    admin_client.expect_json(response)

    #
    # 2. Team
    #
    # Team budget intentionally much larger
    # than the key budget.
    #

    team_data = admin_client.create_team(
        team_alias=team_alias,
        models=[
            fast_model,
        ],
        max_budget=1,
        budget_duration="30d",
    )

    team_id = team_data["team_id"]
    identity_cleanup(team_id, user_id)

    #
    # 3. Membership
    #

    response = admin_client.post(
        "/team/member_add",
        json={
            "team_id": team_id,
            "max_budget_in_team": 0.50,
            "member": {
                "role": "user",
                "user_id": user_id,
            },
        },
    )

    admin_client.expect_json(response)

    #
    # 4. Virtual Key
    #
    # Only this key has the tiny budget.
    #

    response = admin_client.post(
        "/key/generate",
        json={
            "user_id": user_id,
            "team_id": team_id,
            "key_alias": key_alias,
            "models": [
                "all-team-models",
            ],
            "max_budget": key_max_budget,
            "budget_duration": "1h",
            "metadata": {
                "environment": "e2e",
                "purpose": "budget-enforcement-test",
            },
        },
    )

    key_data = admin_client.expect_json(response)

    virtual_key = RedactedKey(key_data["key"])

    context = {
        "user_id": user_id,
        "team_id": team_id,
        "team_alias": team_alias,
        "key_alias": key_alias,
        "virtual_key": virtual_key,
        "max_budget": key_max_budget,
    }

    yield context


@pytest.fixture()
def budget_user_client(
    base_url: str,
    budget_limited_identity: dict,
) -> LiteLLMClient:
    return LiteLLMClient(
        base_url=base_url,
        api_key=budget_limited_identity["virtual_key"],
    )


@pytest.fixture()
def multi_key_identity(
    admin_client: LiteLLMClient,
    fast_model: str,
    coding_model: str,
):
    suffix = uuid.uuid4().hex[:8]

    user_id = f"e2e-lifecycle-user-{suffix}"
    team_alias = f"e2e-lifecycle-team-{suffix}"

    team_id = None
    keys = {}

    try:
        # 1. Buat user tanpa otomatis membuat key.
        response = admin_client.post(
            "/user/new",
            json={
                "user_id": user_id,
                "user_role": "internal_user",
                "auto_create_key": False,
            },
        )

        admin_client.expect_json(response)

        # 2. Buat team khusus untuk pengujian ini.
        team_data = admin_client.create_team(
            team_alias=team_alias,
            models=[fast_model, coding_model],
            max_budget=1,
            budget_duration="30d",
            rpm_limit=30,
            tpm_limit=50000,
        )

        team_id = team_data["team_id"]

        # 3. Hubungkan user ke team.
        response = admin_client.post(
            "/team/member_add",
            json={
                "team_id": team_id,
                "max_budget_in_team": 0.50,
                "member": {
                    "role": "user",
                    "user_id": user_id,
                },
            },
        )

        admin_client.expect_json(response)

        # 4. Buat key untuk masing-masing penggunaan.
        for usage in ("developer-laptop", "developer-ci"):
            key_alias = f"e2e-{usage}-{suffix}"

            response = admin_client.post(
                "/key/generate",
                json={
                    "user_id": user_id,
                    "team_id": team_id,
                    "key_alias": key_alias,
                    "models": ["all-team-models"],
                    "metadata": {
                        "environment": "e2e",
                        "purpose": "lifecycle-test",
                        "usage": usage,
                    },
                },
            )

            if response.status_code != 200:
                raise AssertionError(
                    f"Key provisioning failed for {key_alias}: "
                    f"HTTP {response.status_code}"
                )

            virtual_key = response.json().get("key")

            if not isinstance(virtual_key, str) or not virtual_key:
                raise AssertionError(
                    f"No virtual key returned for {key_alias}"
                )

            keys[usage] = {
                "key_alias": key_alias,
                "virtual_key": virtual_key,
            }

        yield {
            "user_id": user_id,
            "team_id": team_id,
            "team_alias": team_alias,
            "keys": keys,
        }

    finally:
        cleanup_errors = []

        for key_data in keys.values():
            key_alias = key_data["key_alias"]

            try:
                response = admin_client.post(
                    "/key/block",
                    json={
                        "key": key_data["virtual_key"],
                    },
                )

                if response.status_code != 200:
                    cleanup_errors.append(
                        f"Block {key_alias}: HTTP {response.status_code}"
                    )

            except Exception as exc:
                cleanup_errors.append(
                    f"Block {key_alias}: {type(exc).__name__}"
                )

        if team_id is not None:
            try:
                response = admin_client.post(
                    "/team/update",
                    json={
                        "team_id": team_id,
                        "blocked": True,
                    },
                )

                if response.status_code != 200:
                    cleanup_errors.append(
                        f"Block team: HTTP {response.status_code}"
                    )

            except Exception as exc:
                cleanup_errors.append(
                    f"Block team: {type(exc).__name__}"
                )

        if cleanup_errors:
            pytest.fail(
                "Lifecycle cleanup failed: "
                + "; ".join(cleanup_errors),
                pytrace=False,
            )


@pytest.fixture()
def multi_key_clients(
    base_url: str,
    multi_key_identity: dict,
) -> dict[str, LiteLLMClient]:
    clients = {}

    for usage, key_data in multi_key_identity["keys"].items():
        clients[usage] = LiteLLMClient(
            base_url=base_url,
            api_key=key_data["virtual_key"],
        )

    return clients


@pytest.fixture(scope='session')
def pilot_policy():
    path = Path(__file__).resolve().parents[2] / 'llm-gateway-config/policies/teams/pilot.yaml'
    policy = yaml.safe_load(path.read_text())
    assert policy['name'] == 'pilot'
    assert policy['models'] == ['company-fast', 'company-coding']
    return policy


@pytest.fixture()
def pilot_identity_factory(admin_client, base_url, pilot_policy):
    """Only disposable identities; the approved policy file and existing teams stay intact."""
    created = []

    def create(*, team_limits=None, member_budget='policy', member_duration='30d',
               first_key_budget=None, prefix='e2e-p109-', purpose='P1-09-P1-10'):
        limits = {**pilot_policy['limits']['team'], **(team_limits or {})}
        budget = (pilot_policy['limits']['member']['monthly_budget_usd']
                  if member_budget == 'policy' else member_budget)
        suffix = uuid.uuid4().hex[:8]
        team = admin_client.expect_json(admin_client.post('/team/new', json={
            'team_alias': prefix+suffix, 'models': pilot_policy['models'],
            'max_budget': limits['monthly_budget_usd'], 'budget_duration': '30d',
            'rpm_limit': limits['rpm'], 'tpm_limit': limits['tpm'],
            'metadata': {'environment': 'e2e', 'purpose': purpose, 'policy': 'pilot'},
        }))
        ctx = {'team_id': team['team_id'], 'users': [], 'keys': []}
        created.append(ctx)  # Register immediately so partial provisioning is cleaned up.
        for user_number in range(2):
            uid = f'{prefix}{suffix}-{user_number}'
            admin_client.expect_json(admin_client.post('/user/new', json={
                'user_id': uid, 'user_role': 'internal_user', 'auto_create_key': False,
            }))
            member = {'team_id': ctx['team_id'], 'member': {'role': 'user', 'user_id': uid}}
            if budget is not None:
                member.update(max_budget_in_team=budget, budget_duration=member_duration)
            admin_client.expect_json(admin_client.post('/team/member_add', json=member))
            ctx['users'].append(uid)
            for key_number in range(2):
                payload = {'team_id': ctx['team_id'], 'user_id': uid,
                           'key_alias': f'{prefix}{suffix}-{user_number}-{key_number}',
                           'models': ['all-team-models'],
                           'metadata': {'environment': 'e2e', 'purpose': purpose}}
                if first_key_budget is not None and user_number == key_number == 0:
                    payload.update(max_budget=first_key_budget, budget_duration='30d')
                data = admin_client.expect_json(admin_client.post('/key/generate', json=payload))
                ctx['keys'].append({'virtual_key': RedactedKey(data['key']), 'user_id': uid,
                                    'client': LiteLLMClient(base_url, data['key'])})
        return ctx

    try:
        yield create
    finally:
        errors = []
        for ctx in created:
            for key in ctx['keys']:
                try:
                    data = admin_client.expect_json(admin_client.post(
                        '/key/block', json={'key': key['virtual_key']}))
                    if data.get('blocked') is not True:
                        errors.append('key block not confirmed')
                except Exception as exc:
                    errors.append('key cleanup: '+type(exc).__name__)
            try:
                data = admin_client.expect_json(admin_client.post('/team/update', json={
                    'team_id': ctx['team_id'], 'blocked': True}))
                if admin_client.team_info(ctx['team_id'])['team_info'].get('blocked') is not True:
                    errors.append('team block not confirmed')
            except Exception as exc:
                errors.append('team cleanup: '+type(exc).__name__)
        if errors:
            pytest.fail('Pilot fixture cleanup failed: '+'; '.join(errors), pytrace=False)


@pytest.fixture(scope="module")
def opencode_developer(admin_client, base_url, pilot_policy):
    """Exercise the real operator onboarding script, including partial-failure cleanup."""
    workspace = Path(__file__).resolve().parents[2]
    suffix = uuid.uuid4().hex[:8]
    user_id = f"e2e-p1112-{suffix}"
    team_id = None
    try:
        limits = pilot_policy["limits"]["team"]
        team_id = admin_client.create_team(
            team_alias=user_id, models=pilot_policy["models"],
            rpm_limit=limits["rpm"], tpm_limit=limits["tpm"],
            max_budget=limits["monthly_budget_usd"], budget_duration="30d",
        )["team_id"]
        env = dict(os.environ)
        env["LLM_GATEWAY_ENV_FILE"] = os.getenv(
            "E2E_ENV_FILE", str(workspace / "llm-gateway-infra/.env"))
        result = subprocess.run(
            ["bash", str(workspace / "llm-gateway-infra/scripts/onboard-developer.sh"),
             user_id, team_id, "pilot"],
            env=env, capture_output=True, text=True, timeout=200, check=False,
        )
        if result.returncode:
            pytest.fail(f"Operator onboarding failed (exit {result.returncode}); output suppressed", pytrace=False)
        candidates = re.findall(r"^sk-[A-Za-z0-9_-]+$", result.stdout, re.MULTILINE)
        if len(candidates) != 1:
            pytest.fail("Onboarding did not return exactly one virtual key; output suppressed", pytrace=False)
        key = RedactedKey(candidates[0])
        yield {"team_id": team_id, "user_id": user_id, "virtual_key": key,
               "client": LiteLLMClient(base_url, key)}
    finally:
        if team_id:
            errors = []
            try:
                summary = admin_client.offboard_user_keys(user_id=user_id)
                # Re-discovery confirms no unblocked key was left by a partial CLI run.
                keys = admin_client.list_user_keys(user_id=user_id)
                if any(item.get("blocked") is not True for item in keys):
                    errors.append("unblocked developer key remains")
                print("P1_OPENCODE_CLEANUP " + json.dumps(summary))
            except Exception as exc:
                errors.append("developer key cleanup: " + type(exc).__name__)
            try:
                admin_client.expect_json(admin_client.post(
                    "/team/update", json={"team_id": team_id, "blocked": True}))
                if admin_client.team_info(team_id)["team_info"].get("blocked") is not True:
                    errors.append("team block not confirmed")
            except Exception as exc:
                errors.append("team cleanup: " + type(exc).__name__)
            if errors:
                pytest.fail("OpenCode fixture cleanup failed: " + "; ".join(errors), pytrace=False)


@pytest.fixture()
def opencode_project(tmp_path, opencode_developer, base_url):
    executable = shutil.which("opencode")
    if not executable:
        pytest.fail("Existing OpenCode CLI is required for agent acceptance", pytrace=False)
    template_path = Path(__file__).resolve().parents[2] / "llm-gateway-config/clients/opencode/opencode.jsonc"
    template = json.loads(template_path.read_text())
    project = tmp_path / "project"
    prepare_project(project, template, base_url)
    return {"path": project, "executable": executable,
            "env": cli_environment(tmp_path / "cli-state", opencode_developer["virtual_key"])}
```

## 3. llm-gateway-e2e/tests/test_limits.py

SHA-256: `a2806fb8a669f3d024ab06f87e58a2546c6d793f4392640544725293daccaf63`

```python
import pytest
import time

from tests.client import LiteLLMClient


@pytest.mark.live
@pytest.mark.limits
def test_team_rpm_limit_is_enforced(
    rpm_user_client: LiteLLMClient,
    rpm_limited_identity: dict,
    fast_model: str,
):
    assert rpm_limited_identity["rpm_limit"] == 2

    payload = {
        "model": fast_model,
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: ok",
            }
        ],
        "max_tokens": 8,
    }

    responses = []

    for request_number in range(1, 4):
        response = rpm_user_client.post(
            "/v1/chat/completions",
            json=payload,
        )

        print(
            f"request #{request_number}: "
            f"{response.status_code}"
        )

        responses.append(response)

    statuses = [
        response.status_code
        for response in responses
    ]

    assert statuses[0] == 200, (
        "First request should be allowed. "
        f"statuses={statuses}"
    )

    assert statuses[1] == 200, (
        "Second request should be allowed. "
        f"statuses={statuses}"
    )

    assert statuses[2] == 429, (
        "Third request should be rate limited. "
        f"statuses={statuses}. "
        "response body suppressed"
    )


@pytest.mark.live
@pytest.mark.limits
def test_key_budget_is_enforced(
    admin_client: LiteLLMClient,
    budget_user_client: LiteLLMClient,
    budget_limited_identity: dict,
    fast_model: str,
):
    virtual_key = budget_limited_identity["virtual_key"]
    max_budget = budget_limited_identity["max_budget"]

    payload = {
        "model": fast_model,
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: ok",
            }
        ],
        "max_tokens": 8,
    }

    #
    # First request should be accepted because
    # key spend starts at zero.
    #

    first = budget_user_client.post(
        "/v1/chat/completions",
        json=payload,
    )

    assert first.status_code == 200, (
        "First request should be allowed. "
        f"status={first.status_code}, "
        "response body suppressed"
    )

    #
    # Spend persistence is asynchronous.
    #
    # Poll /key/info until recorded spend has
    # crossed the tiny key budget.
    #

    deadline = time.time() + 20
    current_spend = 0.0

    while time.time() < deadline:
        response = admin_client.get(
            "/key/info",
            params={
                "key": virtual_key,
            },
        )

        info_data = admin_client.expect_json(response)

        info = info_data.get(
            "info",
            {},
        )

        current_spend = float(
            info.get("spend") or 0
        )

        if current_spend >= max_budget:
            break

        time.sleep(1)

    assert current_spend >= max_budget, (
        "Spend was not persisted before timeout. "
        f"current_spend={current_spend}, "
        f"max_budget={max_budget}"
    )

    #
    # Key has now exceeded its budget.
    # v1.104.0 default behavior = HTTP 422.
    #

    second = budget_user_client.post(
        "/v1/chat/completions",
        json=payload,
    )

    assert second.status_code == 422, (
        "Expected exhausted key budget to be rejected "
        "with HTTP 422. "
        f"status={second.status_code}, "
        "response body suppressed"
    )


@pytest.mark.live
@pytest.mark.limits
def test_blocked_key_is_rejected(
    admin_client: LiteLLMClient,
    user_client: LiteLLMClient,
    e2e_identity: dict,
    fast_model: str,
):
    payload = {
        "model": fast_model,
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: ok",
            }
        ],
        "max_tokens": 8,
    }

    #
    # 1. Key harus aktif sebelum diblok.
    #

    before = user_client.post(
        "/v1/chat/completions",
        json=payload,
    )

    assert before.status_code == 200, (
        "Virtual key should work before blocking. "
        f"status={before.status_code}, "
        "response body suppressed"
    )

    #
    # 2. Block key yang sama.
    #

    response = admin_client.post(
        "/key/block",
        json={
            "key": e2e_identity["virtual_key"],
        },
    )

    admin_client.expect_json(response)

    #
    # 3. Key yang sama sekarang harus ditolak.
    #

    after = user_client.post(
        "/v1/chat/completions",
        json=payload,
    )

    assert after.status_code in {
        401,
        403,
    }, (
        "Blocked virtual key was still accepted. "
        f"status={after.status_code}, "
        "response body suppressed"
    )
```

## 4. llm-gateway-e2e/tests/test_failure_semantics.py

SHA-256: `d7a8cae32977f254579309db37868a65d5429351be5ea626188965823740aa4d`

```python
"""Gateway rejects dangerous simulation parameters; the same key still works."""
import json
import time

import pytest


FAULTS = {
    "rate_limit": ({"mock_testing_rate_limit_error": True}, 400),
    "server_error": ({"mock_testing_fallbacks": True}, 400),
    "timeout": ({"mock_timeout": True, "mock_response": "unused",
                 "timeout": 0.05, "request_timeout": 0.05}, 400),
}


@pytest.mark.live
@pytest.mark.parametrize("alias", ["company-fast", "company-coding"])
@pytest.mark.parametrize("fault", list(FAULTS))
def test_fault_injection_parameters_are_rejected(pilot_identity_factory, alias, fault):
    ctx = pilot_identity_factory(prefix="e2e-p113-", purpose="P1-13-native-fault")
    client = ctx["keys"][0]["client"]
    injection, expected_status = FAULTS[fault]
    started = time.monotonic()
    response = client.post("/v1/chat/completions", json={
        "model": alias, "messages": [{"role": "user", "content": "Controlled fault test."}],
        "max_tokens": 8, "num_retries": 0, "disable_fallbacks": True, **injection,
    })
    elapsed = time.monotonic() - started
    assert response.status_code == expected_status, f"Dangerous {fault} parameter was not rejected: HTTP {response.status_code}"
    error = response.json().get("error")
    assert isinstance(error, dict), "Expected OpenAI-compatible error object"
    assert isinstance(error.get("message"), str) and error["message"], "Missing error message"
    assert "mock" in error["message"].lower(), "Request was rejected for an unrelated reason"
    assert isinstance(error.get("type"), str) and error["type"], "Missing error type"
    assert "choices" not in response.json(), "A failed request must not look successful"
    assert elapsed < 30, "Fault request exceeded the bounded scenario"
    # Removing request-local injection must restore real inference on the same credential.
    recovery = client.post("/v1/chat/completions", json={
        "model": alias, "messages": [{"role": "user", "content": "Reply exactly: ok"}],
        "max_tokens": 16, "reasoning_effort": "none",
    })
    assert recovery.status_code == 200, f"Recovery failed: HTTP {recovery.status_code}"
    body = recovery.json()
    assert "ok" in body["choices"][0]["message"]["content"].lower()
    assert body["usage"]["completion_tokens"] > 0
    print("P1_NATIVE_FAULT " + json.dumps({
        "alias": alias, "fault": fault, "status": response.status_code,
        "elapsed_seconds": round(elapsed, 3), "recovery_status": recovery.status_code,
        "error_type": error["type"], "simulation": "rejected-by-runtime-security-guard",
    }))
```

## 5. llm-gateway-e2e/tests/native_failure_probe.py

SHA-256: `875fe8aef7d4a356628be79090d85a13a523e110c16a8bd92892ddddd59e246e`

```python
"""Run via docker exec -i existing-gateway python -; no server or provider I/O."""


def main():
    import asyncio
    import copy
    import json
    import logging
    from pathlib import Path
    from unittest.mock import AsyncMock, patch

    logging.disable(logging.CRITICAL)
    import litellm
    import yaml
    from litellm.proxy._types import ProxyException, UserAPIKeyAuth
    from litellm.proxy.common_request_processing import ProxyBaseLLMRequestProcessing
    from litellm.proxy.proxy_server import openai_exception_handler
    from starlette.requests import Request

    config = yaml.safe_load(Path("/app/config.yaml").read_text())
    retries = config["litellm_settings"]["num_retries"]
    assert retries == 2, "Reviewed retry setting changed"
    aliases = {entry["model_name"] for entry in config["model_list"]}
    assert aliases == {"company-fast", "company-coding"}

    async def run():
        results = []
        for alias in sorted(aliases):
            for kind, kwargs, status in (
                ("rate_limit", {"mock_response": "litellm.RateLimitError"}, 429),
                ("server_error", {"mock_response": "litellm.InternalServerError"}, 500),
                ("timeout", {"mock_response": "unused", "mock_timeout": True, "timeout": 0.01}, 408),
            ):
                caught = None
                try:
                    await litellm.acompletion(
                        model="openai/gpt-5.6-terra" if alias == "company-fast" else "openai/gpt-5.6-sol",
                        api_key="native-probe-no-secret", num_retries=0,
                        messages=[{"role": "user", "content": "Native fault probe."}], **kwargs,
                    )
                except Exception as error:
                    caught = error
                assert caught is not None and caught.status_code == status, "SDK fault was not observed"
                processor = ProxyBaseLLMRequestProcessing(data={"model": alias, "metadata": {}})
                logger = type("FailureLogger", (), {
                    "post_call_failure_hook": AsyncMock(return_value=None),
                    "post_call_response_headers_hook": AsyncMock(return_value={}),
                })()
                translated = None
                try:
                    await processor._handle_llm_api_exception(
                        caught, UserAPIKeyAuth(user_id="native-fixture", team_id="native-fixture"), logger)
                except ProxyException as error:
                    translated = error
                assert translated is not None, "Native proxy did not translate the error"
                request = Request({"type": "http", "method": "POST", "path": "/v1/chat/completions", "headers": []})
                response = await openai_exception_handler(request, translated)
                body = json.loads(response.body)
                assert response.status_code == status and isinstance(body.get("error"), dict)
                assert body["error"].get("type") and body["error"].get("message")
                assert "choices" not in body
                results.append({"alias": alias, "case": kind, "http_status": response.status_code,
                                "error_type": body["error"]["type"], "scope": "native-sdk-and-proxy-handler"})

        models = copy.deepcopy(config["model_list"])
        for entry in models:
            entry["litellm_params"]["api_key"] = "native-probe-no-secret"
        router = litellm.Router(model_list=models, num_retries=retries, retry_after=0)
        for kind, exception_type, failures, expect_success, expected_attempts in (
            ("transient_500", litellm.InternalServerError, 2, True, 3),
            ("persistent_500", litellm.InternalServerError, 9, False, 3),
            ("transient_429", litellm.RateLimitError, 2, True, 3),
            ("persistent_429", litellm.RateLimitError, 9, False, 3),
            ("transient_timeout", litellm.Timeout, 2, True, 3),
            ("persistent_timeout", litellm.Timeout, 9, False, 3),
            ("bad_request", litellm.BadRequestError, 9, False, 1),
        ):
            attempts = 0

            async def upstream(*args, **kwargs):
                nonlocal attempts
                attempts += 1
                if attempts <= failures:
                    raise exception_type(message="Controlled native fault", model="company-fast", llm_provider="openai")
                return litellm.ModelResponse(model="company-fast")

            succeeded = False
            metadata = {"model_group": "company-fast"}
            with patch("asyncio.sleep", new=AsyncMock()):
                try:
                    await router.async_function_with_retries(
                        original_function=upstream, model="company-fast", num_retries=retries, metadata=metadata)
                    succeeded = True
                except exception_type:
                    pass
            assert succeeded is expect_success and attempts == expected_attempts, "Native retry contract changed"
            assert metadata["attempted_retries"] == expected_attempts - 1, "Retry metadata differs from actual calls"
            results.append({"case": kind, "attempts": attempts, "succeeded": succeeded,
                            "scope": "native-router-fault-boundary"})
        router.discard()
        print(json.dumps({"status": "PASS", "num_retries": retries, "cases": results,
                          "provider_requests": 0, "gateway_config_changed": False}))

    asyncio.run(run())


if __name__ == "__main__":
    main()
```

## 6. llm-gateway-e2e/tests/maintenance.py

SHA-256: `2f1205c7220ac0c8be25ac0ae3be4fb448dc211e880942c1330c9f53bb93f26e`

```python
"""Bounded maintenance of existing dependencies; never creates a container."""
from contextlib import contextmanager
import json
import os
import subprocess
import time
from urllib.parse import urlsplit


DEPENDENCIES = {"postgres": "llm-gateway-postgres", "redis": "llm-gateway-redis"}


def docker(*args):
    result = subprocess.run(["docker", *args], capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError("Existing-container operation failed; raw output suppressed")
    return result.stdout.strip()


def inspect(name):
    data = json.loads(docker("inspect", "--format", "{{json .}}", name))
    return {"id": data["Id"], "running": data["State"]["Running"]}


@contextmanager
def stopped_dependency(dependency, base_url):
    url = urlsplit(base_url)
    if os.getenv("E2E_ALLOW_EXISTING_OUTAGE") != "1":
        raise RuntimeError("Use the explicit existing-maintenance runner for outage tests")
    if url.hostname not in {"localhost", "127.0.0.1", "::1"} or url.port != 4000:
        raise RuntimeError("Maintenance is restricted to the existing local gateway4000")
    if dependency not in DEPENDENCIES:
        raise RuntimeError("Unsupported dependency")
    name = DEPENDENCIES[dependency]
    gateway = inspect("llm-gateway")
    before = inspect(name)
    if not gateway["running"] or not before["running"]:
        raise RuntimeError("Gateway and dependency must already be running")
    started = time.monotonic()
    try:
        docker("stop", "--time", "5", name)
        assert inspect(name)["running"] is False, "Dependency did not stop"
        yield
    finally:
        docker("start", name)
        deadline = time.monotonic() + 60
        recovered = False
        while time.monotonic() < deadline:
            state = inspect(name)
            try:
                if dependency == "postgres":
                    ready = docker("exec", name, "pg_isready")
                    recovered = "accepting connections" in ready
                else:
                    recovered = docker("exec", name, "redis-cli", "ping") == "PONG"
            except RuntimeError:
                recovered = False
            if recovered:
                break
            time.sleep(1)
        assert recovered, "Dependency did not recover"
        assert state["id"] == before["id"], "Dependency identity changed"
        assert inspect("llm-gateway") == gateway, "Gateway identity/state changed"
        print("P1_OUTAGE_RECOVERY " + json.dumps({"dependency": dependency, "recovered": True,
              "same_container_ids": True, "seconds": round(time.monotonic() - started, 2)}))
```

## 7. llm-gateway-e2e/tests/test_dependency_outage.py

SHA-256: `a13a7e731a974113dad21e31153563aa4d0e3dce7b66b1a0ac3c7b01f926577c`

```python
"""Explicit maintenance gate: negative auth/ACL/budget and retained accounting."""
import json
import time

import pytest

from tests.client import LiteLLMClient


def chat(client, alias="company-fast"):
    return client.post("/v1/chat/completions", json={"model": alias,
        "messages": [{"role": "user", "content": "Reply exactly: ok"}],
        "max_tokens": 16, "reasoning_effort": "none"})


@pytest.mark.live
@pytest.mark.outage
@pytest.mark.parametrize("dependency", ["postgres", "redis"])
def test_dependency_outage_preserves_denials_and_recovers(
        admin_client, base_url, pilot_identity_factory, dependency_outage, dependency):
    valid = pilot_identity_factory(prefix="e2e-outage-", purpose="P1-13-outage")
    denied = pilot_identity_factory(prefix="e2e-outage-", purpose="P1-13-outage")
    budget = pilot_identity_factory(prefix="e2e-outage-", purpose="P1-13-outage", first_key_budget=0.000001)
    active = valid["keys"][0]["client"]
    cold = valid["keys"][1]["client"]
    blocked = valid["keys"][2]
    denied_client = denied["keys"][0]["client"]
    exhausted = budget["keys"][0]
    assert chat(exhausted["client"]).status_code == 200
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if (admin_client.key_info(exhausted["virtual_key"]).get("spend") or 0) > 0.000001:
            break
        time.sleep(1)
    assert chat(exhausted["client"]).status_code == 422
    admin_client.expect_json(admin_client.post("/key/block", json={"key": blocked["virtual_key"]}))
    admin_client.expect_json(admin_client.post("/team/update", json={
        "team_id": denied["team_id"], "models": ["company-fast"]}))
    # Expire the cold token's native60s cache, then warm only the intended grants.
    time.sleep(65)
    assert active.get("/v1/models").status_code == 200
    assert chat(blocked["client"]).status_code in {401, 403}
    assert chat(denied_client, "company-coding").status_code == 403
    assert chat(exhausted["client"]).status_code == 422
    invalid = LiteLLMClient(base_url, "sk-invalid-outage-fixture", timeout=20)
    expected_ids = []
    statuses = {}
    for item in (active, cold, blocked["client"], denied_client, exhausted["client"]):
        item.timeout = 20
    with dependency_outage(dependency):
        for label, client, alias in (
            ("cold", cold, "company-fast"), ("invalid", invalid, "company-fast"),
            ("blocked", blocked["client"], "company-fast"),
            ("denied", denied_client, "company-coding"),
            ("exhausted", exhausted["client"], "company-fast"),
        ):
            response = chat(client, alias)
            statuses[label] = response.status_code
            if label == "cold" and dependency == "redis":
                assert response.status_code == 200
                expected_ids.append(response.json()["id"])
            else:
                allowed = ({401, 403, 422, 503} if dependency == "postgres" else
                           ({403} if label == "denied" else {422} if label == "exhausted" else {401, 403}))
                assert response.status_code in allowed, "Negative/cold access was unexpectedly accepted or returned the wrong error"
                assert "error" in response.json()
        # Pinned existing configuration denies warm grants when PostgreSQL is down.
        # Redis is not configured as native cache here, so it must not affect inference.
        warm = chat(active)
        statuses["warm"] = warm.status_code
        assert warm.status_code == (503 if dependency == "postgres" else 200)
        if warm.status_code == 200:
            expected_ids.append(warm.json()["id"])
    deadline = time.monotonic() + 90
    ready = False
    while time.monotonic() < deadline:
        try:
            ready = admin_client.get("/health/readiness").status_code == 200
        except Exception:
            ready = False
        if ready:
            break
        time.sleep(1)
    assert ready, "Gateway did not recover readiness"
    assert chat(blocked["client"]).status_code in {401, 403}, "Blocked key changed after recovery"
    assert chat(denied_client, "company-coding").status_code == 403, "ACL changed after recovery"
    assert chat(exhausted["client"]).status_code == 422, "Exhausted budget changed after recovery"
    for alias in ("company-fast", "company-coding"):
        response = chat(active, alias)
        assert response.status_code == 200, "Real provider recovery failed"
        expected_ids.append(response.json()["id"])
    deadline = time.monotonic() + 45
    persisted = set()
    while time.monotonic() < deadline:
        page = admin_client.list_user_spend_logs_page(user_id=valid["users"][0],
            start_date="2026-01-01 00:00:00", end_date="2099-01-01 00:00:00")
        persisted = {row["request_id"] for row in page["data"] if row.get("spend", 0) > 0}
        if set(expected_ids) <= persisted:
            break
        time.sleep(1)
    assert set(expected_ids) <= persisted, "An accepted outage/recovery request lost its spend record"
    print("P1_DEPENDENCY_OUTAGE " + json.dumps({"dependency": dependency, "statuses": statuses,
          "recovered_aliases": ["company-fast", "company-coding"], "accepted_requests_persisted": True}))
```

## 8. llm-gateway-e2e/tests/test_key_rotation.py

SHA-256: `d8981aafad6fa0409814a2ac06ba2da679ad9abb5a54f9f11d8431d6a7a140ce`

```python
"""Rotate disposable virtual keys without deleting native identity or spend history."""
import json
import time
import uuid

import pytest

from tests.client import LiteLLMClient, RedactedKey


def infer(client, alias):
    return client.post("/v1/chat/completions", json={
        "model": alias, "messages": [{"role": "user", "content": "Reply exactly: ok"}],
        "max_tokens": 16, "reasoning_effort": "none",
    })


@pytest.mark.live
@pytest.mark.parametrize("alias", ["company-fast", "company-coding"])
def test_virtual_key_rotation_preserves_scope_and_audit(
        admin_client, base_url, pilot_identity_factory, alias):
    identity = pilot_identity_factory(prefix="e2e-rotate-", purpose="P1-16-rotation",
                                      first_key_budget=0.01)
    old = identity["keys"][0]
    before = infer(old["client"], alias)
    assert before.status_code == 200, "Original key did not work"
    request_ids = [before.json()["id"]]
    original = admin_client.key_info(old["virtual_key"])
    fields = ("user_id", "team_id", "models", "max_budget", "budget_duration",
              "rpm_limit", "tpm_limit")
    payload = {field: original[field] for field in fields if original.get(field) is not None}
    payload.update(key_alias="e2e-rotate-replacement-" + uuid.uuid4().hex[:8],
                   metadata={"environment": "e2e", "purpose": "P1-16-rotation"})
    replacement = admin_client.expect_json(admin_client.post("/key/generate", json=payload))
    new = {"virtual_key": RedactedKey(replacement["key"]), "user_id": old["user_id"],
           "client": LiteLLMClient(base_url, replacement["key"])}
    identity["keys"].append(new)  # Register before verification, including partial failure.
    assert new["virtual_key"] != old["virtual_key"], "Rotation returned the old credential"
    replacement_info = admin_client.key_info(new["virtual_key"])
    for field in fields:
        assert replacement_info.get(field) == original.get(field), "Replacement scope changed: " + field
    assert new["client"].get("/v1/models").status_code == 200
    accepted = infer(new["client"], alias)
    assert accepted.status_code == 200, "Replacement failed before cutover"
    request_ids.append(accepted.json()["id"])
    admin_client.expect_json(admin_client.post("/key/block", json={"key": old["virtual_key"]}))
    assert admin_client.key_info(old["virtual_key"])["blocked"] is True
    assert infer(old["client"], alias).status_code in {401, 403}, "Old key remained valid"
    accepted = infer(new["client"], alias)
    assert accepted.status_code == 200, "Replacement failed after cutover"
    request_ids.append(accepted.json()["id"])
    deadline = time.monotonic() + 45
    persisted = set()
    old_spend = new_spend = team_spend = 0
    while time.monotonic() < deadline:
        page = admin_client.list_user_spend_logs_page(user_id=old["user_id"],
            start_date="2026-01-01 00:00:00", end_date="2099-01-01 00:00:00")
        persisted = {row["request_id"] for row in page["data"] if row.get("spend", 0) > 0}
        # Native spend rows and aggregate counters flush asynchronously, separately.
        old_spend = admin_client.key_info(old["virtual_key"])["spend"]
        new_spend = admin_client.key_info(new["virtual_key"])["spend"]
        team_spend = admin_client.team_info(identity["team_id"])["team_info"]["spend"]
        if set(request_ids) <= persisted and min(old_spend, new_spend, team_spend) > 0:
            break
        time.sleep(1)
    assert set(request_ids) <= persisted, "Rotation lost an accepted request's spend history"
    assert len(admin_client.list_user_keys(user_id=old["user_id"])) == 3, "Key history was deleted"
    assert old_spend > 0, "Old key spend was lost"
    assert new_spend > 0, "New key spend was lost"
    assert team_spend > 0, "Team spend was lost"
    print("P1_KEY_ROTATION " + json.dumps({"alias": alias, "old_denied": True,
          "new_accepted": True, "same_scope": True, "records_and_spend_retained": True}))
```

## 9. llm-gateway-e2e/tests/unit/test_fixture_cleanup.py

SHA-256: `e75e65f577095f34e94c52d297568c4e7ab0d335f4f0bc01889f5e4066ea6f1f`

```python
from unittest.mock import Mock

import pytest

from tests.conftest import identity_cleanup


pytestmark = pytest.mark.unit


def configured_client(offline_client, json_response):
    offline_client.offboard_user_keys = Mock(return_value={"blocked_count": 1})
    offline_client.list_user_keys = Mock(return_value=[{"blocked": True}])
    offline_client.post.side_effect = None
    offline_client.post.return_value = json_response({"ok": True})
    offline_client.team_info = Mock(return_value={"team_info": {"blocked": True}})
    return offline_client


def test_cleanup_runs_for_identity_registered_before_setup_failure(offline_client, json_response):
    client = configured_client(offline_client, json_response)
    teardown = identity_cleanup.__wrapped__(client)
    register = next(teardown)
    register("fixture-team", "fixture-user")
    # Owner fixture may fail after registration and before yielding a virtual key.
    with pytest.raises(StopIteration):
        next(teardown)
    client.offboard_user_keys.assert_called_once_with(user_id="fixture-user")
    client.post.assert_called_once_with("/team/update", json={"team_id": "fixture-team", "blocked": True})


@pytest.mark.parametrize("fault", ["offboard-error", "key-not-blocked", "team-not-blocked", "team-http-error"])
def test_cleanup_failure_is_visible_and_preserves_team_attempt(offline_client, json_response, fault):
    client = configured_client(offline_client, json_response)
    if fault == "offboard-error":
        client.offboard_user_keys.side_effect = RuntimeError("private-unit-placeholder")
    elif fault == "key-not-blocked":
        client.list_user_keys.return_value = [{"blocked": False}]
    elif fault == "team-not-blocked":
        client.team_info.return_value = {"team_info": {"blocked": False}}
    else:
        client.post.return_value = json_response({"detail": "private-unit-placeholder"}, status=500)
    teardown = identity_cleanup.__wrapped__(client)
    next(teardown)("fixture-team", "fixture-user")
    with pytest.raises(pytest.fail.Exception) as error:
        next(teardown)
    assert "private-unit-placeholder" not in str(error.value)
    assert client.post.call_count == 1
```

## 10. llm-gateway-e2e/tests/unit/test_transport_privacy.py

SHA-256: `7cdc23828b76ee86ee854bcfcf89858bd732450311f9148006b50cbcd143b5b1`

```python
import pytest
import requests

from tests.client import GatewayTransportError, LiteLLMClient


pytestmark = pytest.mark.unit


@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize("exception", [requests.Timeout, requests.ConnectionError])
def test_transport_errors_suppress_credential_urls_and_bodies(monkeypatch, method, exception):
    value = "private-unit-credential-not-issued"

    def fail(*args, **kwargs):
        raise exception(f"http://gateway/key/info?key={value}; response body={value}")

    monkeypatch.setattr(requests, method, fail)
    client = LiteLLMClient("http://unused.invalid", value)
    with pytest.raises(GatewayTransportError) as error:
        getattr(client, method)("/key/info")
    assert value not in str(error.value)
    assert exception.__name__ in str(error.value)
    assert error.value.__suppress_context__ is True


def test_header_repr_hides_key_without_changing_http_value():
    value = "private-unit-credential-not-issued"
    client = LiteLLMClient("http://unused.invalid", value)
    assert client.headers["Authorization"] == "Bearer " + value
    assert value not in repr(client.headers)
```

## 11. llm-gateway-e2e/tests/unit/test_maintenance.py

SHA-256: `b0936db1915cc811cb833bc5cba1ce95a84a256081348554c09917b8e1775db3`

```python
import json

import pytest

from tests import maintenance


pytestmark = pytest.mark.unit


@pytest.mark.parametrize("dependency", ["postgres", "redis"])
def test_dependency_is_restored_after_test_assertion_fails(monkeypatch, dependency):
    monkeypatch.setenv("E2E_ALLOW_EXISTING_OUTAGE", "1")
    name = maintenance.DEPENDENCIES[dependency]
    running = {"llm-gateway": True, name: True}
    calls = []

    def docker(*args):
        calls.append(args)
        if args[0] == "inspect":
            target = args[-1]
            return json.dumps({"Id": "existing-" + target, "State": {"Running": running[target]}})
        if args[0] == "stop":
            running[name] = False
        elif args[0] == "start":
            running[name] = True
        elif args[0] == "exec":
            return "accepting connections" if dependency == "postgres" else "PONG"
        return ""

    monkeypatch.setattr(maintenance, "docker", docker)
    with pytest.raises(AssertionError, match="intentional unit assertion"):
        with maintenance.stopped_dependency(dependency, "http://localhost:4000"):
            assert running[name] is False
            raise AssertionError("intentional unit assertion")
    assert running[name] is True
    assert sum(call[0] == "stop" for call in calls) == 1
    assert sum(call[0] == "start" for call in calls) == 1


@pytest.mark.parametrize("base_url,enabled", [
    ("http://localhost:4000", False),
    ("https://external.invalid:4000", True),
    ("http://localhost:4001", True),
])
def test_maintenance_refuses_unapproved_or_remote_target(monkeypatch, base_url, enabled):
    monkeypatch.setenv("E2E_ALLOW_EXISTING_OUTAGE", "1" if enabled else "0")
    calls = []
    monkeypatch.setattr(maintenance, "docker", lambda *args: calls.append(args))
    with pytest.raises(RuntimeError):
        with maintenance.stopped_dependency("postgres", base_url):
            pytest.fail("Unsafe maintenance target was accepted")
    assert calls == []
```

## 12. llm-gateway-e2e/tests/unit/test_opencode.py

SHA-256: `e29908e576b2741f235fb29eb5a1ef1ed689cda11090c22b2360a5e9fbffee76`

```python
import copy
import json
from pathlib import Path
import sys

import pytest

from tests.opencode import (
    assert_agent_workflow, cli_environment, parse_events, prepare_project, run_cli,
)


pytestmark = pytest.mark.unit
RECEIPT = {"status": "PASS", "receipt": "a" * 32}


def workflow():
    def tool(name, data, output="done"):
        return {"type": "tool_use", "part": {"tool": name, "state": {
            "status": "completed", "input": data, "output": output}}}
    return [tool("read", {"filePath": "calculator.py"}),
            tool("edit", {"filePath": "calculator.py"}),
            tool("shell", {"command": "python3 verify.py"}, json.dumps(RECEIPT)),
            {"type": "text", "part": {"text": "PASS " + RECEIPT["receipt"]}}]


def test_actual_tool_sequence_is_accepted():
    assert assert_agent_workflow(workflow(), RECEIPT)["receipt_consumed"] is True


@pytest.mark.parametrize("fault", [
    "text-only", "missing-read", "missing-edit", "shell-not-completed",
    "wrong-command", "wrong-tool-result", "wrong-final-receipt", "wrong-order",
])
def test_success_text_cannot_replace_actual_tool_result(fault):
    events = workflow()
    if fault == "text-only":
        events = events[-1:]
    elif fault == "missing-read":
        events = events[1:]
    elif fault == "missing-edit":
        events.pop(1)
    elif fault == "shell-not-completed":
        events[2]["part"]["state"]["status"] = "error"
    elif fault == "wrong-command":
        events[2]["part"]["state"]["input"]["command"] = "echo PASS"
    elif fault == "wrong-tool-result":
        events[2]["part"]["state"]["output"] = "PASS"
    elif fault == "wrong-final-receipt":
        events[-1]["part"]["text"] = "PASS " + "b" * 32
    elif fault == "wrong-order":
        events[-1], events[-2] = events[-2], events[-1]
    with pytest.raises(AssertionError):
        assert_agent_workflow(events, RECEIPT)


@pytest.mark.parametrize("output", ["not-json unit-credential", "[]", "", '{"type":"error","error":"unit-credential"}'])
def test_invalid_cli_events_fail_without_raw_output(output):
    with pytest.raises(AssertionError) as error:
        parse_events(output)
    assert "unit-credential" not in str(error.value)


def test_cli_failure_suppresses_stdout_and_stderr(tmp_path):
    with pytest.raises(AssertionError) as error:
        run_cli([sys.executable, "-c", "print('unit-credential'); raise SystemExit(4)"],
                cwd=tmp_path, env={"PATH": "/usr/bin:/bin"})
    assert "exit 4" in str(error.value)
    assert "unit-credential" not in str(error.value)


def test_cli_environment_does_not_inherit_admin_credentials(tmp_path, monkeypatch):
    monkeypatch.setenv("LITELLM_MASTER_KEY", "unit-admin-only")
    monkeypatch.setenv("OPENAI_API_KEY", "unit-provider-only")
    monkeypatch.setenv("OPENCODE_CONFIG", "/personal/settings.json")
    env = cli_environment(tmp_path, "unit-developer-only")
    assert not {"LITELLM_MASTER_KEY", "OPENAI_API_KEY", "OPENCODE_CONFIG"} & env.keys()
    assert env["COMPANY_LLM_API_KEY"] == "unit-developer-only"
    assert all(str(tmp_path) in env[f"XDG_{name}_HOME"] for name in ("DATA", "CONFIG", "STATE", "CACHE"))


def test_fixture_uses_real_template_without_mutating_it(tmp_path):
    # Unit CI checks out only E2E. Live acceptance loads the actual config sibling;
    # this unit checks transformation/permissions using the same public contract.
    template = {"model": "company-ai/company-coding", "providers": {"company-ai": {
        "env": ["COMPANY_LLM_API_KEY"], "settings": {"baseURL": "http://localhost:4000/v1"},
        "package": "@opencode/ai/providers/openai-compatible",
        "models": {"company-fast": {}, "company-coding": {}},
    }}}
    before = copy.deepcopy(template)
    config = prepare_project(tmp_path / "project", template, "http://localhost:4000")
    assert template == before
    assert set(config["providers"]) == {"company-ai"}
    assert set(config["providers"]["company-ai"]["models"]) == {"company-fast", "company-coding"}
    assert config["agents"]["build"]["steps"] == 8
    assert config["providers"]["company-ai"]["body"]["max_tokens"] == 768
    assert {"action": "external_directory", "resource": "*", "effect": "deny"} in config["permissions"]
```

## 13. llm-gateway-e2e/tests/unit/test_suite_validator.py

SHA-256: `4857ee10684b70477331931558d3f76bdf318eebd9e3c62209d958bc611870c4`

```python
from pathlib import Path
import subprocess
import sys

import pytest


pytestmark = pytest.mark.unit
ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("missing", [
    None,
    "test_multiple_user_keys_work_before_offboarding",
    "test_user_offboarding_blocks_all_keys",
    "test_pilot_policy_is_persisted",
    "test_team_rate_limits_are_shared_and_recover",
    "test_member_budget_is_shared_across_keys",
    "test_team_budget_blocks_all_members",
    "test_key_budget_does_not_block_other_keys",
    "test_member_budget_window_resets_without_losing_total_spend",
    "test_opencode_onboarding_uses_developer_key",
    "test_opencode_agent_reads_edits_runs_and_uses_tool_result",
    "test_fault_injection_parameters_are_rejected",
    "test_dependency_outage_preserves_denials_and_recovers",
    "test_virtual_key_rotation_preserves_scope_and_audit",
])
def test_validator_requires_each_lifecycle_test(tmp_path, missing):
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    replaced = False

    # Validate a disposable copy; never remove or rename the real tests.
    for source in (ROOT / "tests").glob("test_*.py"):
        content = source.read_text(encoding="utf-8")
        if missing and f"def {missing}(" in content:
            content = content.replace(f"def {missing}(", f"def removed_{missing}(")
            replaced = True
        (test_dir / source.name).write_text(content, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/ci/validate-suite.py")],
        cwd=tmp_path, capture_output=True, text=True, timeout=10,
        check=False,
    )

    if missing is None:
        assert result.returncode == 0, result.stderr
        assert "Required regression tests: PASS" in result.stdout
    else:
        assert replaced, "Required gateway test was already missing from the real suite"
        assert result.returncode != 0
        assert "required regression test(s) missing" in result.stderr
        assert missing in result.stderr
```

## 14. llm-gateway-e2e/scripts/ci/validate-suite.py

SHA-256: `1acd2d497e5fff34907b08e70e9771d70572a3c38994e98d8858140e76bedd00`

```python
#!/usr/bin/env python3

from __future__ import annotations

import ast
import sys
from pathlib import Path


TEST_DIR = Path("tests")


REQUIRED_TESTS = {
    "test_litellm_is_alive",
    "test_user_can_see_expected_models",
    "test_invalid_key_is_rejected",
    "test_company_fast_inference",
    "test_company_coding_inference",
    "test_streaming",
    "test_tool_calling",
    "test_team_policy_changes_without_key_rotation",
    "test_spend_is_attributed_to_user",
    "test_blocked_key_is_rejected",
    "test_team_rpm_limit_is_enforced",
    "test_key_budget_is_enforced",
    "test_multiple_user_keys_work_before_offboarding",
    "test_user_offboarding_blocks_all_keys",
    "test_pilot_policy_is_persisted",
    "test_team_rate_limits_are_shared_and_recover",
    "test_member_budget_is_shared_across_keys",
    "test_team_budget_blocks_all_members",
    "test_key_budget_does_not_block_other_keys",
    "test_member_budget_window_resets_without_losing_total_spend",
    "test_opencode_onboarding_uses_developer_key",
    "test_opencode_agent_reads_edits_runs_and_uses_tool_result",
    "test_fault_injection_parameters_are_rejected",
    "test_dependency_outage_preserves_denials_and_recovers",
    "test_virtual_key_rotation_preserves_scope_and_audit",
}


def fail(message: str) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    sys.exit(1)


if not TEST_DIR.exists():
    fail("tests directory not found")


test_files = sorted(
    TEST_DIR.rglob("test_*.py")
)


if not test_files:
    fail("no test files found")


print(
    f"Found {len(test_files)} test file(s)"
)


discovered_tests: set[str] = set()


for path in test_files:
    print(f"Inspecting: {path}")

    try:
        source = path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            source,
            filename=str(path),
        )

    except SyntaxError as exc:
        fail(
            f"Python syntax error in "
            f"{path}: {exc}"
        )

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            if node.name.startswith(
                "test_"
            ):
                discovered_tests.add(
                    node.name
                )


missing_tests = (
    REQUIRED_TESTS
    - discovered_tests
)


if missing_tests:
    fail(
        "required regression test(s) "
        "missing: "
        + ", ".join(
            sorted(missing_tests)
        )
    )


print()
print(
    f"Discovered "
    f"{len(discovered_tests)} "
    "test function(s)"
)

print(
    "Required regression tests: PASS"
)
```

## 15. llm-gateway-e2e/scripts/run-native.sh

SHA-256: `51eb333afb31a72f17843c849b5fd928582dd4bcdf177f4622ded54ecb1a2601`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GATEWAY_CONTAINER="${E2E_GATEWAY_CONTAINER:-llm-gateway}"

echo "Native LiteLLM fault/retry probe on the existing gateway container."
echo "No provider requests or gateway configuration changes."

exec docker exec --interactive "$GATEWAY_CONTAINER" python - \
    < "$REPO_ROOT/tests/native_failure_probe.py"
```

## 16. llm-gateway-e2e/scripts/run-outage.sh

SHA-256: `bc7449481c2dad02ecb85f14bac3a22db080fd0d2e15aa744dfb74908fdc657d`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "${1:-}" != "--confirm-existing-maintenance" ]; then
    echo "Usage: $0 --confirm-existing-maintenance (brief local dependency outage)" >&2
    exit 1
fi
shift
for dependency in llm-gateway-postgres llm-gateway-redis; do
    if [ "$(docker inspect --format '{{.State.Running}}' "$dependency")" != true ]; then
        echo "ERROR: dependencies must already be running" >&2
        exit 1
    fi
done
# Outer recovery guard complements the Python context manager and fixture cleanup.
recover() {
    docker start llm-gateway-postgres llm-gateway-redis >/dev/null
}
trap recover EXIT
export E2E_ALLOW_EXISTING_OUTAGE=1
export E2E_LIVE_MARKERS="live and outage"
"$SCRIPT_DIR/run-live.sh" tests/test_dependency_outage.py --tb=short -x -s "$@"
```

## 17. llm-gateway-e2e/scripts/run-all.sh

SHA-256: `212089e105c43d4b40fbe15a46683b8f06929d735fb7ec0c5f46b9ceccf423a7`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")" &&
    pwd
)"

INCLUDE_OUTAGE=false
if [ "${1:-}" = "--include-outage" ] && [ "$#" -eq 1 ]; then
    INCLUDE_OUTAGE=true
elif [ "$#" -ne 0 ]; then
    echo "Usage: $0 [--include-outage]" >&2
    exit 1
fi

"$SCRIPT_DIR/run-unit.sh"
"$SCRIPT_DIR/run-smoke.sh"
"$SCRIPT_DIR/run-native.sh"
"$SCRIPT_DIR/run-live.sh"
if [ "$INCLUDE_OUTAGE" = true ]; then
    "$SCRIPT_DIR/run-outage.sh" --confirm-existing-maintenance
else
    echo "Maintenance outage tests not selected; full release verification requires --include-outage."
fi
```

## 18. llm-gateway-e2e/scripts/run-live.sh

SHA-256: `dd6decb2ffb02a07b5ea96010a624700cf749c5abcc5fec16d4aa5bdfbb6b3ed`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")" &&
  pwd
)"

ROOT_DIR="$(
  cd "$SCRIPT_DIR/.." &&
  pwd
)"

ENV_FILE="${E2E_ENV_FILE:-$ROOT_DIR/../llm-gateway-infra/.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "ERROR: environment file not found:"
  echo "$ENV_FILE"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

export E2E_FAST_MODEL="${E2E_FAST_MODEL:-company-fast}"
export E2E_CODING_MODEL="${E2E_CODING_MODEL:-company-coding}"

cd "$ROOT_DIR"

echo "WARNING:"
echo "This test suite sends real requests to the LLM provider."
echo

python3 -m pytest \
    -v \
    -m "${E2E_LIVE_MARKERS:-live and not outage}" \
    "$@"
```

## 19. llm-gateway-e2e/pytest.ini

SHA-256: `78250e6bb8bfc186a2fc6ea9cd69c357005c22a626dab0b0dbdf75bf4d120a67`

```ini
[pytest]
testpaths = tests

addopts =
    -ra
    --strict-markers

markers =
    unit: offline regression tests; no gateway or provider requests
    live: sends real requests to an upstream LLM provider
    policy: modifies temporary LiteLLM team policy
    spend: validates asynchronous spend attribution
    limits: validates budget and rate-limit enforcement
    outage: explicitly stops/starts existing local dependencies; maintenance runner only
```

## 20. llm-gateway-e2e/.github/workflows/validate.yml

SHA-256: `0f46d999ec11abae4a7c3c599abc030ac7ab6ac968a8e73364b0972b8bda1b08`

```yaml
name: Validate E2E Suite

on:
  pull_request:

  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  validate:
    name: Validate E2E Suite
    runs-on: ubuntu-latest

    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"

          cache: "pip"
          cache-dependency-path: requirements.lock

      - name: Install ShellCheck
        run: |
          sudo apt-get update
          sudo apt-get install -y shellcheck

      - name: Install Python dependencies
        run: |
          python -m pip install --require-hashes -r requirements.lock

      - name: Validate E2E suite
        run: |
          ./scripts/ci/validate.sh
```

## 21. llm-gateway-infra/.github/workflows/validate.yml

SHA-256: `9f0cdd8817878118eaf686a464001d3904fa54c8e4690acdccb3aca9ff1bd905`

```yaml
name: Validate Infrastructure

on:
  pull_request:

  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  validate:
    name: Validate Infrastructure
    runs-on: ubuntu-latest

    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"

      - name: Install ShellCheck
        run: |
          sudo apt-get update
          sudo apt-get install -y shellcheck

      - name: Create CI environment
        run: |
          cat > .env <<'EOF'
          LITELLM_BASE_URL=http://localhost:4000

          LITELLM_MASTER_KEY=ci-master-placeholder
          LITELLM_SALT_KEY=ci-salt-placeholder

          POSTGRES_DB=litellm
          POSTGRES_USER=litellm
          POSTGRES_PASSWORD=ci-postgres-password

          DATABASE_URL=postgresql://litellm:ci-postgres-password@postgres:5432/litellm

          REDIS_HOST=redis
          REDIS_PORT=6379
          REDIS_PASSWORD=

          OPENAI_API_KEY=ci-provider-placeholder

          LLM_GATEWAY_CONFIG_DIR=../llm-gateway-config
          LITELLM_CONFIG_PATH=.github/fixtures/litellm_config.yaml

          HEALTHCHECK_API_KEY=ci-healthcheck-placeholder
          EOF

      - name: Install validation dependencies
        run: python -m pip install --require-hashes -r scripts/requirements.lock

      - name: Validate infrastructure
        run: |
          ./scripts/ci/validate.sh
```

## 22. llm-gateway-config/.github/workflows/validate.yml

SHA-256: `77f34be3701200920a19736bdbaa4e41e3da47c0e3b11937702623c5a646f792`

```yaml
name: Validate Config

on:
  pull_request:

  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  validate:
    name: Validate Config
    runs-on: ubuntu-latest

    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"

          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --require-hashes -r scripts/ci/requirements.lock

      - name: Validate config repository
        run: |
          ./scripts/ci/validate.sh
```

## 23. llm-gateway-config/scripts/ci/requirements.lock

SHA-256: `c9202ee0b7d35153154ac1cc5ae2a58891736f68dcea2fe766b74206ce6d6b7f`

```text
# Locked to the existing tested Python 3.12 environment; generated 2026-10-17.
# Source: scripts/ci/requirements.txt
# Install with: python3 -m pip install --require-hashes -r <this-file>

PyYAML==6.0.3 \
    --hash=sha256:00c4bdeba853cc34e7dd471f16b4114f4162dc03e6b7afcc2128711f0eca823c \
    --hash=sha256:0150219816b6a1fa26fb4699fb7daa9caf09eb1999f3b70fb6e786805e80375a \
    --hash=sha256:02893d100e99e03eda1c8fd5c441d8c60103fd175728e23e431db1b589cf5ab3 \
    --hash=sha256:02ea2dfa234451bbb8772601d7b8e426c2bfa197136796224e50e35a78777956 \
    --hash=sha256:0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6 \
    --hash=sha256:10892704fc220243f5305762e276552a0395f7beb4dbf9b14ec8fd43b57f126c \
    --hash=sha256:16249ee61e95f858e83976573de0f5b2893b3677ba71c9dd36b9cf8be9ac6d65 \
    --hash=sha256:1d37d57ad971609cf3c53ba6a7e365e40660e3be0e5175fa9f2365a379d6095a \
    --hash=sha256:1ebe39cb5fc479422b83de611d14e2c0d3bb2a18bbcb01f229ab3cfbd8fee7a0 \
    --hash=sha256:214ed4befebe12df36bcc8bc2b64b396ca31be9304b8f59e25c11cf94a4c033b \
    --hash=sha256:2283a07e2c21a2aa78d9c4442724ec1eb15f5e42a723b99cb3d822d48f5f7ad1 \
    --hash=sha256:22ba7cfcad58ef3ecddc7ed1db3409af68d023b7f940da23c6c2a1890976eda6 \
    --hash=sha256:27c0abcb4a5dac13684a37f76e701e054692a9b2d3064b70f5e4eb54810553d7 \
    --hash=sha256:28c8d926f98f432f88adc23edf2e6d4921ac26fb084b028c733d01868d19007e \
    --hash=sha256:2e71d11abed7344e42a8849600193d15b6def118602c4c176f748e4583246007 \
    --hash=sha256:34d5fcd24b8445fadc33f9cf348c1047101756fd760b4dacb5c3e99755703310 \
    --hash=sha256:37503bfbfc9d2c40b344d06b2199cf0e96e97957ab1c1b546fd4f87e53e5d3e4 \
    --hash=sha256:3c5677e12444c15717b902a5798264fa7909e41153cdf9ef7ad571b704a63dd9 \
    --hash=sha256:3ff07ec89bae51176c0549bc4c63aa6202991da2d9a6129d7aef7f1407d3f295 \
    --hash=sha256:41715c910c881bc081f1e8872880d3c650acf13dfa8214bad49ed4cede7c34ea \
    --hash=sha256:418cf3f2111bc80e0933b2cd8cd04f286338bb88bdc7bc8e6dd775ebde60b5e0 \
    --hash=sha256:44edc647873928551a01e7a563d7452ccdebee747728c1080d881d68af7b997e \
    --hash=sha256:4a2e8cebe2ff6ab7d1050ecd59c25d4c8bd7e6f400f5f82b96557ac0abafd0ac \
    --hash=sha256:4ad1906908f2f5ae4e5a8ddfce73c320c2a1429ec52eafd27138b7f1cbe341c9 \
    --hash=sha256:501a031947e3a9025ed4405a168e6ef5ae3126c59f90ce0cd6f2bfc477be31b7 \
    --hash=sha256:5190d403f121660ce8d1d2c1bb2ef1bd05b5f68533fc5c2ea899bd15f4399b35 \
    --hash=sha256:5498cd1645aa724a7c71c8f378eb29ebe23da2fc0d7a08071d89469bf1d2defb \
    --hash=sha256:5cf4e27da7e3fbed4d6c3d8e797387aaad68102272f8f9752883bc32d61cb87b \
    --hash=sha256:5e0b74767e5f8c593e8c9b5912019159ed0533c70051e9cce3e8b6aa699fcd69 \
    --hash=sha256:5ed875a24292240029e4483f9d4a4b8a1ae08843b9c54f43fcc11e404532a8a5 \
    --hash=sha256:5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b \
    --hash=sha256:5fdec68f91a0c6739b380c83b951e2c72ac0197ace422360e6d5a959d8d97b2c \
    --hash=sha256:6344df0d5755a2c9a276d4473ae6b90647e216ab4757f8426893b5dd2ac3f369 \
    --hash=sha256:64386e5e707d03a7e172c0701abfb7e10f0fb753ee1d773128192742712a98fd \
    --hash=sha256:652cb6edd41e718550aad172851962662ff2681490a8a711af6a4d288dd96824 \
    --hash=sha256:66291b10affd76d76f54fad28e22e51719ef9ba22b29e1d7d03d6777a9174198 \
    --hash=sha256:66e1674c3ef6f541c35191caae2d429b967b99e02040f5ba928632d9a7f0f065 \
    --hash=sha256:6adc77889b628398debc7b65c073bcb99c4a0237b248cacaf3fe8a557563ef6c \
    --hash=sha256:79005a0d97d5ddabfeeea4cf676af11e647e41d81c9a7722a193022accdb6b7c \
    --hash=sha256:7c6610def4f163542a622a73fb39f534f8c101d690126992300bf3207eab9764 \
    --hash=sha256:7f047e29dcae44602496db43be01ad42fc6f1cc0d8cd6c83d342306c32270196 \
    --hash=sha256:8098f252adfa6c80ab48096053f512f2321f0b998f98150cea9bd23d83e1467b \
    --hash=sha256:850774a7879607d3a6f50d36d04f00ee69e7fc816450e5f7e58d7f17f1ae5c00 \
    --hash=sha256:8d1fab6bb153a416f9aeb4b8763bc0f22a5586065f86f7664fc23339fc1c1fac \
    --hash=sha256:8da9669d359f02c0b91ccc01cac4a67f16afec0dac22c2ad09f46bee0697eba8 \
    --hash=sha256:8dc52c23056b9ddd46818a57b78404882310fb473d63f17b07d5c40421e47f8e \
    --hash=sha256:9149cad251584d5fb4981be1ecde53a1ca46c891a79788c0df828d2f166bda28 \
    --hash=sha256:93dda82c9c22deb0a405ea4dc5f2d0cda384168e466364dec6255b293923b2f3 \
    --hash=sha256:96b533f0e99f6579b3d4d4995707cf36df9100d67e0c8303a0c55b27b5f99bc5 \
    --hash=sha256:9c57bb8c96f6d1808c030b1687b9b5fb476abaa47f0db9c0101f5e9f394e97f4 \
    --hash=sha256:9c7708761fccb9397fe64bbc0395abcae8c4bf7b0eac081e12b809bf47700d0b \
    --hash=sha256:9f3bfb4965eb874431221a3ff3fdcddc7e74e3b07799e0e84ca4a0f867d449bf \
    --hash=sha256:a33284e20b78bd4a18c8c2282d549d10bc8408a2a7ff57653c0cf0b9be0afce5 \
    --hash=sha256:a80cb027f6b349846a3bf6d73b5e95e782175e52f22108cfa17876aaeff93702 \
    --hash=sha256:b30236e45cf30d2b8e7b3e85881719e98507abed1011bf463a8fa23e9c3e98a8 \
    --hash=sha256:b3bc83488de33889877a0f2543ade9f70c67d66d9ebb4ac959502e12de895788 \
    --hash=sha256:b865addae83924361678b652338317d1bd7e79b1f4596f96b96c77a5a34b34da \
    --hash=sha256:b8bb0864c5a28024fac8a632c443c87c5aa6f215c0b126c449ae1a150412f31d \
    --hash=sha256:ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc \
    --hash=sha256:bdb2c67c6c1390b63c6ff89f210c8fd09d9a1217a465701eac7316313c915e4c \
    --hash=sha256:c1ff362665ae507275af2853520967820d9124984e0f7466736aea23d8611fba \
    --hash=sha256:c2514fceb77bc5e7a2f7adfaa1feb2fb311607c9cb518dbc378688ec73d8292f \
    --hash=sha256:c3355370a2c156cffb25e876646f149d5d68f5e0a3ce86a5084dd0b64a994917 \
    --hash=sha256:c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5 \
    --hash=sha256:d0eae10f8159e8fdad514efdc92d74fd8d682c933a6dd088030f3834bc8e6b26 \
    --hash=sha256:d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f \
    --hash=sha256:ebc55a14a21cb14062aa4162f906cd962b28e2e9ea38f9b4391244cd8de4ae0b \
    --hash=sha256:eda16858a3cab07b80edaf74336ece1f986ba330fdb8ee0d6c0d68fe82bc96be \
    --hash=sha256:ee2922902c45ae8ccada2c5b501ab86c36525b883eff4255313a253a3160861c \
    --hash=sha256:efd7b85f94a6f21e4932043973a7ba2613b059c4a000551892ac9f1d11f5baf3 \
    --hash=sha256:f7057c9a337546edc7973c0d3ba84ddcdf0daa14533c2065749c9075001090e6 \
    --hash=sha256:fa160448684b4e94d80416c0fa4aac48967a969efe22931448d853ada8baf926 \
    --hash=sha256:fc09d0aa354569bc501d4e787133afc08552722d3ab34836a80547331bb5d4a0
```

## 24. llm-gateway-infra/scripts/requirements.lock

SHA-256: `bb1ddcc99e410fba8ab5a332aded0549b2cf214bb4bb63b8a1c83478a9573b7a`

```text
# Locked to the existing tested Python 3.12 environment; generated 2026-10-17.
# Source: scripts/requirements.txt
# Install with: python3 -m pip install --require-hashes -r <this-file>

PyYAML==6.0.3 \
    --hash=sha256:00c4bdeba853cc34e7dd471f16b4114f4162dc03e6b7afcc2128711f0eca823c \
    --hash=sha256:0150219816b6a1fa26fb4699fb7daa9caf09eb1999f3b70fb6e786805e80375a \
    --hash=sha256:02893d100e99e03eda1c8fd5c441d8c60103fd175728e23e431db1b589cf5ab3 \
    --hash=sha256:02ea2dfa234451bbb8772601d7b8e426c2bfa197136796224e50e35a78777956 \
    --hash=sha256:0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6 \
    --hash=sha256:10892704fc220243f5305762e276552a0395f7beb4dbf9b14ec8fd43b57f126c \
    --hash=sha256:16249ee61e95f858e83976573de0f5b2893b3677ba71c9dd36b9cf8be9ac6d65 \
    --hash=sha256:1d37d57ad971609cf3c53ba6a7e365e40660e3be0e5175fa9f2365a379d6095a \
    --hash=sha256:1ebe39cb5fc479422b83de611d14e2c0d3bb2a18bbcb01f229ab3cfbd8fee7a0 \
    --hash=sha256:214ed4befebe12df36bcc8bc2b64b396ca31be9304b8f59e25c11cf94a4c033b \
    --hash=sha256:2283a07e2c21a2aa78d9c4442724ec1eb15f5e42a723b99cb3d822d48f5f7ad1 \
    --hash=sha256:22ba7cfcad58ef3ecddc7ed1db3409af68d023b7f940da23c6c2a1890976eda6 \
    --hash=sha256:27c0abcb4a5dac13684a37f76e701e054692a9b2d3064b70f5e4eb54810553d7 \
    --hash=sha256:28c8d926f98f432f88adc23edf2e6d4921ac26fb084b028c733d01868d19007e \
    --hash=sha256:2e71d11abed7344e42a8849600193d15b6def118602c4c176f748e4583246007 \
    --hash=sha256:34d5fcd24b8445fadc33f9cf348c1047101756fd760b4dacb5c3e99755703310 \
    --hash=sha256:37503bfbfc9d2c40b344d06b2199cf0e96e97957ab1c1b546fd4f87e53e5d3e4 \
    --hash=sha256:3c5677e12444c15717b902a5798264fa7909e41153cdf9ef7ad571b704a63dd9 \
    --hash=sha256:3ff07ec89bae51176c0549bc4c63aa6202991da2d9a6129d7aef7f1407d3f295 \
    --hash=sha256:41715c910c881bc081f1e8872880d3c650acf13dfa8214bad49ed4cede7c34ea \
    --hash=sha256:418cf3f2111bc80e0933b2cd8cd04f286338bb88bdc7bc8e6dd775ebde60b5e0 \
    --hash=sha256:44edc647873928551a01e7a563d7452ccdebee747728c1080d881d68af7b997e \
    --hash=sha256:4a2e8cebe2ff6ab7d1050ecd59c25d4c8bd7e6f400f5f82b96557ac0abafd0ac \
    --hash=sha256:4ad1906908f2f5ae4e5a8ddfce73c320c2a1429ec52eafd27138b7f1cbe341c9 \
    --hash=sha256:501a031947e3a9025ed4405a168e6ef5ae3126c59f90ce0cd6f2bfc477be31b7 \
    --hash=sha256:5190d403f121660ce8d1d2c1bb2ef1bd05b5f68533fc5c2ea899bd15f4399b35 \
    --hash=sha256:5498cd1645aa724a7c71c8f378eb29ebe23da2fc0d7a08071d89469bf1d2defb \
    --hash=sha256:5cf4e27da7e3fbed4d6c3d8e797387aaad68102272f8f9752883bc32d61cb87b \
    --hash=sha256:5e0b74767e5f8c593e8c9b5912019159ed0533c70051e9cce3e8b6aa699fcd69 \
    --hash=sha256:5ed875a24292240029e4483f9d4a4b8a1ae08843b9c54f43fcc11e404532a8a5 \
    --hash=sha256:5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b \
    --hash=sha256:5fdec68f91a0c6739b380c83b951e2c72ac0197ace422360e6d5a959d8d97b2c \
    --hash=sha256:6344df0d5755a2c9a276d4473ae6b90647e216ab4757f8426893b5dd2ac3f369 \
    --hash=sha256:64386e5e707d03a7e172c0701abfb7e10f0fb753ee1d773128192742712a98fd \
    --hash=sha256:652cb6edd41e718550aad172851962662ff2681490a8a711af6a4d288dd96824 \
    --hash=sha256:66291b10affd76d76f54fad28e22e51719ef9ba22b29e1d7d03d6777a9174198 \
    --hash=sha256:66e1674c3ef6f541c35191caae2d429b967b99e02040f5ba928632d9a7f0f065 \
    --hash=sha256:6adc77889b628398debc7b65c073bcb99c4a0237b248cacaf3fe8a557563ef6c \
    --hash=sha256:79005a0d97d5ddabfeeea4cf676af11e647e41d81c9a7722a193022accdb6b7c \
    --hash=sha256:7c6610def4f163542a622a73fb39f534f8c101d690126992300bf3207eab9764 \
    --hash=sha256:7f047e29dcae44602496db43be01ad42fc6f1cc0d8cd6c83d342306c32270196 \
    --hash=sha256:8098f252adfa6c80ab48096053f512f2321f0b998f98150cea9bd23d83e1467b \
    --hash=sha256:850774a7879607d3a6f50d36d04f00ee69e7fc816450e5f7e58d7f17f1ae5c00 \
    --hash=sha256:8d1fab6bb153a416f9aeb4b8763bc0f22a5586065f86f7664fc23339fc1c1fac \
    --hash=sha256:8da9669d359f02c0b91ccc01cac4a67f16afec0dac22c2ad09f46bee0697eba8 \
    --hash=sha256:8dc52c23056b9ddd46818a57b78404882310fb473d63f17b07d5c40421e47f8e \
    --hash=sha256:9149cad251584d5fb4981be1ecde53a1ca46c891a79788c0df828d2f166bda28 \
    --hash=sha256:93dda82c9c22deb0a405ea4dc5f2d0cda384168e466364dec6255b293923b2f3 \
    --hash=sha256:96b533f0e99f6579b3d4d4995707cf36df9100d67e0c8303a0c55b27b5f99bc5 \
    --hash=sha256:9c57bb8c96f6d1808c030b1687b9b5fb476abaa47f0db9c0101f5e9f394e97f4 \
    --hash=sha256:9c7708761fccb9397fe64bbc0395abcae8c4bf7b0eac081e12b809bf47700d0b \
    --hash=sha256:9f3bfb4965eb874431221a3ff3fdcddc7e74e3b07799e0e84ca4a0f867d449bf \
    --hash=sha256:a33284e20b78bd4a18c8c2282d549d10bc8408a2a7ff57653c0cf0b9be0afce5 \
    --hash=sha256:a80cb027f6b349846a3bf6d73b5e95e782175e52f22108cfa17876aaeff93702 \
    --hash=sha256:b30236e45cf30d2b8e7b3e85881719e98507abed1011bf463a8fa23e9c3e98a8 \
    --hash=sha256:b3bc83488de33889877a0f2543ade9f70c67d66d9ebb4ac959502e12de895788 \
    --hash=sha256:b865addae83924361678b652338317d1bd7e79b1f4596f96b96c77a5a34b34da \
    --hash=sha256:b8bb0864c5a28024fac8a632c443c87c5aa6f215c0b126c449ae1a150412f31d \
    --hash=sha256:ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc \
    --hash=sha256:bdb2c67c6c1390b63c6ff89f210c8fd09d9a1217a465701eac7316313c915e4c \
    --hash=sha256:c1ff362665ae507275af2853520967820d9124984e0f7466736aea23d8611fba \
    --hash=sha256:c2514fceb77bc5e7a2f7adfaa1feb2fb311607c9cb518dbc378688ec73d8292f \
    --hash=sha256:c3355370a2c156cffb25e876646f149d5d68f5e0a3ce86a5084dd0b64a994917 \
    --hash=sha256:c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5 \
    --hash=sha256:d0eae10f8159e8fdad514efdc92d74fd8d682c933a6dd088030f3834bc8e6b26 \
    --hash=sha256:d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f \
    --hash=sha256:ebc55a14a21cb14062aa4162f906cd962b28e2e9ea38f9b4391244cd8de4ae0b \
    --hash=sha256:eda16858a3cab07b80edaf74336ece1f986ba330fdb8ee0d6c0d68fe82bc96be \
    --hash=sha256:ee2922902c45ae8ccada2c5b501ab86c36525b883eff4255313a253a3160861c \
    --hash=sha256:efd7b85f94a6f21e4932043973a7ba2613b059c4a000551892ac9f1d11f5baf3 \
    --hash=sha256:f7057c9a337546edc7973c0d3ba84ddcdf0daa14533c2065749c9075001090e6 \
    --hash=sha256:fa160448684b4e94d80416c0fa4aac48967a969efe22931448d853ada8baf926 \
    --hash=sha256:fc09d0aa354569bc501d4e787133afc08552722d3ab34836a80547331bb5d4a0
```

## 25. llm-gateway-e2e/requirements.lock

SHA-256: `b568b242bba5c1d3fc407fb47e0a5fa1ca1f91dd9274a00692e37d3f388f690a`

```text
# Locked to the existing tested Python 3.12 environment; generated 2026-10-17.
# Source: requirements.txt
# Install with: python3 -m pip install --require-hashes -r <this-file>

certifi==2026.7.22 \
    --hash=sha256:62f22742b58a1a33014a2b6b706588a8d7e2a88ae7bd1a6ebe8c992928483775 \
    --hash=sha256:741e2c3b351ddf169a738da9f2c048608ff7f2c5cc02f1ebc6b118bb090d5d55

charset-normalizer==3.5.2 \
    --hash=sha256:01077390b03f7988f11d700a2194e69b119741a86b1a638b1db88891e3eced8e \
    --hash=sha256:01b0c0d2262a9e28e8484a278c7e1b5d650e3ac8cf2683d2967e25899f208bdf \
    --hash=sha256:04851f73ae72b8413dddadb16a49dfee95263553741fd42d546f7d66907e6be5 \
    --hash=sha256:0521c5665880b33d603717defa76c094048900010897909952397feb3039da56 \
    --hash=sha256:0774bf9bf620249fee3e0b8b9fd3065de213be30f3aa94ce2494b3b638949e26 \
    --hash=sha256:0891b9d3903c5571c03771ca669a4b0ec5618ca722a5c957d3d29cd4e5062848 \
    --hash=sha256:0c951d5e6dd9c2ff60609476752bee49da4206adde960ebc247766937f72e718 \
    --hash=sha256:0fed1d06615f022ee3b13caf5e8b180cfea32bb2c5aded8a9d44277afc040f93 \
    --hash=sha256:114e4d0c92d618409ed82a99e22b5c5e768fe995f2973f78265f4524f49d4640 \
    --hash=sha256:11912e4bb14baae7c5d8791aa55ba0a3a03ec6729073307b0f57270abaa713d3 \
    --hash=sha256:11a4d68a6ecda3292cb1e50239e111543ba5d709bb62a6b4ea1afcfa729d8875 \
    --hash=sha256:124fbf1a8ff966d87ae05bb8bd45a71f966055ed8bba320d0c7cf450bc5f4d0e \
    --hash=sha256:1461ac396c4fdb983a675f20aa555624f0ee18ac83d832b9244ffff3d8055275 \
    --hash=sha256:1503bccbeb36d5527790c3930327704c39af22de3112f1b1666a9f3ce15ee204 \
    --hash=sha256:15bb4005af6320d259dc7593ca84a38d7fe06a421dbcf7b910ae23979101e787 \
    --hash=sha256:15c44f7edfd477b06f517a5cc317fc1707edb9de2c865f43d4b6513907473234 \
    --hash=sha256:16fa0eccf81304b79c5cd87f9271c3b85dd9dd99245e4422ae9c0dd45e0f99d3 \
    --hash=sha256:183b88127acdb4fabe59d951ab424faf1af7b63cdbb5f776186c1ea2ffcaed98 \
    --hash=sha256:195c26fb65950f8fce54e26349852b7bdd7c5f120aeefbcc440b8a20faaed4a3 \
    --hash=sha256:1afb975bd5d68d5ce9f6b6d44fdf2f7e34b895a35e95708a7a91b20a3b51d187 \
    --hash=sha256:1b4cbc7c3491ccb4aa17fcd8165649d01cf39f76de1696da8631b5f71b85401d \
    --hash=sha256:1bc0baf5ef96b6ede57d47f4b8fe4d9d84019c3bfcbeb20a41edc6a6ee341f1f \
    --hash=sha256:1c50fe28bbc2ced33386f298650d91218076c05420e6cbd790b913adc41659e7 \
    --hash=sha256:1db38f4c5496827c1a501846d64d14c3b80c7e6714e406cd7dc36a9899fa1011 \
    --hash=sha256:211d5a3eb6af8f513b8d4ca19a8c1b7accab1b5f0d3175f9826b03c1a920dc1f \
    --hash=sha256:23851fb4e1b85ed3f6c2a27b777cdfe2e19fb5b38429a8faf38c7542b7665869 \
    --hash=sha256:254eb48b9fa5ee9898a3c445825a1f340fe53712a098904b39b0bddba8ea3cb1 \
    --hash=sha256:2625388c6c754520c37abaf3b41eb34d1cc4a373f457898f08606c8e362b891d \
    --hash=sha256:281cb91036248400f4cc957495cccd44c275c2e0c5854f7e45ac5cf7dc193847 \
    --hash=sha256:28a15fdad492a99b6eccfaaed66ef3f74050680545ea61ec8b2f4c538f1f1320 \
    --hash=sha256:28b4f0d66fb834ff90f28209ac7bce77868c45d8c93e26f906709d9b7c2e1af9 \
    --hash=sha256:2a925889534b3748302dae5dead07cc13480de1dac3aea80a941b729b471ef93 \
    --hash=sha256:2b7b3bbfb4fe8ef40600792d762fbaa9057559f9d3fad209525b7a22b99e91fd \
    --hash=sha256:2c9ad19a6cfcd5ea5c0d41161d22f9df1dcc277e9bef2751391334546a314c00 \
    --hash=sha256:2cc961b171b3f3440f410489ab3573e86aea8736134ebbb40ea1338b7f0831bc \
    --hash=sha256:2ce45c6627b22c47e390bc91a41c3d13032192e699fa0bea96e9671b373d69b0 \
    --hash=sha256:2e06a3a98f916dd41d27f3105e02e7a40181c98c94b9158733d03a6f80506c09 \
    --hash=sha256:304d5463e65a35d7bb0850550e0780395395f6fcf452f04db7d5ca7cecc425ac \
    --hash=sha256:304d8e4d493af723536393eee0c689eb7813f4a474c8b479dee63f1fdd98f621 \
    --hash=sha256:30fcd120b732aa79317f08dee04d7de0847822e4cf7ee0e9f445bb958832252c \
    --hash=sha256:31f3930700408d211f13378ccbe1c40845d8da54bd0681fac3a9b5aae81c7aa8 \
    --hash=sha256:34276fd796040bf0993ab33a369aa572e6979c7aab225a88893667ad8eac8f7a \
    --hash=sha256:355ad8011081dec5412240c087a9a0c9d4d5039f3ed11a3f13e18c2b29b56c51 \
    --hash=sha256:38a873987f3be698494da8b2e3085e29da02da7b633dce73e79c699a113d7bf0 \
    --hash=sha256:39de2a259fc954455c57274dc94c79d5842774e1247a016aff30bc0efed0f4ef \
    --hash=sha256:3d14b50de6bf4d0edf857a9386836846f982b8f524e188e2e68b96d702bcf4aa \
    --hash=sha256:3d21b8b13c7592db2ac5e544a6d83187b995257472b0c9e8351b6d507ae37ed6 \
    --hash=sha256:3d31298449090ab8d47b7b1b2a555ff73cac7ed438a08b7ac160980c7ebed649 \
    --hash=sha256:3ddacd27458c45bdacd6bd6db644bfb730efbf9e830310186e3045c9c5be8fb2 \
    --hash=sha256:3df041de8887954562c9b261cba85ca0e9ded74048daf125f45edcfaa4832229 \
    --hash=sha256:40ab6bffa02ae10a0581e6c198be7d2d8ca5c2a0c64e4ed3465d766df457573e \
    --hash=sha256:4275811936e2f06feff5e598fb42a1b7ae852da8e39605211892b56b81a34efd \
    --hash=sha256:443eae2bf318abeaf6f15d785138f71fd6de770e99a92158b8b814265e079115 \
    --hash=sha256:447441e76ec720b15e64418d32e092297340387053047c7c694f579efb0ee1d9 \
    --hash=sha256:4495c5002a7b28557e7e222e77e0b661183e432b7d6d2e788101e3f240e05b8c \
    --hash=sha256:44bd4fbb29dfbeba60e7d2bd000c59e4b21ddb3cc53912b14048d37092706d7c \
    --hash=sha256:4685902cf26edf013ed7a3da0f426ebba7a00ebb9541386d835afbf002c11cab \
    --hash=sha256:498dc3188ca05a68231ac3fdbfc7f57eb67e1343c30e0fea17f8218c1599b253 \
    --hash=sha256:4c2b5031f63e331e3839b40aed2dd6f191e9c07edbde303e7876846ea1946995 \
    --hash=sha256:4d48f2d08b9de5864e2c8744d4461b862fb149a18274abc8b698c45975573438 \
    --hash=sha256:4f87960d57feabfb618e4e0af6e7371645fa26a277860739d6e5d6e0012c92f0 \
    --hash=sha256:50e3adfb96fc189eb27b1cf62d3b598b89b4bb0420d93a3d3e42e137409011be \
    --hash=sha256:51cf45226a9b588d0d2b4880c62d686934b63ab0bd79ca23ab0e9762eb27441b \
    --hash=sha256:52aa6992700996af31f375de0c6bacd402b0097fe40b53c426b9f51a90ebabc7 \
    --hash=sha256:55ea99acb17b9325618de155a0cd6a2e8f5d10be008113e1d433bbb58db543b2 \
    --hash=sha256:56bc200a365efb37383b7852e4cc5898d3b2da5987289b543956cf8cad71018a \
    --hash=sha256:588461c2e8384d309bd63e5826019b6977bc66d629b99ac8737bb795d7b2cb5a \
    --hash=sha256:58ca3755ee7ff7f59b57789ec9833c9de9ea275405cdd240eda1f193112e398a \
    --hash=sha256:58f361dcbab699cf8f42db3f47c8e7fd1036f138c23a5d08de9fde5f425a730c \
    --hash=sha256:598a11a2c7ebaa5334bf698bf29568c9c390abac6a154d8170fedecd1cea38c5 \
    --hash=sha256:59f63901b0031c3136cf64704dcb21de0bbae62ce2c9529bc39d27665463de37 \
    --hash=sha256:5cde776b7cc66e4f6c99612cea4aa7269aa65863f7a15841b2c264f103822f4e \
    --hash=sha256:5e2b6b57e9733d39f0c9fd3185efa6b8e29652c4cd8fe94180272cf6ed9a78c4 \
    --hash=sha256:5fb29fb8cd1a46c27a1bf9613ad5ec2599310d46b4025d9556404a6b6a292800 \
    --hash=sha256:6045373d5a89a5ec71afde535db987ca28e76dfa276c2d4c818265b375d4b055 \
    --hash=sha256:619799369eeef6366ed3e8755a5670f4f2f0fb6b30a0fd7264dc0fdc2357058e \
    --hash=sha256:62588a277bfb59def052abd940703fa35107152bf479781a878617d60faf8fb5 \
    --hash=sha256:62603db9a7caa0802eaa28c1c46fecd7b3a263a774069c24c3c28c302448721c \
    --hash=sha256:65cd72beeeca9d3aaea1201e5923859f308f952f9c71de93f06063c79f0f7a3b \
    --hash=sha256:68eb192d85ab8e5f6ec69c2bc6ac0179fbf04a5ac1569d12fbef74883fe102d0 \
    --hash=sha256:6bd128f206a7752ae1f2ab6c61bf8a24ba28913a10df8b14c2637b973ff97a80 \
    --hash=sha256:6be488a102b8cf28d0391d8c4ba7748938ae28b78ad901f8585520fca33ead1a \
    --hash=sha256:7218e8f32b0956cfcd048fd42d9d5779809745ca1d86113ca56f66e7ae1549c4 \
    --hash=sha256:7441d755b7ab94f8d4eb3e43ec05482d760842fd263d003a99102d742cd835e2 \
    --hash=sha256:749e97e1b32313717a565abbe321bc2190bc8b35f1a67e4cdbc7c56c8d8ffe58 \
    --hash=sha256:75a3ceed0724d625d64b86ca20aba182e4df462e04c2414fc941c0f523f06aac \
    --hash=sha256:780fbe7cab297b81dad9fb8dc5eb003c0468ffb0d9e5f65068c53a34661a96bc \
    --hash=sha256:78456a747de8dc58360ffa581f30a002baf5aa28cb262536545e91f113ed7639 \
    --hash=sha256:7967d08cf06dee78443b874f98c98036f624f3a4e73e11f9f64f5be4d25393cf \
    --hash=sha256:7a881931aa470808df94a8c380eed2bbbc76cd9dc622310f99665658c821eb6d \
    --hash=sha256:7dcd882da75ef9adf94903b1e3b9419e8aa8fb4c7396822b834b9ef7fb96954f \
    --hash=sha256:7e841fb9010836c992c9f12fcbd43a831de93a5f726fc1ccd8ca1d0268c5014c \
    --hash=sha256:7fdde2c9fd9e3eca40631e024664cf2584272cc8f96308cbe5fdfc930f51d8bc \
    --hash=sha256:8024d00c3faf3fc0c16e07a69f4405e8eac7cc0ab15f65fe6cf43827c4cf72b4 \
    --hash=sha256:80d02b6f04e92601a081dd97b23d3128033098bff5d35d392ddcc0476ea11253 \
    --hash=sha256:838dcc90063569a0448120554591a1d6c4a4ffe11babf048908793154ab86ade \
    --hash=sha256:849df64e889b2e17230d58410a03dba311a65b163508fd33679b2b737d4b7858 \
    --hash=sha256:87475fabc8d9996fd9c27debb395e642e8c838d78a00b6e932227a0e06b81e26 \
    --hash=sha256:87e50a3e7cb90af586b6c5faf23e302a970415ac73bd7bd90a515a04b427ef96 \
    --hash=sha256:89b53f3cda69831909888e0494f4fa0bcd3537e3e138dabeb620bd6ad946bae8 \
    --hash=sha256:8a893cc101149f80a653f82062ebc95b34525a2614382e1da5458fe7c6997249 \
    --hash=sha256:8b2bfab86aa71ae13aa41a6a26aab338e0db2b8bc75434b05aea89e011ff35a4 \
    --hash=sha256:8d86d6fc60743dc916eb79e2eb1ec4818e21e427731543af40a3021851174a13 \
    --hash=sha256:915563965d418f986e7e145accc592eae9e1a1be3566ff98a05d7a9ec42a76e1 \
    --hash=sha256:92888bb3187c5ba50500b00b3b310c9f2c651709d28036077680cb5255450a03 \
    --hash=sha256:93223adc95033dd47133a46ccfc316a0139176fd79085762e27202ec56018f03 \
    --hash=sha256:9373ad13ef0d2c0fb761e04e55bfdee5a08b52cef2c882c8fbe9935b1517152e \
    --hash=sha256:9409a8bf35cf78353942504b24a57de3d75b708997a1e4bd8db71ac8633ce364 \
    --hash=sha256:9b7f416ff0978e2f2249330527f0ad6fa02f4932e6199692d3b52da2048c19e4 \
    --hash=sha256:9bde855991b7e362c146535e3136a50bfaffc0487d38b33ca7e5edefc6e23849 \
    --hash=sha256:9cae88599c7219005d879f98e5ed53341e9a122af585e1091200358a3003d2a0 \
    --hash=sha256:9cf9b1a857e25c4baceeb3624e92a56df3668f398c4acba74e174d81fb4d1d3a \
    --hash=sha256:9f56f72050826f63dcee7a7f55b0a77168cb3bfc553fd405e7f8f9ece75a4036 \
    --hash=sha256:a090bb2c68df85450502e3e20d665e3a5af9c65a84d6508ed477badd49166fd3 \
    --hash=sha256:a192e2c40070d92c3ccf777e3a5c4ff515573cd2bb7ed0c537fdadbbec5bbf21 \
    --hash=sha256:a19a731138fc27d5682277d3b9df22855cea1239bce7fcec5f78f42ef2d1f3c3 \
    --hash=sha256:a66c3bc5ab1f0ff2164fc9965ddd611ff0802173f4b9d24554c563f6ab7e1d6e \
    --hash=sha256:a815775b6c38d4e0ff7bcffbeba67feded90202bb6a226b8dd35f1c855217413 \
    --hash=sha256:a89012d6d5476ee112d20d998570ed58df2260a852afb1758809cd6900411d21 \
    --hash=sha256:ae4f5fea5b8b8ccff88238cc8569303e5ee95efae67fa62922a311397a71f346 \
    --hash=sha256:b6856554c4f44d79fc2307d5768854310a8f0096e501c75637542c82292b0429 \
    --hash=sha256:b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685 \
    --hash=sha256:b736353c0a625bbd5fcec108576e2385db3496f4f771f785ff32e108d3c3bc45 \
    --hash=sha256:b7fd005a73d9e657273b7a10dc71a9e03c8fb9ee6999798d6918ce095b81ac7f \
    --hash=sha256:b91363207bd9dc966a691e959bb47f64b30f7ac4b072be9968b366982f7db77c \
    --hash=sha256:ba0b1d2620edf869789c3879223f52bf2afc5d31b3cb47cc57b3a12c05e2aa9d \
    --hash=sha256:bbbfc8e28816f19d7c0f1816664980c0a9875d01b27cdf8eedddb639d9e108ad \
    --hash=sha256:bd16aabe4a02a297c23417aa17ac6299dbd8c49f673bcd645b4929b11f5a4400 \
    --hash=sha256:c0afc6800ba57ccc350374c5bd6150419915d95ce93cdbab2d783d75eaf30ecb \
    --hash=sha256:c6708715abcf3c73b99508253e961a9967f02fe536532834149574eda6de0d1c \
    --hash=sha256:c7c9ab723cde841fefb34efbad91e87f00a674b1fe1cd0784fde742bf2c154dc \
    --hash=sha256:c8f3d67aeaf55f017982b73683f0e7342ba2f6635a78f69ce89ebb26aa411e5c \
    --hash=sha256:c9790464842f85f437dbbb54417eda1e0e6bfc52dd8d22d6fd1c994b73b2dc74 \
    --hash=sha256:ca403d7e4798f525fdfc78e258820419cbbd0f0ecbab9de7840e3c017cf6b8cf \
    --hash=sha256:d008d90a7f2471519aef0c90dfbe73b3e6e4d5e66ac48e19154c17e89e98b604 \
    --hash=sha256:d19fbd981a488e22cd04883659ca6b08f50b5974f9fd7c95655ef6a043e5893f \
    --hash=sha256:d1befeed746d247c81127bb14de9dc3d30edb6e5976d34f83f86ed262b1d9105 \
    --hash=sha256:d2374b62878abb00cd8309b32af6c0b715cd02dec0ca74ef12e5069bdc64144a \
    --hash=sha256:d376bbd28b3a8999db1a103b3b388aee6f1ddeb3e51bc2172993efdcd86e064d \
    --hash=sha256:d4a7319f304a774bed22115bc891618e45f85065ab44ea6acd07d274e750519a \
    --hash=sha256:d6734d2ef8a50fbf8445c139477da401f50d62a0606bf00e20ec6d87773fefb1 \
    --hash=sha256:d760fe2a4d7c3b226cb9026d6a842868d52a7901bd98420e1baf14e80da85cf5 \
    --hash=sha256:d913de495d90407cd859d263bee2e5d1a4ed3eb6573c04e70d9ec619a7cbed7f \
    --hash=sha256:db19d07e2e0129e974a0e65d0064fc222a446cd5122c2fd4184d2af9fc734a9e \
    --hash=sha256:dca9ab98072a5a54ebacebdc45f53e645336b320c667410b061be1ca588ae709 \
    --hash=sha256:ddc7dacc8ece3a182e7f15cb862d1fd616b46d076cb1ae9dd232b2c38b655874 \
    --hash=sha256:ddf19c062bea7a0cc80f519243d2c01dd091be0cf952a0750d4ad576709559f5 \
    --hash=sha256:def79fa35ef0cef8d2accec024f4fdc7ead3012ff02f5215c783f39f03ef8cfc \
    --hash=sha256:df29a0a7107f7011e77f4eebdddec4c7331e24d787a0b21a46d63bdf7445da95 \
    --hash=sha256:e09a3942ecbdee5cce73ea9d42da82b81b72ac1bf031ce069b93b5adf4eac8cd \
    --hash=sha256:e242bb1c5e76e97dfa9e7f209a71e93a01d7f19ffdd5cfbb2e2d55b4f08f8ab0 \
    --hash=sha256:e243bd13217235fc7290c621941c3f5cc8b66e4872495be821d7436ba2fb838d \
    --hash=sha256:e2af3aad578aa6bd1384bcf4750fc285e5a9de53f40b7d41e5a0bf748edeb2b3 \
    --hash=sha256:e4e81e09c1578b8df602e3db08b0b3ea0a6947ad612f52bf8dc5ea8d47691f0c \
    --hash=sha256:e54da4baf05720032d527874d40b65fa4d7e5c6c6a43d0c3adbeffcaf275a2b3 \
    --hash=sha256:e80e6c2f55656b4824d72065abb4ddd6a525c74bd78a0aab5d9fc2cf4fb5af50 \
    --hash=sha256:ed2a239c0ea213acc1908150a3037257083c7c083128f1a4cec2ec4b97dca491 \
    --hash=sha256:ed905975ab14056a2e5eb1c376cb2e1ebc5396baf84163939c518556fccde9f5 \
    --hash=sha256:ee21e28f0430bd6dc9086c6e525d5e818a44a5ad19720c8a0ef766792f3eb5e5 \
    --hash=sha256:ee43c17b173d46a3212baa6ead3ae258eeabdae48c263a01ccf0218c366dd655 \
    --hash=sha256:ef4fcbf3327382cd4c9f540babd61248208af7b93eec4de397b4d5f58a09e288 \
    --hash=sha256:eff0ac9dbe711a4aee69bf04a83896aa9b85f19641264053a9f6d48573abb7dd \
    --hash=sha256:f0aa869112ef88429ae17820d99c3dd9504c9e9c671d3c246f3d7442cb051084 \
    --hash=sha256:f3c96f633825733f735c5a9cf21d21a257d8e1edf0b1cee0a064b9c424ca0f7d \
    --hash=sha256:f5833ad231be5eb6553de524a70f48d71b2c8563101750531e0b80184e175cd4 \
    --hash=sha256:f5ec61164adcec446f8969a3358ec3f9b26bbda3b9213e5586d219afa8df2915 \
    --hash=sha256:f7d486c83842422badd511868fd8a9a20e9407ace71564b6af47ce7e60a336c1 \
    --hash=sha256:fb9e68df06293761f9fe66ade60a9bc6d0f5e42b8acf2939a9158af86ab0e5bd \
    --hash=sha256:fc14a032f813bf5fe624d991960ea83e9715adc27e4c1830a2361eb1d02ac341 \
    --hash=sha256:fcff63213e8e6e47770541a4607175404f47cbb3ebea7b6058cc82d524a0e424 \
    --hash=sha256:fd1fbe0f116b6e55da77aca2c6ddcddcfac2186cbf78bdebf40fc156efca389d \
    --hash=sha256:fe9753dfee015c570d73df76f899f18444d41388bffcde097deba51c4fadbb9f

idna==3.20 \
    --hash=sha256:a7db850025b95ded1eae8a46181a1a6c56c92c96f0e2b005d9ff8dc0210cab44 \
    --hash=sha256:ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c

iniconfig==2.3.0 \
    --hash=sha256:c76315c77db068650d49c5b56314774a7804df16fee4402c1f19d6d15d8c4730 \
    --hash=sha256:f631c04d2c48c52b84d0d0549c99ff3859c98df65b3101406327ecc7d53fbf12

packaging==26.3 \
    --hash=sha256:94edc256424af38762eb31306eed28beb9f0efc50a8837492c9d6fd6004aed79 \
    --hash=sha256:d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c

pluggy==1.6.0 \
    --hash=sha256:7dcc130b76258d33b90f61b658791dede3486c3e6bfb003ee5c9bfb396dd22f3 \
    --hash=sha256:e920276dd6813095e9377c0bc5566d94c932c33b27a3e3945d8389c374dd4746

Pygments==2.21.0 \
    --hash=sha256:2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9 \
    --hash=sha256:610ca751c9bc2492b38eb9a38a7fbc93edbbb2d7182edaf34e66ae493dee5c8c

pytest==9.0.3 \
    --hash=sha256:2c5efc453d45394fdd706ade797c0a81091eccd1d6e4bccfcd476e2b8e0ab5d9 \
    --hash=sha256:b86ada508af81d19edeb213c681b1d48246c1a91d304c6c81a427674c17eb91c

PyYAML==6.0.3 \
    --hash=sha256:00c4bdeba853cc34e7dd471f16b4114f4162dc03e6b7afcc2128711f0eca823c \
    --hash=sha256:0150219816b6a1fa26fb4699fb7daa9caf09eb1999f3b70fb6e786805e80375a \
    --hash=sha256:02893d100e99e03eda1c8fd5c441d8c60103fd175728e23e431db1b589cf5ab3 \
    --hash=sha256:02ea2dfa234451bbb8772601d7b8e426c2bfa197136796224e50e35a78777956 \
    --hash=sha256:0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6 \
    --hash=sha256:10892704fc220243f5305762e276552a0395f7beb4dbf9b14ec8fd43b57f126c \
    --hash=sha256:16249ee61e95f858e83976573de0f5b2893b3677ba71c9dd36b9cf8be9ac6d65 \
    --hash=sha256:1d37d57ad971609cf3c53ba6a7e365e40660e3be0e5175fa9f2365a379d6095a \
    --hash=sha256:1ebe39cb5fc479422b83de611d14e2c0d3bb2a18bbcb01f229ab3cfbd8fee7a0 \
    --hash=sha256:214ed4befebe12df36bcc8bc2b64b396ca31be9304b8f59e25c11cf94a4c033b \
    --hash=sha256:2283a07e2c21a2aa78d9c4442724ec1eb15f5e42a723b99cb3d822d48f5f7ad1 \
    --hash=sha256:22ba7cfcad58ef3ecddc7ed1db3409af68d023b7f940da23c6c2a1890976eda6 \
    --hash=sha256:27c0abcb4a5dac13684a37f76e701e054692a9b2d3064b70f5e4eb54810553d7 \
    --hash=sha256:28c8d926f98f432f88adc23edf2e6d4921ac26fb084b028c733d01868d19007e \
    --hash=sha256:2e71d11abed7344e42a8849600193d15b6def118602c4c176f748e4583246007 \
    --hash=sha256:34d5fcd24b8445fadc33f9cf348c1047101756fd760b4dacb5c3e99755703310 \
    --hash=sha256:37503bfbfc9d2c40b344d06b2199cf0e96e97957ab1c1b546fd4f87e53e5d3e4 \
    --hash=sha256:3c5677e12444c15717b902a5798264fa7909e41153cdf9ef7ad571b704a63dd9 \
    --hash=sha256:3ff07ec89bae51176c0549bc4c63aa6202991da2d9a6129d7aef7f1407d3f295 \
    --hash=sha256:41715c910c881bc081f1e8872880d3c650acf13dfa8214bad49ed4cede7c34ea \
    --hash=sha256:418cf3f2111bc80e0933b2cd8cd04f286338bb88bdc7bc8e6dd775ebde60b5e0 \
    --hash=sha256:44edc647873928551a01e7a563d7452ccdebee747728c1080d881d68af7b997e \
    --hash=sha256:4a2e8cebe2ff6ab7d1050ecd59c25d4c8bd7e6f400f5f82b96557ac0abafd0ac \
    --hash=sha256:4ad1906908f2f5ae4e5a8ddfce73c320c2a1429ec52eafd27138b7f1cbe341c9 \
    --hash=sha256:501a031947e3a9025ed4405a168e6ef5ae3126c59f90ce0cd6f2bfc477be31b7 \
    --hash=sha256:5190d403f121660ce8d1d2c1bb2ef1bd05b5f68533fc5c2ea899bd15f4399b35 \
    --hash=sha256:5498cd1645aa724a7c71c8f378eb29ebe23da2fc0d7a08071d89469bf1d2defb \
    --hash=sha256:5cf4e27da7e3fbed4d6c3d8e797387aaad68102272f8f9752883bc32d61cb87b \
    --hash=sha256:5e0b74767e5f8c593e8c9b5912019159ed0533c70051e9cce3e8b6aa699fcd69 \
    --hash=sha256:5ed875a24292240029e4483f9d4a4b8a1ae08843b9c54f43fcc11e404532a8a5 \
    --hash=sha256:5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b \
    --hash=sha256:5fdec68f91a0c6739b380c83b951e2c72ac0197ace422360e6d5a959d8d97b2c \
    --hash=sha256:6344df0d5755a2c9a276d4473ae6b90647e216ab4757f8426893b5dd2ac3f369 \
    --hash=sha256:64386e5e707d03a7e172c0701abfb7e10f0fb753ee1d773128192742712a98fd \
    --hash=sha256:652cb6edd41e718550aad172851962662ff2681490a8a711af6a4d288dd96824 \
    --hash=sha256:66291b10affd76d76f54fad28e22e51719ef9ba22b29e1d7d03d6777a9174198 \
    --hash=sha256:66e1674c3ef6f541c35191caae2d429b967b99e02040f5ba928632d9a7f0f065 \
    --hash=sha256:6adc77889b628398debc7b65c073bcb99c4a0237b248cacaf3fe8a557563ef6c \
    --hash=sha256:79005a0d97d5ddabfeeea4cf676af11e647e41d81c9a7722a193022accdb6b7c \
    --hash=sha256:7c6610def4f163542a622a73fb39f534f8c101d690126992300bf3207eab9764 \
    --hash=sha256:7f047e29dcae44602496db43be01ad42fc6f1cc0d8cd6c83d342306c32270196 \
    --hash=sha256:8098f252adfa6c80ab48096053f512f2321f0b998f98150cea9bd23d83e1467b \
    --hash=sha256:850774a7879607d3a6f50d36d04f00ee69e7fc816450e5f7e58d7f17f1ae5c00 \
    --hash=sha256:8d1fab6bb153a416f9aeb4b8763bc0f22a5586065f86f7664fc23339fc1c1fac \
    --hash=sha256:8da9669d359f02c0b91ccc01cac4a67f16afec0dac22c2ad09f46bee0697eba8 \
    --hash=sha256:8dc52c23056b9ddd46818a57b78404882310fb473d63f17b07d5c40421e47f8e \
    --hash=sha256:9149cad251584d5fb4981be1ecde53a1ca46c891a79788c0df828d2f166bda28 \
    --hash=sha256:93dda82c9c22deb0a405ea4dc5f2d0cda384168e466364dec6255b293923b2f3 \
    --hash=sha256:96b533f0e99f6579b3d4d4995707cf36df9100d67e0c8303a0c55b27b5f99bc5 \
    --hash=sha256:9c57bb8c96f6d1808c030b1687b9b5fb476abaa47f0db9c0101f5e9f394e97f4 \
    --hash=sha256:9c7708761fccb9397fe64bbc0395abcae8c4bf7b0eac081e12b809bf47700d0b \
    --hash=sha256:9f3bfb4965eb874431221a3ff3fdcddc7e74e3b07799e0e84ca4a0f867d449bf \
    --hash=sha256:a33284e20b78bd4a18c8c2282d549d10bc8408a2a7ff57653c0cf0b9be0afce5 \
    --hash=sha256:a80cb027f6b349846a3bf6d73b5e95e782175e52f22108cfa17876aaeff93702 \
    --hash=sha256:b30236e45cf30d2b8e7b3e85881719e98507abed1011bf463a8fa23e9c3e98a8 \
    --hash=sha256:b3bc83488de33889877a0f2543ade9f70c67d66d9ebb4ac959502e12de895788 \
    --hash=sha256:b865addae83924361678b652338317d1bd7e79b1f4596f96b96c77a5a34b34da \
    --hash=sha256:b8bb0864c5a28024fac8a632c443c87c5aa6f215c0b126c449ae1a150412f31d \
    --hash=sha256:ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc \
    --hash=sha256:bdb2c67c6c1390b63c6ff89f210c8fd09d9a1217a465701eac7316313c915e4c \
    --hash=sha256:c1ff362665ae507275af2853520967820d9124984e0f7466736aea23d8611fba \
    --hash=sha256:c2514fceb77bc5e7a2f7adfaa1feb2fb311607c9cb518dbc378688ec73d8292f \
    --hash=sha256:c3355370a2c156cffb25e876646f149d5d68f5e0a3ce86a5084dd0b64a994917 \
    --hash=sha256:c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5 \
    --hash=sha256:d0eae10f8159e8fdad514efdc92d74fd8d682c933a6dd088030f3834bc8e6b26 \
    --hash=sha256:d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f \
    --hash=sha256:ebc55a14a21cb14062aa4162f906cd962b28e2e9ea38f9b4391244cd8de4ae0b \
    --hash=sha256:eda16858a3cab07b80edaf74336ece1f986ba330fdb8ee0d6c0d68fe82bc96be \
    --hash=sha256:ee2922902c45ae8ccada2c5b501ab86c36525b883eff4255313a253a3160861c \
    --hash=sha256:efd7b85f94a6f21e4932043973a7ba2613b059c4a000551892ac9f1d11f5baf3 \
    --hash=sha256:f7057c9a337546edc7973c0d3ba84ddcdf0daa14533c2065749c9075001090e6 \
    --hash=sha256:fa160448684b4e94d80416c0fa4aac48967a969efe22931448d853ada8baf926 \
    --hash=sha256:fc09d0aa354569bc501d4e787133afc08552722d3ab34836a80547331bb5d4a0

requests==2.34.2 \
    --hash=sha256:2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0 \
    --hash=sha256:f288924cae4e29463698d6d60bc6a4da69c89185ad1e0bcc4104f584e960b9ed

urllib3==2.8.0 \
    --hash=sha256:0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3 \
    --hash=sha256:63bf2ead4c879426ebf22ef2a781eeb4aa3b4ae798a0435506f8687fd5bb9b63
```

## 26. llm-gateway-docs/.gitleaks.toml

SHA-256: `69af8bd59bb687e5ddc5d15941026286ebea05944a53b17dc260e46a5b215912`

```toml
title = "LLM Gateway documentation secret scanning"

[extend]
useDefault = true

# Exact values below are two blocked native token identifiers and five verified
# source-file checksums. None is an API credential; no path or rule is excluded.
# Evidence: reports/phase1-final-evidence/docs-secret-findings-verification.json
[allowlist]
description = "Exact verified audit identifiers and source-file checksums"
regexTarget = "secret"
regexes = [
  '''^032cceed19a1b385dd7d4fea7e965c98a59f70da3e82bbc818674d9b52ede7c2$''',
  '''^648efb4502c4f258073b52e01fab950bdabdc184110349731d755164d17ae96b$''',
  '''^b9ab0f23d15f33aeb87a5c2548012279a94521854f57eb54894ef98ef281f000$''',
  '''^d8981aafad6fa0409814a2ac06ba2da679ad9abb5a54f9f11d8431d6a7a140ce$''',
  '''^dccad2518497c3c49ea7ab8bc52b452080d780d26306d8d397ad0a872eb8c867$''',
  '''^055d975c489424025eb355a477f6183434ac1b4eafa37f4f1d530b33caf36849$''',
  '''^d4266b9a40dd5c715d3290a76a08c20db8a9b093c215d6e0cdb3e8748f17dd67$''',
]

# Verified source-manifest checksums, not API credentials.
# Evidence: reports/phase1-final-evidence/docs-source-hash-findings-verification.json
```

## 27. llm-gateway-docs/reports/phase1-final-evidence/config-drill.py

SHA-256: `92fc9809e9f382bd06c2693ba3fb531fb8346d27af28869b4d368da176765b8c`

```python
"""Reproduce the authorized config-only drill on the existing local gateway."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone


WORKSPACE = Path(__file__).resolve().parents[3]
INFRA = WORKSPACE / "llm-gateway-infra"
CONFIG = WORKSPACE / "llm-gateway-config/config/litellm_config.yaml"
RELEASE = INFRA / "scripts/release/release.sh"
NAMES = ["llm-gateway", "llm-gateway-postgres", "llm-gateway-redis"]


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, cwd=INFRA, **kwargs)


def identities():
    items = json.loads(run("docker", "inspect", *NAMES, capture_output=True).stdout)
    assert all(item["State"]["Running"] for item in items)
    return {name: {"id": item["Id"], "image_id": item["Image"]}
            for name, item in zip(NAMES, items)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confirm-existing-maintenance", action="store_true", required=True)
    parser.parse_args()
    original = CONFIG.read_bytes()
    assert original.count(b"request_timeout: 180") == 1, "Unexpected starting config"
    initial_stat = CONFIG.stat()
    initial_ids = identities()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    baseline = "p1-final-base-" + stamp
    candidate = "p1-final-test-" + stamp
    run(str(RELEASE), "capture", baseline)
    try:
        with tempfile.TemporaryDirectory(prefix="phase1-config-drill-") as directory:
            path = Path(directory) / "candidate.yaml"
            changed = original.replace(b"request_timeout: 180", b"request_timeout: 181", 1)
            path.write_bytes(changed)
            run(str(RELEASE), "capture", candidate, "--config", str(path))
            run(str(RELEASE), "deploy", candidate)
            assert CONFIG.read_bytes() == changed
            assert CONFIG.stat().st_ino == initial_stat.st_ino
            run(str(RELEASE), "rollback", baseline)
    finally:
        if CONFIG.read_bytes() != original:
            run(str(RELEASE), "rollback", baseline)
    assert CONFIG.read_bytes() == original, "Original config was not restored"
    assert CONFIG.stat().st_ino == initial_stat.st_ino, "Bind mount inode changed"
    assert identities() == initial_ids, "Existing container/image identity changed"
    run(str(INFRA / "scripts/health/check-all.sh"))
    print("P1_CONFIG_ROLLBACK " + json.dumps({"baseline": baseline, "candidate": candidate,
          "original_config_sha256": hashlib.sha256(original).hexdigest(),
          "config_exactly_restored": True, "inode_preserved": True,
          "same_container_ids_and_images": True, "scope": "config-only; same image/schema"}))


if __name__ == "__main__":
    main()
```

## 28. llm-gateway-infra/scripts/ci/validate-compose.py

SHA-256: `d56a79b316d382550e22946ca9ef2f28a43f752553045056558d4ba624f6eeb4`

```python
#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml


def fail(message: str) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    sys.exit(1)


if len(sys.argv) not in {3, 4}:
    fail(
        "Usage: "
        "validate-compose.py "
        "<base|dev> <compose-json|-> [base-compose-yaml]"
    )


mode = sys.argv[1]
compose_file = Path(sys.argv[2])


if mode not in {
    "base",
    "dev",
}:
    fail(
        "mode must be 'base' or 'dev'"
    )


if sys.argv[2] != "-" and not compose_file.exists():
    fail(
        f"Compose JSON not found: "
        f"{compose_file}"
    )


if sys.argv[2] == "-":
    compose = json.load(sys.stdin)
else:
    with compose_file.open(encoding="utf-8") as f:
        compose = json.load(f)


services = compose.get(
    "services",
    {}
)


required_services = {
    "litellm",
    "postgres",
    "redis",
}


missing_services = (
    required_services
    - set(services)
)

if missing_services:
    fail(
        "Missing service(s): "
        + ", ".join(
            sorted(missing_services)
        )
    )


def ports(
    service_name: str,
) -> list[dict[str, Any]]:

    value = (
        services
        .get(service_name, {})
        .get("ports", [])
    )

    return value or []


def networks(
    service_name: str,
) -> set[str]:

    value = (
        services
        .get(service_name, {})
        .get("networks", {})
    )

    if isinstance(value, dict):
        return set(value)

    if isinstance(value, list):
        return set(value)

    return set()


#
# All services must be connected to
# the private backend network.
#

for service_name in required_services:

    service_networks = networks(
        service_name
    )

    if "llm-backend" not in service_networks:
        fail(
            f"{service_name} is not connected "
            "to llm-backend"
        )


#
# LiteLLM must publish port 4000.
#

litellm_ports = ports("litellm")

has_litellm_4000 = any(
    int(port.get("target", 0)) == 4000
    and str(
        port.get("published", "")
    ) == "4000"
    for port in litellm_ports
)

if not has_litellm_4000:
    fail(
        "LiteLLM must publish port 4000"
    )


#
# LiteLLM config mount must be read-only.
#

litellm_volumes = (
    services["litellm"]
    .get("volumes", [])
    or []
)

config_mount = None

for volume in litellm_volumes:

    if not isinstance(volume, dict):
        continue

    if (
        volume.get("target")
        == "/app/config.yaml"
    ):
        config_mount = volume
        break


if config_mount is None:
    fail(
        "LiteLLM config volume "
        "is not mounted at /app/config.yaml"
    )


if not config_mount.get(
    "read_only",
    False,
):
    fail(
        "LiteLLM config mount "
        "must be read-only"
    )


source_file = (Path(sys.argv[3]) if len(sys.argv) == 4 else
               Path(__file__).resolve().parents[2] / "docker-compose.yml")
try:
    source = yaml.safe_load(source_file.read_text())
    declared = [volume for volume in source["services"]["litellm"]["volumes"]
                if isinstance(volume, dict) and volume.get("target") == "/app/config.yaml"]
    source_is_safe = (len(declared) == 1 and declared[0].get("type") == "bind"
                      and declared[0].get("bind", {}).get("create_host_path") is False)
except (OSError, yaml.YAMLError, KeyError, TypeError, AttributeError):
    source_is_safe = False
# Compose releases differ: some JSON serializers omit false values (or the entire
# empty bind object). Require explicit false in the source and reject normalized
# true/null; never infer safety from an omitted source option.
normalized_bind = config_mount.get("bind", {})
normalized_is_safe = (isinstance(normalized_bind, dict)
                      and ("create_host_path" not in normalized_bind
                           or normalized_bind["create_host_path"] is False))
if config_mount.get("type") != "bind" or not source_is_safe or not normalized_is_safe:
    fail("LiteLLM config bind must set create_host_path=false")


#
# Base compose:
#
# Postgres / Redis may be exposed
# internally, but must NOT be
# published to the host.
#

if mode == "base":

    if ports("postgres"):
        fail(
            "PostgreSQL must not publish "
            "a host port in base compose"
        )

    if ports("redis"):
        fail(
            "Redis must not publish "
            "a host port in base compose"
        )


#
# Development override:
#
# Host ports are allowed, but only
# through 127.0.0.1.
#

if mode == "dev":

    expected = {
        "postgres": 5432,
        "redis": 6379,
    }

    for service_name, expected_port \
            in expected.items():

        service_ports = ports(
            service_name
        )

        matching = [
            port
            for port in service_ports
            if int(
                port.get(
                    "target",
                    0,
                )
            ) == expected_port
        ]

        if not matching:
            fail(
                f"{service_name} must publish "
                f"{expected_port} in dev mode"
            )

        for port in matching:

            host_ip = port.get(
                "host_ip"
            )

            if host_ip != "127.0.0.1":
                fail(
                    f"{service_name} dev port "
                    "must bind to 127.0.0.1, "
                    f"got: {host_ip!r}"
                )


print(
    f"Docker Compose "
    f"{mode} validation: PASS"
)
```

## 29. llm-gateway-infra/scripts/ci/test-compose-contract.py

SHA-256: `d91ff54edf9b88f5e0a2621b74b0264d13b78f0276b939c43817be981d77a1fb`

```python
#!/usr/bin/env python3
"""Regression for Compose JSON serializers that omit explicitly false bind options."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


VALIDATOR = Path(__file__).with_name("validate-compose.py")


class ConfigBindContractTests(unittest.TestCase):
    def check_contract(self, *, normalized=None, declared=None, expected=0):
        mount = {"type": "bind", "target": "/app/config.yaml", "read_only": True,
                 "bind": {"create_host_path": False}}
        source_mount = copy.deepcopy(mount)
        if normalized is not None:
            mount = normalized
        if declared is None:
            declared = [source_mount]
        services = {name: {"networks": {"llm-backend": {}}}
                    for name in ("postgres", "redis", "litellm")}
        services["litellm"].update(ports=[{"target": 4000, "published": "4000"}], volumes=[mount])
        source = {"services": {"litellm": {"volumes": declared}}}
        with tempfile.TemporaryDirectory(prefix="compose-contract-") as directory:
            path = Path(directory) / "source.yaml"
            path.write_text(yaml.safe_dump(source))
            result = subprocess.run([sys.executable, str(VALIDATOR), "base", "-", str(path)],
                                    input=json.dumps({"services": services}), capture_output=True,
                                    text=True, timeout=10, check=False)
        self.assertEqual(result.returncode, expected, result.stderr)
        if expected:
            self.assertIn("create_host_path=false", result.stderr)

    def mount(self, **updates):
        return {"type": "bind", "target": "/app/config.yaml", "read_only": True, **updates}

    def test_explicit_normalized_false_is_accepted(self):
        self.check_contract()

    def test_omitted_normalized_bind_is_accepted_with_explicit_source_false(self):
        self.check_contract(normalized=self.mount())

    def test_empty_normalized_bind_is_accepted_with_explicit_source_false(self):
        self.check_contract(normalized=self.mount(bind={}))

    def test_normalized_true_or_null_is_rejected(self):
        for value in (True, None):
            with self.subTest(value=value):
                self.check_contract(normalized=self.mount(bind={"create_host_path": value}), expected=1)

    def test_explicit_source_true_is_rejected(self):
        self.check_contract(normalized=self.mount(),
                            declared=[self.mount(bind={"create_host_path": True})], expected=1)

    def test_omitted_source_option_is_rejected(self):
        self.check_contract(normalized=self.mount(), declared=[self.mount()], expected=1)

    def test_short_source_syntax_is_rejected(self):
        self.check_contract(declared=["./config.yaml:/app/config.yaml:ro"], expected=1)

    def test_duplicate_source_mount_is_rejected(self):
        mount = self.mount(bind={"create_host_path": False})
        self.check_contract(declared=[mount, copy.deepcopy(mount)], expected=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## 30. llm-gateway-infra/scripts/ci/validate.sh

SHA-256: `bc3665772531a23b155e306bec00ba7b6bfcb46853bee685488f4f3f5cc907b5`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")" &&
  pwd
)"

REPO_ROOT="$(
  cd "$SCRIPT_DIR/../.." &&
  pwd
)"

cd "$REPO_ROOT"

echo
echo "======================================"
echo "LLM Gateway Infra Validation"
echo "======================================"

echo
echo "[1/7] Bash syntax"

while IFS= read -r -d '' file; do
  echo "Checking: $file"
  bash -n "$file"
done < <(
  find scripts \
    -type f \
    -name "*.sh" \
    -print0
)

echo "Bash syntax: PASS"


echo
echo "[2/7] ShellCheck"

if ! command -v shellcheck >/dev/null; then
  echo "ERROR: shellcheck is not installed."
  exit 1
fi

find scripts \
  -type f \
  -name "*.sh" \
  -print0 \
  | xargs -0 shellcheck \
      --severity=warning

echo "ShellCheck: PASS"


echo
echo "[3/7] Environment template"

python3 \
  scripts/ci/validate-env-example.py


echo
echo "[4/7] Base Docker Compose"

LITELLM_CONFIG_PATH="$REPO_ROOT/.github/fixtures/litellm_config.yaml"
export LITELLM_CONFIG_PATH

docker compose \
  config \
  --quiet

docker compose \
  config \
  --format json \
  | python3 scripts/ci/validate-compose.py base -


echo
echo "[5/7] Development override"

docker compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  config \
  --quiet

docker compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  config \
  --format json \
  | python3 scripts/ci/validate-compose.py dev -


echo
echo "[6/7] Operational regression tests"

python3 scripts/ci/test-operations.py
python3 scripts/ci/test-compose-contract.py

echo
echo "[7/7] Git safety"

if git ls-files \
    | grep -qE '(^|/)\.env$'; then

    echo "ERROR: .env is tracked by Git."
    exit 1
fi

if git ls-files \
    | grep -qE '\.(dump|sql)$'; then

    echo "ERROR: database backup "
    echo "is tracked by Git."
    exit 1
fi


echo
echo "======================================"
echo "INFRA VALIDATION: PASSED"
echo "======================================"
```

## 31. llm-gateway-docs/.github/workflows/validate.yml

SHA-256: `2dee530289e73947074daf91a458a4ea9806fa66e479b56e783256a9bbe67ad1`

```yaml
name: Validate Documentation

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  validate:
    name: Validate Documentation
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout
        uses: actions/checkout@v7
      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - name: Validate standalone documentation
        run: python scripts/validate-docs.py
```

## 32. llm-gateway-docs/reports/phase1-final-evidence/audit-final.py

SHA-256: `43c9b3aa06ce65cf7e27e3a08619b6cf75bed3251fcabc9a6054e5133a8b5d37`

```python
"""Read-only aggregate audit; never persist raw gateway logs, keys or messages."""
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone


OUT = Path(__file__).resolve().parent
SINCE = "2026-10-17T03:54:52Z"


def capture(*args):
    return subprocess.check_output(args, text=True, errors="replace")


def query(sql):
    return json.loads(capture("docker", "exec", "llm-gateway-postgres", "psql", "-U", "litellm",
                              "-d", "litellm", "-At", "-c", sql))


def main():
    privacy = query('''SELECT json_build_object(
        'rows',count(*),
        'messages_nonempty',count(*) FILTER (WHERE COALESCE(messages::text,'null') NOT IN ('null','[]','{}','""')),
        'responses_nonempty',count(*) FILTER (WHERE COALESCE(response::text,'null') NOT IN ('null','[]','{}','""')),
        'raw_key_pattern_rows',count(*) FILTER (WHERE concat(api_key,messages::text,response::text,metadata::text)
            ~ 'sk-[A-Za-z0-9_-]{20,}'))
        FROM "LiteLLM_SpendLogs" WHERE "startTime">='2026-10-17 03:54:52'::timestamp''')
    keys = query('''SELECT json_build_object('created',count(*),
        'unblocked',count(*) FILTER (WHERE blocked IS NOT TRUE))
        FROM "LiteLLM_VerificationToken" WHERE created_at>='2026-10-17 03:54:52'::timestamp
        AND (key_alias LIKE 'e2e-%' OR user_id LIKE 'e2e-%')''')
    teams = query('''SELECT json_build_object('created',count(*),
        'unblocked',count(*) FILTER (WHERE blocked IS NOT TRUE))
        FROM "LiteLLM_TeamTable" WHERE created_at>='2026-10-17 03:54:52'::timestamp
        AND team_alias LIKE 'e2e-%' ''')
    spend = query('''SELECT json_build_object('paid_rows',count(*),'native_spend_usd',COALESCE(sum(spend),0))
        FROM "LiteLLM_SpendLogs" WHERE "startTime">='2026-10-17 03:54:52'::timestamp
        AND "user" LIKE 'e2e-%' AND spend>0''')
    logs = subprocess.run(["docker", "logs", "--since", SINCE, "llm-gateway"],
                          check=True, capture_output=True, text=True, errors="replace")
    raw = logs.stdout + logs.stderr  # In memory only. Neither stream is printed/saved.
    log_privacy = {"lines": len(raw.splitlines()),
        "raw_key_pattern_matches": len(re.findall(r"\bsk-[A-Za-z0-9_-]{20,}\b", raw)),
        "toy_source_marker_present": "def subtotal_cents(" in raw,
        "toy_response_marker_present": '"receipt":' in raw}
    del raw, logs
    names = ["llm-gateway", "llm-gateway-postgres", "llm-gateway-redis"]
    inspected = json.loads(capture("docker", "inspect", *names))
    runtime = {name: {"id": item["Id"], "image_id": item["Image"],
                      "image_tag": item["Config"]["Image"], "running": item["State"]["Running"]}
               for name, item in zip(names, inspected)}
    images = json.loads(capture("docker", "image", "inspect", *[item["Image"] for item in inspected]))
    for name, item in zip(names, images):
        runtime[name]["repo_digests"] = item.get("RepoDigests", [])
        runtime[name]["platform"] = item["Os"] + "/" + item["Architecture"]
    result = {"captured_at": datetime.now(timezone.utc).isoformat(), "since_utc": SINCE,
              "scope": "current goal window; aggregate inspection, not all historical traffic",
              "spend_privacy": privacy, "fixture_keys": keys, "fixture_teams": teams,
              "fixture_usage": spend, "runtime_log_privacy": log_privacy, "runtime": runtime}
    (OUT / "privacy-cleanup-runtime-final.json").write_text(json.dumps(result, indent=2) + "\n")
    assert privacy["rows"] > 0 and keys["created"] > 0 and teams["created"] > 0
    assert all(privacy[field] == 0 for field in ("messages_nonempty", "responses_nonempty", "raw_key_pattern_rows"))
    assert keys["unblocked"] == teams["unblocked"] == 0, "Fixture cleanup incomplete"
    assert log_privacy["raw_key_pattern_matches"] == 0, "Raw-key pattern found; investigate privately"
    assert not log_privacy["toy_source_marker_present"] and not log_privacy["toy_response_marker_present"]
    assert all(item["running"] for item in runtime.values())
    assert [runtime[name]["id"][:12] for name in names] == ["9c77da1dea53", "2abff28af371", "04c48e8f579d"]
    print("FINAL_AGGREGATE_PRIVACY_CLEANUP_RUNTIME: PASS")


if __name__ == "__main__":
    main()
```
