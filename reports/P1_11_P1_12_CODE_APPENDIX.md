# Lampiran kode P1-11/P1-12

Snapshot2026-10-17, Asia/Jakarta. Baca [laporan sederhana](P1_11_P1_12_OPENCODE_REPORT.md) dahulu.
Delapan file source lengkap; shared file juga mempertahankan pekerjaan sesi lama.
Tidak memuat environment/runtime credential. Baca file terkait saja.

| Source | SHA-256 |
|---|---|
| [llm-gateway-e2e/tests/conftest.py](../../llm-gateway-e2e/tests/conftest.py) | `2cd0abe4c6fc6b2b0f08de21b3eca47164b9af87f32f942712d9bee6cde4d4d9` |
| [llm-gateway-e2e/tests/opencode.py](../../llm-gateway-e2e/tests/opencode.py) | `b9697262e937533be8ad17aa12d12d8a56e56bfc31db792abdba0271ed170bb6` |
| [llm-gateway-e2e/tests/test_opencode.py](../../llm-gateway-e2e/tests/test_opencode.py) | `9c97323b1b98dfb51eaf91c157a74521d5137bb80fe8ac57974172b0d7a1d2fb` |
| [llm-gateway-e2e/tests/test_inference.py](../../llm-gateway-e2e/tests/test_inference.py) | `f4f670b674063a30e9d86ba307b9fd400f8dccb855b5905b3c0667ee497f5d8a` |
| [llm-gateway-e2e/tests/unit/test_opencode.py](../../llm-gateway-e2e/tests/unit/test_opencode.py) | `f31325cea1770f8bcbc50d3e7c5244684c55b1bc3afcdcc422691037b0caef33` |
| [llm-gateway-e2e/tests/unit/test_suite_validator.py](../../llm-gateway-e2e/tests/unit/test_suite_validator.py) | `ac09b3a8daf038aaef85cb3aae8955934f99ccc4a4d681931fe0ccfbf50b8b34` |
| [llm-gateway-e2e/scripts/ci/validate-suite.py](../../llm-gateway-e2e/scripts/ci/validate-suite.py) | `c12c7be279d004e72f18736b2217aa9c4db490712a37f1e7a0773bbf2ac744d6` |
| [llm-gateway-e2e/scripts/test-opencode.sh](../../llm-gateway-e2e/scripts/test-opencode.sh) | `01c259a3e2e3cebac1667dbebaa5458bc526fc5925e7358609404ea5a507e642` |

## llm-gateway-e2e/tests/conftest.py

SHA-256: `2cd0abe4c6fc6b2b0f08de21b3eca47164b9af87f32f942712d9bee6cde4d4d9`

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
def e2e_identity(
    admin_client: LiteLLMClient,
    fast_model: str,
    coding_model: str,
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

    virtual_key = key_data["key"]

    context = {
        "user_id": user_id,
        "team_id": team_id,
        "team_alias": team_alias,
        "key_alias": key_alias,
        "virtual_key": virtual_key,
    }

    yield context

    #
    # Cleanup
    #
    # Jangan print key.
    #

    try:
        admin_client.post(
            "/key/block",
            json={
                "key": virtual_key,
            },
        )
    finally:
        #
        # Buat team hasil test inert.
        #
        admin_client.post(
            "/team/update",
            json={
                "team_id": team_id,
                "blocked": True,
            },
        )


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

    virtual_key = key_data["key"]

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

    #
    # Cleanup
    #
    # Jangan print virtual key.
    #

    try:
        admin_client.post(
            "/key/block",
            json={
                "key": virtual_key,
            },
        )
    finally:
        admin_client.post(
            "/team/update",
            json={
                "team_id": team_id,
                "blocked": True,
            },
        )


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

    virtual_key = key_data["key"]

    context = {
        "user_id": user_id,
        "team_id": team_id,
        "team_alias": team_alias,
        "key_alias": key_alias,
        "virtual_key": virtual_key,
        "max_budget": key_max_budget,
    }

    yield context

    #
    # Cleanup
    #

    try:
        admin_client.post(
            "/key/block",
            json={
                "key": virtual_key,
            },
        )
    finally:
        admin_client.post(
            "/team/update",
            json={
                "team_id": team_id,
                "blocked": True,
            },
        )


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
               first_key_budget=None):
        limits = {**pilot_policy['limits']['team'], **(team_limits or {})}
        budget = (pilot_policy['limits']['member']['monthly_budget_usd']
                  if member_budget == 'policy' else member_budget)
        suffix = uuid.uuid4().hex[:8]
        team = admin_client.expect_json(admin_client.post('/team/new', json={
            'team_alias': 'e2e-p109-'+suffix, 'models': pilot_policy['models'],
            'max_budget': limits['monthly_budget_usd'], 'budget_duration': '30d',
            'rpm_limit': limits['rpm'], 'tpm_limit': limits['tpm'],
            'metadata': {'environment': 'e2e', 'purpose': 'P1-09-P1-10', 'policy': 'pilot'},
        }))
        ctx = {'team_id': team['team_id'], 'users': [], 'keys': []}
        created.append(ctx)  # Register immediately so partial provisioning is cleaned up.
        for user_number in range(2):
            uid = f'e2e-p109-{suffix}-{user_number}'
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
                           'key_alias': f'e2e-p109-{suffix}-{user_number}-{key_number}',
                           'models': ['all-team-models'],
                           'metadata': {'environment': 'e2e', 'purpose': 'P1-09-P1-10'}}
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

## llm-gateway-e2e/tests/opencode.py

SHA-256: `b9697262e937533be8ad17aa12d12d8a56e56bfc31db792abdba0271ed170bb6`

```python
"""CLI adapter and pure evidence checks; gateway HTTP remains in client.py."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import signal
import subprocess


PROMPT = (
    "Read calculator.py. Fix subtotal_cents so it returns the sum of integer "
    "prices, including zero for an empty list. Use your editing tool to change "
    "calculator.py, then execute exactly python3 verify.py using your shell tool. "
    "Do not read or edit the verifier or other files. If verification fails, fix "
    "the function and run the same verifier again. Finish with PASS and the full "
    "receipt value printed by the successful verifier. Keep the answer brief."
)

VERIFIER = '''import json
from pathlib import Path
import uuid
from calculator import subtotal_cents

for values in ([], [99], [120, 230, 50], [-50, 20], [7] * 13):
    assert subtotal_cents(values) == sum(values)
receipt = {"status": "PASS", "receipt": uuid.uuid4().hex}
Path("receipt.json").write_text(json.dumps(receipt))
print(json.dumps(receipt))
'''


def cli_environment(state_dir: Path, virtual_key: str) -> dict[str, str]:
    """No master/provider keys, personal auth, or plugins inherited by the agent."""
    env = {"PATH": os.environ["PATH"], "NO_COLOR": "1", "TERM": "dumb",
           "COMPANY_LLM_API_KEY": virtual_key}
    for name in ("DATA", "CONFIG", "STATE", "CACHE"):
        env[f"XDG_{name}_HOME"] = str(state_dir / name.lower())
    return env


def prepare_project(project: Path, template: dict, base_url: str) -> dict:
    project.mkdir(parents=True)
    config = copy.deepcopy(template)
    provider = config["providers"]["company-ai"]
    provider["settings"].update(baseURL=base_url.rstrip("/") + "/v1", timeout=60000)
    provider["body"] = {"max_tokens": 768, "reasoning_effort": "none"}
    config.update(
        snapshots=False,
        policies=[
            {"action": "provider.use", "resource": "*", "effect": "deny"},
            {"action": "provider.use", "resource": "company-ai", "effect": "allow"},
        ],
        agents={"build": {"steps": 8}, "title": {"disabled": True}},
        permissions=[
            {"action": "*", "resource": "*", "effect": "deny"},
            {"action": "read", "resource": "calculator.py", "effect": "allow"},
            {"action": "edit", "resource": "calculator.py", "effect": "allow"},
            {"action": "shell", "resource": "python3 verify.py", "effect": "allow"},
            {"action": "external_directory", "resource": "*", "effect": "deny"},
        ],
    )
    (project / "opencode.json").write_text(json.dumps(config, indent=2) + "\n")
    (project / "calculator.py").write_text("def subtotal_cents(prices):\n    return len(prices)\n")
    (project / "verify.py").write_text(VERIFIER)
    return config


def run_cli(command: list[str], *, cwd: Path, env: dict, timeout: int = 180) -> str:
    """Capture output privately; fail without copying a credential/body into pytest."""
    process = subprocess.Popen(command, cwd=cwd, env=env, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    try:
        stdout, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise AssertionError("OpenCode command timed out; raw output suppressed") from None
    if process.returncode:
        errors = []
        for line in stdout.splitlines():
            try:
                event = json.loads(line)
                if isinstance(event, dict) and event.get("type") == "error":
                    detail = event.get("error", {})
                    errors.append({"type": detail.get("type"), "status": detail.get("status")})
            except ValueError:
                pass
        raise AssertionError(f"OpenCode command failed (exit {process.returncode}); categories={errors}; raw output suppressed")
    return stdout


def parse_events(output: str) -> list[dict]:
    try:
        events = [json.loads(line) for line in output.splitlines() if line.strip()]
        assert events and all(isinstance(event, dict) for event in events)
    except (ValueError, AssertionError):
        raise AssertionError("Invalid OpenCode JSON events; raw output suppressed") from None
    if any(event.get("type") == "error" for event in events):
        raise AssertionError("OpenCode emitted an error event; raw output suppressed")
    return events


def assert_agent_workflow(events: list[dict], receipt: dict) -> dict:
    """A printed success marker alone must never pass agent acceptance."""
    assert receipt.get("status") == "PASS", "Verifier did not pass"
    nonce = receipt.get("receipt")
    assert isinstance(nonce, str) and len(nonce) == 32, "Invalid verifier receipt"
    completed = []
    final_text = ""
    read_index = edit_index = shell_index = final_index = None
    for index, event in enumerate(events):
        part = event.get("part", {})
        state = part.get("state", {})
        tool = part.get("tool")
        if tool and state.get("status") == "completed":
            completed.append(tool)
            if tool == "read" and "calculator.py" in json.dumps(state.get("input", {})):
                read_index = index
            if tool in ("edit", "write", "patch") and "calculator.py" in json.dumps(state.get("input", {})):
                edit_index = index
            if tool in ("shell", "bash") and state.get("input", {}).get("command", "").strip() == "python3 verify.py":
                if nonce in str(state.get("output", "")):
                    shell_index = index
        if event.get("type") == "text":
            final_text += part.get("text", "")
            if nonce in final_text:
                final_index = index
    assert all(i is not None for i in (read_index, edit_index, shell_index, final_index)), "Missing read/edit/shell/tool-result evidence"
    assert read_index < edit_index < shell_index < final_index, "Tool result was not consumed after verification"
    assert "PASS" in final_text, "Agent did not report successful verification"
    return {"completed_tools": completed, "receipt_consumed": True,
            "read_edit_verify_order": True, "event_count": len(events)}
```

## llm-gateway-e2e/tests/test_opencode.py

SHA-256: `9c97323b1b98dfb51eaf91c157a74521d5137bb80fe8ac57974172b0d7a1d2fb`

```python
import hashlib
import json
import subprocess
import sys
import time

import pytest

from tests.accounting import PRICES
from tests.opencode import PROMPT, VERIFIER, assert_agent_workflow, parse_events, run_cli


def test_opencode_onboarding_uses_developer_key(admin_client, opencode_developer, pilot_policy):
    ctx = opencode_developer
    key = admin_client.key_info(ctx["virtual_key"])
    assert key["user_id"] == ctx["user_id"]
    assert key["team_id"] == ctx["team_id"]
    assert key["models"] == ["all-team-models"]
    team = admin_client.team_info(ctx["team_id"])["team_info"]
    assert set(team["models"]) == set(pilot_policy["models"])
    for field, policy_name in (("max_budget", "monthly_budget_usd"),
                               ("rpm_limit", "rpm"), ("tpm_limit", "tpm")):
        assert team[field] == pilot_policy["limits"]["team"][policy_name]
    budget = admin_client.member_info(ctx["team_id"], ctx["user_id"])["litellm_budget_table"]
    assert budget["max_budget"] == pilot_policy["limits"]["member"]["monthly_budget_usd"]
    assert budget["budget_duration"] == "30d" and budget["budget_reset_at"]
    models = ctx["client"].expect_json(ctx["client"].get("/v1/models"))["data"]
    assert {row["id"] for row in models} == set(pilot_policy["models"])
    user = admin_client.expect_json(admin_client.get("/user/info", params={"user_id": ctx["user_id"]}))["user_info"]
    assert user["user_role"] == "internal_user"
    print("P1_ONBOARDING " + json.dumps({"user_id": ctx["user_id"], "team_id": ctx["team_id"],
          "models": sorted(team["models"]), "policy": "pilot", "operator_script": True}))


@pytest.mark.live
@pytest.mark.parametrize("alias", ["company-fast", "company-coding"])
def test_opencode_agent_reads_edits_runs_and_uses_tool_result(
        admin_client, opencode_developer, opencode_project, alias):
    project = opencode_project["path"]
    output = run_cli(
        [opencode_project["executable"], "run", "--standalone", "--format", "json",
         "--agent", "build", "--model", "company-ai/" + alias, PROMPT],
        cwd=project, env=opencode_project["env"],
    )
    events = parse_events(output)
    print("P1_OPENCODE_TRACE " + json.dumps({"alias": alias, "events": [
        {"type": event.get("type"), "tool": event.get("part", {}).get("tool"),
         "status": event.get("part", {}).get("state", {}).get("status")}
        for event in events]}))
    receipt_path = project / "receipt.json"
    assert receipt_path.exists(), "The real verifier did not run"
    assert (project / "verify.py").read_text() == VERIFIER, "Agent modified the verifier"
    summary = assert_agent_workflow(events, json.loads(receipt_path.read_text()))
    # Independently execute the unchanged verifier against the resulting code.
    check = subprocess.run([sys.executable, "verify.py"], cwd=project,
                           capture_output=True, text=True, timeout=10, check=False)
    assert check.returncode == 0, "Resulting code failed independent verification"
    ctx = opencode_developer
    expected_requests = sum(event.get("type") == "step_start" for event in events)
    assert 1 <= expected_requests <= 8, "Agent exceeded the bounded scenario"
    keys = admin_client.list_user_keys(user_id=ctx["user_id"])
    assert len(keys) == 1, "Expected one developer credential"
    rows = []
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        history = admin_client.list_user_spend_logs_page(
            user_id=ctx["user_id"], start_date="2026-01-01 00:00:00", end_date="2099-01-01 00:00:00")
        assert not history.get("total_is_capped", False)
        assert history["total"] == len(history["data"]), "Unexpected history truncation"
        rows = [row for row in history["data"] if row.get("model_group") == alias]
        if len(rows) == expected_requests and sum(row.get("completion_tokens", 0) for row in rows) > 0:
            break
        time.sleep(1)
    assert len(rows) == expected_requests, "OpenCode request history is incomplete or unexpected"
    for row in rows:
        assert row["user"] == ctx["user_id"] and row["team_id"] == ctx["team_id"]
        assert row["api_key"] == keys[0]["token"], "Spend belongs to a different credential"
        assert row["model"] in {PRICES[alias]["upstream"], PRICES[alias]["upstream"].removeprefix("openai/")}
        assert 0 <= row["completion_tokens"] <= 768, "Output exceeded fixture token bound"
    summary.update(alias=alias, user_id=ctx["user_id"], team_id=ctx["team_id"],
                   persisted_requests=len(rows),
                   prompt_tokens=sum(row["prompt_tokens"] for row in rows),
                   completion_tokens=sum(row["completion_tokens"] for row in rows),
                   native_spend_usd=sum(row["spend"] for row in rows),
                   code=(project / "calculator.py").read_text(),
                   code_sha256=hashlib.sha256((project / "calculator.py").read_bytes()).hexdigest())
    print("P1_OPENCODE_AGENT " + json.dumps(summary))
```

## llm-gateway-e2e/tests/test_inference.py

SHA-256: `f4f670b674063a30e9d86ba307b9fd400f8dccb855b5905b3c0667ee497f5d8a`

```python
import json

import pytest


@pytest.mark.live
def test_company_fast_inference(
    user_client,
    fast_model,
):
    response = user_client.post(
        "/v1/chat/completions",
        json={
            "model": fast_model,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Reply exactly with "
                        "E2E_FAST_OK"
                    ),
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    content = (
        data["choices"][0]
        ["message"]
        ["content"]
    )

    assert "E2E_FAST_OK" in content


@pytest.mark.live
def test_company_coding_inference(
    user_client,
    coding_model,
):
    response = user_client.post(
        "/v1/chat/completions",
        json={
            "model": coding_model,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Reply exactly with "
                        "E2E_CODING_OK"
                    ),
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    content = (
        data["choices"][0]
        ["message"]
        ["content"]
    )

    assert "E2E_CODING_OK" in content


@pytest.mark.live
@pytest.mark.parametrize("model_fixture", ["fast_model", "coding_model"])
def test_streaming(
    user_client,
    request,
    model_fixture,
):
    response = user_client.post(
        "/v1/chat/completions",
        stream=True,
        json={
            "model": request.getfixturevalue(model_fixture),
            "stream": True,
            "max_tokens": 32,
            "reasoning_effort": "none",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Reply exactly with "
                        "E2E_STREAM_OK"
                    ),
                }
            ],
        },
    )

    assert response.status_code == 200

    chunks = []
    done_received = False

    for raw_line in response.iter_lines(
        decode_unicode=True
    ):
        if not raw_line:
            continue

        if not raw_line.startswith("data: "):
            continue

        payload = raw_line[6:]

        if payload == "[DONE]":
            done_received = True
            break

        data = json.loads(payload)

        delta = (
            data
            .get("choices", [{}])[0]
            .get("delta", {})
            .get("content")
        )

        if delta:
            chunks.append(delta)

    content = "".join(chunks)

    assert done_received
    assert "E2E_STREAM_OK" in content

@pytest.mark.live
@pytest.mark.parametrize("model_fixture", ["fast_model", "coding_model"])
def test_tool_calling(user_client, request, model_fixture):
    """Both aliases must preserve structured tool calls needed by coding clients."""
    response = user_client.post(
        "/v1/chat/completions",
        json={
            "model": request.getfixturevalue(model_fixture),
            "messages": [{"role": "user", "content": "Look up the status of ticket TICKET-123."}],
            "tools": [{
                "type": "function",
                "function": {
                    "name": "lookup_ticket",
                    "description": "Return the status of a ticket.",
                    "parameters": {
                        "type": "object",
                        "properties": {"ticket_id": {"type": "string"}},
                        "required": ["ticket_id"],
                        "additionalProperties": False,
                    },
                },
            }],
            "tool_choice": {"type": "function", "function": {"name": "lookup_ticket"}},
        },
    )
    assert response.status_code == 200
    calls = response.json()["choices"][0]["message"]["tool_calls"]
    assert len(calls) == 1
    assert calls[0]["id"]
    assert calls[0]["type"] == "function"
    assert calls[0]["function"]["name"] == "lookup_ticket"
    assert json.loads(calls[0]["function"]["arguments"]) == {"ticket_id": "TICKET-123"}
```

## llm-gateway-e2e/tests/unit/test_opencode.py

SHA-256: `f31325cea1770f8bcbc50d3e7c5244684c55b1bc3afcdcc422691037b0caef33`

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
    template = json.loads((Path(__file__).resolve().parents[3] /
                          "llm-gateway-config/clients/opencode/opencode.jsonc").read_text())
    before = copy.deepcopy(template)
    config = prepare_project(tmp_path / "project", template, "http://localhost:4000")
    assert template == before
    assert set(config["providers"]) == {"company-ai"}
    assert set(config["providers"]["company-ai"]["models"]) == {"company-fast", "company-coding"}
    assert config["agents"]["build"]["steps"] == 8
    assert config["providers"]["company-ai"]["body"]["max_tokens"] == 768
    assert {"action": "external_directory", "resource": "*", "effect": "deny"} in config["permissions"]
```

## llm-gateway-e2e/tests/unit/test_suite_validator.py

SHA-256: `ac09b3a8daf038aaef85cb3aae8955934f99ccc4a4d681931fe0ccfbf50b8b34`

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

## llm-gateway-e2e/scripts/ci/validate-suite.py

SHA-256: `c12c7be279d004e72f18736b2217aa9c4db490712a37f1e7a0773bbf2ac744d6`

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

## llm-gateway-e2e/scripts/test-opencode.sh

SHA-256: `01c259a3e2e3cebac1667dbebaa5458bc526fc5925e7358609404ea5a507e642`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Actual operator onboarding, both aliases and verified agent tool execution.
# The standard live runner loads the existing infra environment privately.
exec "$SCRIPT_DIR/run-live.sh" tests/test_opencode.py "$@"
```
