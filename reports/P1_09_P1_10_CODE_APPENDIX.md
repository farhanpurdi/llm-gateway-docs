# Lampiran kode P1-09/P1-10

Snapshot source 2026-10-13, Asia/Jakarta. Baca [laporan sederhana](P1_09_P1_10_LIMITS_COST_REPORT.md) dahulu.
Baca hanya file terkait; snapshot mencakup isi lengkap sebelas file yang ditambah/diubah pada sesi ini.
File shared juga berisi implementasi sesi lama yang tetap dipertahankan. Secret runtime tidak dicantumkan.

| File | SHA-256 |
|---|---|
| [llm-gateway-infra/scripts/teams/add-member.sh](../../llm-gateway-infra/scripts/teams/add-member.sh) | `2497cedc9fa4896e2afa018f7a58e906500363aeeab70d7a3dca72afd4a7c76a` |
| [llm-gateway-infra/scripts/ci/test-operations.py](../../llm-gateway-infra/scripts/ci/test-operations.py) | `dd4122fc15dc68b03e3e13a0c650633af505f378bca2b9fc93aca0b3c3bb9cc8` |
| [llm-gateway-e2e/requirements.txt](../../llm-gateway-e2e/requirements.txt) | `3329ef44d4e998ae4854a3804b7016800b702ff34c5a65bc9973b5da053aaab2` |
| [llm-gateway-e2e/tests/client.py](../../llm-gateway-e2e/tests/client.py) | `403ca0bc397aef52615a554299c8c2528f661fdedea902e1e6527c89e549e751` |
| [llm-gateway-e2e/tests/conftest.py](../../llm-gateway-e2e/tests/conftest.py) | `33f0eb27d5ce4804690dbe71dbfa1e13a688840dd8ca1b67b85b99a0e3fcc87d` |
| [llm-gateway-e2e/tests/accounting.py](../../llm-gateway-e2e/tests/accounting.py) | `4404fc37a5c1d941f24f478cae72bbb4ef809e135072d8a29506910bb02b25df` |
| [llm-gateway-e2e/tests/test_pilot_limits.py](../../llm-gateway-e2e/tests/test_pilot_limits.py) | `2436f542d19fed52a145236398cad8b9921625a679b208cecda843a3e4ac5312` |
| [llm-gateway-e2e/tests/test_spend.py](../../llm-gateway-e2e/tests/test_spend.py) | `d74c339724a8fd60ad450b8e7922f16f428b73c0dae7ceee53f6962222660d1a` |
| [llm-gateway-e2e/tests/unit/test_accounting.py](../../llm-gateway-e2e/tests/unit/test_accounting.py) | `a69ebad2f27e4b283096ad91c2f59d0c1edb9ef01542050c2d6afbe58993feef` |
| [llm-gateway-e2e/tests/unit/test_suite_validator.py](../../llm-gateway-e2e/tests/unit/test_suite_validator.py) | `30988ed8539270071626e3ff8b2f88266250c3672ea56bdb6395eaf70d2fcfd9` |
| [llm-gateway-e2e/scripts/ci/validate-suite.py](../../llm-gateway-e2e/scripts/ci/validate-suite.py) | `66d657679e74793e81c0e0606a6859c2527e49bdb471aac8b5b163ac2badd08e` |

## llm-gateway-infra/scripts/teams/add-member.sh

SHA-256: `2497cedc9fa4896e2afa018f7a58e906500363aeeab70d7a3dca72afd4a7c76a`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"

if [ "$#" -ne 3 ]; then
    echo "Usage:"
    echo "  $0 <team-id> <user-id> <team-policy-name>"
    exit 1
fi

TEAM_ID="$1"
USER_ID="$2"
POLICY_NAME="$3"

POLICY_FILE="$LLM_GATEWAY_CONFIG_DIR/policies/teams/${POLICY_NAME}.yaml"

POLICY_JSON="$(
    python3 "$REPO_ROOT/scripts/lib/read-team-policy.py" \
        "$POLICY_FILE"
)"

MEMBER_BUDGET="$(
python3 - "$POLICY_JSON" <<'PY'
import json
import sys

policy = json.loads(sys.argv[1])

print(
    policy["limits"]["member"]["monthly_budget_usd"]
)
PY
)"

BODY="$(
python3 - "$TEAM_ID" "$USER_ID" "$MEMBER_BUDGET" <<'PY'
import json
import sys

team_id = sys.argv[1]
user_id = sys.argv[2]
member_budget = float(sys.argv[3])

print(json.dumps({
    "team_id": team_id,
    "max_budget_in_team": member_budget,
    "budget_duration": "30d",
    "member": {
        "role": "user",
        "user_id": user_id,
    }
}))
PY
)"

litellm_admin_request \
    POST \
    /team/member_add \
    "$BODY" \
    | python3 -m json.tool
```

## llm-gateway-infra/scripts/ci/test-operations.py

SHA-256: `dd4122fc15dc68b03e3e13a0c650633af505f378bca2b9fc93aca0b3c3bb9cc8`

```python
#!/usr/bin/env python3
"""Offline failure-path checks; Docker and the real .env are never used."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('release_manager', ROOT / 'scripts/release/manage.py')
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)
CONFIG = b'''model_list:
- model_name: company-fast
  litellm_params: {model: openai/gpt-5.6-terra, api_key: os.environ/OPENAI_API_KEY}
- model_name: company-coding
  litellm_params: {model: openai/gpt-5.6-sol, api_key: os.environ/OPENAI_API_KEY}
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
'''


class Operations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.envfile = self.path / '.env'
        self.envfile.write_text(f'LITELLM_BASE_URL=http://localhost:4000\nLITELLM_MASTER_KEY=test-only\n'
                                f'POSTGRES_DB=litellm\nPOSTGRES_USER=litellm\nLLM_GATEWAY_CONFIG_DIR={ROOT}\n')
        binary = self.path / 'docker'
        binary.write_text('#!/bin/sh\necho UNEXPECTED_DOCKER >&2\nexit 99\n')
        binary.chmod(0o700)
        self.env = dict(os.environ, LLM_GATEWAY_ENV_FILE=str(self.envfile),
                        PATH=f'{self.path}:{os.environ["PATH"]}')
        self.release_patch = patch.object(manager, 'RELEASES', self.path / 'releases')
        self.release_patch.start()
        self.addCleanup(self.release_patch.stop)
        manager.RELEASES.mkdir()

    def shell(self, script, *args, **env):
        return subprocess.run(['bash', str(ROOT / 'scripts' / script), *args],
                              env={**self.env, **env}, text=True, capture_output=True)

    def test_main_database_restore_rejected_before_docker(self):
        for target in ('litellm', 'other', 'litellm;drop', '-bad'):
            with self.subTest(target=target):
                result = self.shell('backup/restore-postgres-test.sh', 'missing.dump', RESTORE_DB=target)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('dedicated', result.stderr)
                self.assertNotIn('UNEXPECTED_DOCKER', result.stderr)

    def test_readiness_rejects_healthy_http_when_dependency_fails(self):
        curl = self.path / "curl"
        curl.write_text("#!/bin/sh\nexit 0\n")
        curl.chmod(0o700)
        result = self.shell("health/readiness.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("readiness (HTTP + dependencies): OK", result.stdout)

    def test_restore_rejects_postgres_identifier_truncation(self):
        self.envfile.write_text(self.envfile.read_text().replace("POSTGRES_DB=litellm", "POSTGRES_DB=" + "a" * 63))
        result = self.shell("backup/restore-postgres-test.sh", "missing.dump")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dedicated", result.stderr)
        self.assertNotIn("UNEXPECTED_DOCKER", result.stderr)

    def test_common_preserves_callers_script_directory(self):
        result = subprocess.run(['bash', '-c',
            f'SCRIPT_DIR=caller; source "{ROOT}/scripts/lib/common.sh"; test "$SCRIPT_DIR" = caller'],
            env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 0)

    def test_onboard_requires_policy_before_creating_user(self):
        result = self.shell('onboard-developer.sh', 'test-user', 'test-team')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('team-policy-name', result.stdout)
        self.assertNotIn('unbound variable', result.stderr)

    def test_policy_scripts_preserve_team_and_member_monthly_limits(self):
        config = self.path / 'config'
        policies = config / 'policies/teams'
        policies.mkdir(parents=True)
        policy = {'name': 'pilot', 'models': ['company-fast', 'company-coding'],
                  'limits': {'team': {'monthly_budget_usd': 10, 'rpm': 30, 'tpm': 100000},
                             'member': {'monthly_budget_usd': 2}}}
        (policies / 'pilot.yaml').write_text(yaml.safe_dump(policy))
        self.envfile.write_text(self.envfile.read_text().replace(
            f'LLM_GATEWAY_CONFIG_DIR={ROOT}', f'LLM_GATEWAY_CONFIG_DIR={config}'))
        capture = self.path / 'request.json'
        curl = self.path / 'curl'
        curl.write_text(f'#!{__import__("sys").executable}\n'
                        'import json,sys\nfrom pathlib import Path\n'
                        f'Path({str(capture)!r}).write_text(sys.argv[sys.argv.index("-d")+1])\n'
                        'print(json.dumps({"team_id":"unit-team"}))\n')
        curl.chmod(0o700)
        cases = [
            ('teams/create-team.sh', ('pilot',), {'team_alias': 'pilot',
             'models': policy['models'], 'max_budget': 10, 'budget_duration': '30d',
             'rpm_limit': 30, 'tpm_limit': 100000}),
            ('teams/add-member.sh', ('unit-team', 'unit-user', 'pilot'),
             {'team_id': 'unit-team', 'max_budget_in_team': 2,
              'budget_duration': '30d', 'member': {'role': 'user', 'user_id': 'unit-user'}}),
        ]
        for script, args, expected in cases:
            with self.subTest(script=script):
                result = self.shell(script, *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(capture.read_text())
                self.assertEqual({field: payload.get(field) for field in expected}, expected)

    def test_corrupted_backup_rejected_before_docker(self):
        backup = self.path / 'bad.dump'
        backup.write_bytes(b'changed')
        Path(str(backup) + '.env').write_text('test')
        Path(str(backup) + '.json').write_text(json.dumps({'sha256': 'wrong', 'environment_sha256': 'wrong'}))
        result = self.shell('backup/verify-backup.sh', str(backup))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('checksum mismatch', result.stderr)
        self.assertNotIn('UNEXPECTED_DOCKER', result.stderr)

    def test_release_rejects_path_traversal(self):
        for name in ('../outside', '.', 'a/b', ''):
            with self.assertRaises(ValueError):
                manager.release_dir(name)

    def test_release_rejects_inline_credentials(self):
        with self.assertRaises(ValueError):
            manager.validate_config(CONFIG.replace(b'os.environ/OPENAI_API_KEY', b'inline-secret'))

    def test_release_rejects_removed_alias(self):
        with self.assertRaises(ValueError):
            manager.validate_config(CONFIG.replace(b'company-coding', b'other'))

    def test_release_accepts_approved_models_with_changed_timeout(self):
        doc = yaml.safe_load(CONFIG)
        doc['model_list'][1]['litellm_params']['timeout'] = 181
        manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_wrong_upstreams_for_each_alias(self):
        for index in (0, 1):
            for upstream in ('openai/unapproved', 'anthropic/unapproved', None):
                with self.subTest(index=index, upstream=upstream):
                    doc = yaml.safe_load(CONFIG)
                    doc['model_list'][index]['litellm_params']['model'] = upstream
                    with self.assertRaises(ValueError):
                        manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_duplicate_and_extra_aliases(self):
        for name in ('company-fast', 'extra'):
            with self.subTest(name=name):
                doc = yaml.safe_load(CONFIG)
                doc['model_list'].append({'model_name': name, 'litellm_params': {
                    'model': 'openai/gpt-5.6-terra', 'api_key': 'os.environ/OPENAI_API_KEY'}})
                with self.assertRaises(ValueError):
                    manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_malformed_shapes_with_value_error(self):
        for field, value in (('model_list', None), ('model_list', ['invalid']),
                             ('general_settings', []), ('router_settings', None)):
            with self.subTest(field=field, value=value):
                doc = yaml.safe_load(CONFIG)
                doc[field] = value
                with self.assertRaises(ValueError):
                    manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_different_environment_references(self):
        for field in ('api_key', 'master_key', 'database_url'):
            with self.subTest(field=field):
                doc = yaml.safe_load(CONFIG)
                target = doc['model_list'][0]['litellm_params'] if field == 'api_key' else doc['general_settings']
                target[field] = 'os.environ/OTHER_VARIABLE'
                with self.assertRaises(ValueError):
                    manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_provider_and_endpoint_overrides(self):
        for field, value in (('custom_llm_provider', 'anthropic'),
                             ('api_base', 'https://example.invalid'),
                             ('base_url', 'https://example.invalid'), ('api_type', 'azure')):
            with self.subTest(field=field):
                doc = yaml.safe_load(CONFIG)
                doc['model_list'][0]['litellm_params'][field] = value
                with self.assertRaises(ValueError):
                    manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_alternate_routing(self):
        for location in ('litellm_settings', 'router_settings', 'general_settings'):
            for field in ('fallbacks', 'model_group_alias', 'default_model'):
                with self.subTest(location=location, field=field):
                    doc = yaml.safe_load(CONFIG)
                    doc.setdefault(location, {})[field] = 'unapproved'
                    with self.assertRaises(ValueError):
                        manager.validate_config(yaml.safe_dump(doc))

    def test_release_rejects_invalid_and_duplicate_yaml(self):
        for content in (b'[broken', b'duplicate: 1\nduplicate: 2\n' + CONFIG):
            with self.assertRaises(ValueError):
                manager.validate_config(content)

    def test_capture_rejects_wrong_contract_before_creating_artifact(self):
        config = self.path / 'invalid.yaml'
        config.write_bytes(CONFIG.replace(b'openai/gpt-5.6-terra', b'openai/unapproved'))
        with patch.object(manager, 'runtime', return_value={'config_path': str(config)}), \
             patch.object(manager, 'revisions') as revisions:
            with self.assertRaises(ValueError):
                manager.capture('invalid')
        revisions.assert_not_called()
        self.assertFalse(manager.release_dir('invalid').exists())

    def test_release_rejects_wrong_contract_even_with_matching_checksum(self):
        release = manager.release_dir('wrong-contract')
        release.mkdir()
        candidate = CONFIG.replace(b'openai/gpt-5.6-terra', b'openai/unapproved')
        state = {'containers': {}, 'config_path': '/test', 'gateway': 'gateway'}
        (release / 'config.yaml').write_bytes(candidate)
        (release / 'manifest.json').write_text(json.dumps({**state, 'config_sha256': manager.digest(candidate)}))
        with self.assertRaises(ValueError):
            manager.load_release('wrong-contract', state)

    def test_config_write_preserves_bind_mount_inode(self):
        config = self.path / 'config.yaml'
        config.write_bytes(b'original-long-config')
        inode = config.stat().st_ino
        manager.write_config(config, b'short')
        self.assertEqual(config.read_bytes(), b'short')
        self.assertEqual(inode, config.stat().st_ino)

    def test_release_checksum_and_identity_guards(self):
        release = manager.release_dir('baseline')
        release.mkdir()
        (release / 'config.yaml').write_bytes(CONFIG)
        state = {'containers': {'gateway': {'id': 'same', 'image_id': 'sha256:test'}},
                 'config_path': '/test', 'gateway': 'gateway'}
        manifest = {**state, 'config_sha256': manager.digest(CONFIG)}
        (release / 'manifest.json').write_text(json.dumps(manifest))
        self.assertEqual(manager.load_release('baseline', state), CONFIG)
        with self.assertRaises(ValueError):
            manager.load_release('baseline', {**state, 'containers': {}})
        (release / 'config.yaml').write_bytes(CONFIG + b'\n')
        with self.assertRaises(ValueError):
            manager.load_release('baseline', state)

    def test_failed_deployment_recovers_original_config_and_records_failure(self):
        config = self.path / 'config.yaml'
        config.write_bytes(CONFIG)
        candidate = CONFIG + b'# candidate\n'
        state = {'config_path': str(config), 'gateway': 'existing'}
        checks = []
        def verify(_state, data):
            checks.append(data)
            if len(checks) == 1:
                raise RuntimeError('simulated failed readiness')
        with patch.object(manager, 'runtime', return_value=state), \
             patch.object(manager, 'load_release', return_value=candidate), \
             patch.object(manager, 'run', return_value=subprocess.CompletedProcess([], 0, stdout='backup.dump\n')), \
             patch.object(manager, 'verify', side_effect=verify):
            with self.assertRaisesRegex(RuntimeError, 'simulated'):
                manager.apply_release('candidate')
        self.assertEqual(config.read_bytes(), CONFIG)
        self.assertEqual(checks, [candidate, CONFIG])
        record = json.loads(next(manager.RELEASES.glob('operation-*.json')).read_text())
        self.assertEqual(record['status'], 'failed')
        self.assertEqual(record['recovery'], 'passed')
        self.assertEqual(Path(record['recovery_config']).read_bytes(), CONFIG)


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

## llm-gateway-e2e/requirements.txt

SHA-256: `3329ef44d4e998ae4854a3804b7016800b702ff34c5a65bc9973b5da053aaab2`

```text
pytest>=9.0.3,<9.1
requests>=2.32,<3.0
PyYAML>=6.0.3,<7
```

## llm-gateway-e2e/tests/client.py

SHA-256: `403ca0bc397aef52615a554299c8c2528f661fdedea902e1e6527c89e549e751`

```python
from __future__ import annotations

from typing import Any

import requests


class RedactedKey(str):
    """Keep HTTP behavior while hiding credentials in pytest/container reprs."""
    def __repr__(self):
        return '<redacted credential>'


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

## llm-gateway-e2e/tests/conftest.py

SHA-256: `33f0eb27d5ce4804690dbe71dbfa1e13a688840dd8ca1b67b85b99a0e3fcc87d`

```python
from __future__ import annotations

import os
import uuid
from pathlib import Path

import yaml

import pytest

from tests.client import LiteLLMClient, RedactedKey


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
```

## llm-gateway-e2e/tests/accounting.py

SHA-256: `4404fc37a5c1d941f24f478cae72bbb4ef809e135072d8a29506910bb02b25df`

```python
"""Independent checks for bounded, default-tier text requests; no HTTP here."""
from decimal import Decimal
import math


# Official OpenAI model pages verified 2026-10-13; USD per token.
# This is a test oracle, not a runtime price override.
PRICES = {
    'company-fast': {'upstream': 'openai/gpt-5.6-terra',
                     'input_cost_per_token': 0.000002,
                     'cache_read_input_token_cost': 0.0000002,
                     'output_cost_per_token': 0.000012},
    'company-coding': {'upstream': 'openai/gpt-5.6-sol',
                       'input_cost_per_token': 0.000004,
                       'cache_read_input_token_cost': 0.0000004,
                       'output_cost_per_token': 0.000020},
}
PRICE_SOURCES = {
    'company-fast': 'https://developers.openai.com/api/docs/models/gpt-5.6-terra',
    'company-coding': 'https://developers.openai.com/api/docs/models/gpt-5.6-sol',
}


def text_cost(alias, usage):
    counts = {name: usage.get(name) for name in (
        'prompt_tokens', 'completion_tokens', 'total_tokens')}
    details = usage.get('prompt_tokens_details') or {}
    cached = details.get('cached_tokens', 0)
    for value in [*counts.values(), cached]:
        if type(value) is not int or value < 0:
            raise AssertionError('Usage counts must be non-negative integers')
    prompt, output = counts['prompt_tokens'], counts['completion_tokens']
    if counts['total_tokens'] != prompt + output or cached > prompt:
        raise AssertionError('Inconsistent token usage')
    if prompt > 272000 or details.get('cache_creation_tokens', 0):
        raise AssertionError('Scenario is outside standard short-text pricing')
    prices = PRICES[alias]
    # Reasoning tokens are already part of completion_tokens; do not add twice.
    return sum(Decimal(str(prices[field])) * count for field, count in (
        ('input_cost_per_token', prompt - cached),
        ('cache_read_input_token_cost', cached), ('output_cost_per_token', output)))


def assert_spend_record(row, *, alias, usage, request_id, user_id, team_id, token):
    identity = {'request_id': request_id, 'user': user_id,
                'team_id': team_id, 'api_key': token}
    if any(row.get(field) != value for field, value in identity.items()):
        raise AssertionError('Request/key/user/team attribution mismatch')
    if row.get('model_group') != alias:
        raise AssertionError('Logical alias attribution mismatch')
    if row.get('model') not in {PRICES[alias]['upstream'], PRICES[alias]['upstream'].removeprefix('openai/')}:
        raise AssertionError('Upstream model attribution mismatch')
    for field in ('prompt_tokens', 'completion_tokens', 'total_tokens'):
        if row.get(field) != usage[field]:
            raise AssertionError('Stored token usage differs from provider response')
    spend = row.get('spend')
    if isinstance(spend, bool) or not isinstance(spend, (int, float)) or not math.isfinite(spend):
        raise AssertionError('Spend must be a finite number')
    expected = text_cost(alias, usage)
    if expected <= 0 or abs(Decimal(str(spend)) - expected) > Decimal('0.00000001'):
        raise AssertionError('Stored cost differs from independently calculated token cost')
    return expected
```

## llm-gateway-e2e/tests/test_pilot_limits.py

SHA-256: `2436f542d19fed52a145236398cad8b9921625a679b208cecda843a3e4ac5312`

```python
import json
import os
import time
from datetime import datetime, timezone, timedelta

import pytest


def complete(key, *, padding=0):
    return key['client'].post('/v1/chat/completions', json={
        'model': 'company-fast', 'messages': [{'role': 'user',
            'content': 'Reply with exactly: ok.\n' + 'context ' * padding}],
        'max_tokens': 16, 'reasoning_effort': 'none',
    })


def allowed(response):
    assert response.status_code == 200, f'Expected inference HTTP200, got {response.status_code}'
    return response.json()


def denied_budget(response, scope):
    assert response.status_code == 422, f'Expected exhausted {scope} HTTP422, got {response.status_code}'
    message = str(response.json().get('error', {}).get('message', '')).lower()
    assert 'budget' in message and scope in message, 'Wrong budget rejection scope'


def denied_rate(response):
    assert response.status_code == 429, f'Expected gateway HTTP429, got {response.status_code}'
    message = str(response.json().get('error', {}).get('message', '')).lower()
    assert 'team' in message and ('rate limit' in message or 'tpm' in message), 'Not a gateway team limit'


def wait_until(check, *, timeout=45):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = check()
        if value:
            return value
        time.sleep(1)
    raise AssertionError('Asynchronous budget/spend condition was not observed before timeout')


@pytest.mark.policy
def test_pilot_policy_is_persisted(admin_client, pilot_identity_factory, pilot_policy):
    ctx = pilot_identity_factory()
    team = admin_client.team_info(ctx['team_id'])['team_info']
    limits = pilot_policy['limits']['team']
    assert team['models'] == pilot_policy['models']
    assert team['max_budget'] == limits['monthly_budget_usd']
    assert team['rpm_limit'] == limits['rpm']
    assert team['tpm_limit'] == limits['tpm']
    assert team['budget_duration'] == '30d'
    reset = datetime.fromisoformat(team['budget_reset_at'].replace('Z', '+00:00'))
    assert timedelta(0) < reset-datetime.now(timezone.utc) <= timedelta(days=31)
    assert (reset.day, reset.hour, reset.minute, reset.second) == (1, 0, 0, 0)
    for uid in ctx['users']:
        budget = admin_client.member_info(ctx['team_id'], uid)['litellm_budget_table']
        assert budget['max_budget'] == pilot_policy['limits']['member']['monthly_budget_usd']
        assert budget['budget_duration'] == '30d'
        reset = datetime.fromisoformat(budget['budget_reset_at'].replace('Z', '+00:00'))
        assert timedelta(0) < reset-datetime.now(timezone.utc) <= timedelta(days=31)
        assert (reset.day, reset.hour, reset.minute, reset.second) == (1, 0, 0, 0)
    for key in ctx['keys']:
        info = admin_client.key_info(key['virtual_key'])
        assert info['max_budget'] is None  # Member budget is not multiplied per key.
    print('P1_POLICY '+json.dumps({'models': team['models'], 'team_usd': team['max_budget'],
          'member_usd': budget['max_budget'], 'rpm': team['rpm_limit'],
          'tpm': team['tpm_limit'], 'team_duration': '30d', 'member_duration': '30d',
          'reset_mode': 'calendar', 'next_reset_utc': team['budget_reset_at']}))


@pytest.mark.live
@pytest.mark.limits
@pytest.mark.parametrize('limit', ['rpm', 'tpm'])
def test_team_rate_limits_are_shared_and_recover(pilot_identity_factory, limit):
    ctx = pilot_identity_factory(team_limits={limit: 2 if limit == 'rpm' else 60})
    keys = ctx['keys']
    padding = 16 if limit == 'tpm' else 0
    allowed(complete(keys[0], padding=padding))
    if limit == 'rpm':
        allowed(complete(keys[2]))  # A different member consumes the same team RPM.
    denied_rate(complete(keys[1], padding=padding))  # Another key cannot bypass the limit.
    # Real recovery on the same team; never reset shared runtime counters.
    time.sleep(65)
    allowed(complete(keys[2], padding=padding))
    print('P1_LIMIT '+json.dumps({'scope': 'team', 'limit': limit,
                                 'shared_keys_members': True, 'recovery': True}))


@pytest.mark.live
@pytest.mark.limits
def test_member_budget_is_shared_across_keys(admin_client, pilot_identity_factory):
    tiny = 0.000001
    ctx = pilot_identity_factory(member_budget=tiny)
    keys = ctx['keys']
    allowed(complete(keys[0]))
    wait_until(lambda: (admin_client.member_info(ctx['team_id'], keys[0]['user_id']).get('spend') or 0) >= tiny)
    denied_budget(complete(keys[0]), 'team')
    denied_budget(complete(keys[1]), 'team')
    allowed(complete(keys[2]))  # Another member has an independent budget.
    print('P1_LIMIT '+json.dumps({'scope': 'member', 'both_keys_denied': True,
                                 'other_member_allowed': True}))


@pytest.mark.live
@pytest.mark.limits
def test_team_budget_blocks_all_members(admin_client, pilot_identity_factory):
    tiny = 0.000001
    ctx = pilot_identity_factory(team_limits={'monthly_budget_usd': tiny}, member_budget=None)
    allowed(complete(ctx['keys'][0]))
    wait_until(lambda: (admin_client.team_info(ctx['team_id'])['team_info'].get('spend') or 0) >= tiny)
    for key in (ctx['keys'][1], ctx['keys'][2]):
        denied_budget(complete(key), 'team')
    print('P1_LIMIT '+json.dumps({'scope': 'team_budget', 'all_members_denied': True}))


@pytest.mark.live
@pytest.mark.limits
def test_key_budget_does_not_block_other_keys(admin_client, pilot_identity_factory):
    tiny = 0.000001
    ctx = pilot_identity_factory(first_key_budget=tiny)
    allowed(complete(ctx['keys'][0]))
    wait_until(lambda: (admin_client.key_info(ctx['keys'][0]['virtual_key']).get('spend') or 0) >= tiny)
    denied_budget(complete(ctx['keys'][0]), 'budget')
    allowed(complete(ctx['keys'][1]))
    print('P1_LIMIT '+json.dumps({'scope': 'key', 'other_key_allowed': True}))


@pytest.mark.live
@pytest.mark.limits
def test_member_budget_window_resets_without_losing_total_spend(admin_client, pilot_identity_factory):
    ctx = pilot_identity_factory(member_budget=0.000001, member_duration='5s')
    key = ctx['keys'][0]
    before = admin_client.member_info(ctx['team_id'], key['user_id'])['litellm_budget_table']['budget_reset_at']
    allowed(complete(key))
    def reset_observed():
        member = admin_client.member_info(ctx['team_id'], key['user_id'])
        budget = member['litellm_budget_table']
        if budget['budget_reset_at'] > before and (member.get('spend') or 0) == 0 and (member.get('total_spend') or 0) > 0:
            return member
        return None
    # Pinned proxy checks due budgets every 597-605s; 5s is the budget window,
    # not the scheduler interval. Keep runtime settings unchanged.
    member = wait_until(reset_observed, timeout=int(os.getenv('E2E_BUDGET_RESET_TIMEOUT', '660')))
    assert member['litellm_budget_table']['max_budget'] == 0.000001
    allowed(complete(ctx['keys'][1]))
    print('P1_LIMIT '+json.dumps({'scope': 'member_reset', 'test_duration': '5s',
                                 'cycle_spend_reset': True, 'total_spend_retained': True}))
```

## llm-gateway-e2e/tests/test_spend.py

SHA-256: `d74c339724a8fd60ad450b8e7922f16f428b73c0dae7ceee53f6962222660d1a`

```python
import json
import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from tests.accounting import PRICES, assert_spend_record, text_cost


@pytest.mark.live
@pytest.mark.spend
@pytest.mark.parametrize('alias', ['company-fast', 'company-coding'])
def test_spend_is_attributed_to_user(admin_client, pilot_identity_factory, alias):
    """Match provider response to persisted tokens, cost, key, member, user and team."""
    assert admin_client.model_prices() == PRICES, 'Active prices/mapping differ from official test snapshot'
    ctx = pilot_identity_factory()
    start = (datetime.now(timezone.utc)-timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
    requests = []
    for key in (ctx['keys'][0], ctx['keys'][2]):
        response = key['client'].post('/v1/chat/completions', json={
            'model': alias, 'messages': [{'role': 'user', 'content': 'Reply with exactly: ok.'}],
            'max_tokens': 16, 'reasoning_effort': 'none', 'service_tier': 'default',
        })
        assert response.status_code == 200, f'Expected inference HTTP200, got {response.status_code}'
        body = response.json()
        assert body.get('service_tier', 'default') == 'default', 'Scenario requires standard pricing'
        usage = body['usage']
        # Pinned LiteLLM stores the provider response ID, not x-litellm-call-id.
        request_id = body.get('id')
        assert request_id, 'Provider response identifier missing'
        expected = text_cost(alias, usage)
        key_alias = admin_client.key_info(key['virtual_key'])['key_alias']
        token = next(item['token'] for item in admin_client.list_user_keys(user_id=key['user_id'])
                     if item['key_alias'] == key_alias)
        requests.append({'key': key, 'token': token, 'request_id': request_id,
                         'usage': usage, 'expected': expected})

    end = (datetime.now(timezone.utc)+timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
    deadline = time.monotonic()+45
    rows = {}
    while time.monotonic() < deadline:
        for item in requests:
            page = admin_client.list_user_spend_logs_page(
                user_id=item['key']['user_id'], start_date=start, end_date=end)
            assert not page.get('total_is_capped', False)
            assert page['total'] == len(page['data']), 'Unexpected history pagination/truncation'
            matches = [row for row in page['data'] if row.get('request_id') == item['request_id']]
            assert len(matches) <= 1, 'Duplicate request in spend history'
            if matches:
                rows[item['request_id']] = matches[0]
        if len(rows) == len(requests):
            break
        time.sleep(1)
    expected_count = len(requests)
    assert len(rows) == expected_count, 'Spend records did not persist before deadline'

    expected_total = Decimal(0)
    for item in requests:
        expected_total += assert_spend_record(
            rows[item['request_id']], alias=alias, usage=item['usage'],
            request_id=item['request_id'], user_id=item['key']['user_id'],
            team_id=ctx['team_id'], token=item['token'])

    # Request rows and aggregate counters flush asynchronously and separately.
    deadline = time.monotonic()+45
    aggregates_match = False
    while time.monotonic() < deadline:
        actual = []
        for item in requests:
            uid = item['key']['user_id']
            user = admin_client.expect_json(admin_client.get('/user/info', params={'user_id': uid}))['user_info']
            actual.extend([
                (admin_client.key_info(item['key']['virtual_key']).get('spend'), item['expected']),
                (admin_client.member_info(ctx['team_id'], uid).get('spend'), item['expected']),
                (user.get('spend'), item['expected']),
            ])
        actual.append((admin_client.team_info(ctx['team_id'])['team_info'].get('spend'), expected_total))
        aggregates_match = all(value is not None and abs(Decimal(str(value))-expected) <= Decimal('0.00000001')
                               for value, expected in actual)
        if aggregates_match:
            break
        time.sleep(1)
    assert aggregates_match, 'Key/member/user/team aggregates differ from request cost'
    print('P1_ACCOUNTING '+json.dumps({
        'alias': alias, 'upstream': PRICES[alias]['upstream'], 'requests': len(requests),
        'tokens': [item['usage'] for item in requests],
        'expected_usd': float(expected_total),
        'stored_usd': sum(rows[item['request_id']]['spend'] for item in requests),
        'key_member_user_team_match': True,
    }))
```

## llm-gateway-e2e/tests/unit/test_accounting.py

SHA-256: `a69ebad2f27e4b283096ad91c2f59d0c1edb9ef01542050c2d6afbe58993feef`

```python
from copy import deepcopy
from decimal import Decimal

import pytest

from tests.accounting import PRICES, assert_spend_record, text_cost
from tests.client import LiteLLMClient, RedactedKey


pytestmark = pytest.mark.unit
USAGE = {'prompt_tokens': 100, 'completion_tokens': 10, 'total_tokens': 110,
         'prompt_tokens_details': {'cached_tokens': 20},
         'completion_tokens_details': {'reasoning_tokens': 5}}


@pytest.mark.parametrize('alias,expected', [('company-fast', '0.000284'), ('company-coding', '0.000528')])
def test_cost_discounts_cached_input_and_does_not_double_count_reasoning(alias, expected):
    assert text_cost(alias, USAGE) == Decimal(expected)


@pytest.mark.parametrize('field,value', [('prompt_tokens', -1), ('completion_tokens', True),
    ('total_tokens', 111), ('prompt_tokens', float('nan')), ('completion_tokens', None)])
def test_invalid_provider_usage_is_rejected(field, value):
    usage = deepcopy(USAGE)
    usage[field] = value
    with pytest.raises(AssertionError):
        text_cost('company-fast', usage)


@pytest.mark.parametrize('cached', [-1, 101, True])
def test_impossible_cache_usage_is_rejected(cached):
    usage = deepcopy(USAGE)
    usage['prompt_tokens_details']['cached_tokens'] = cached
    with pytest.raises(AssertionError):
        text_cost('company-fast', usage)


@pytest.mark.parametrize('case', ['long-context', 'cache-write'])
def test_nonstandard_pricing_is_not_silently_counted_as_standard(case):
    usage = deepcopy(USAGE)
    if case == 'long-context':
        usage.update(prompt_tokens=272001, total_tokens=272011)
    else:
        usage['prompt_tokens_details']['cache_creation_tokens'] = 1
    with pytest.raises(AssertionError, match='outside standard'):
        text_cost('company-fast', usage)


@pytest.mark.parametrize('field,value', [('request_id', 'wrong'), ('user', 'other'),
    ('team_id', 'other'), ('api_key', 'other'), ('model_group', 'company-coding'),
    ('model', 'wrong'), ('prompt_tokens', 99), ('completion_tokens', 9),
    ('total_tokens', 109), ('spend', 0.1), ('spend', float('nan')), ('spend', True)])
def test_wrong_attribution_tokens_and_cost_fail_the_live_assertion(field, value):
    row = {'request_id': 'request', 'user': 'user', 'team_id': 'team', 'api_key': 'token',
           'model_group': 'company-fast', 'model': 'gpt-5.6-terra',
           **{name: USAGE[name] for name in ('prompt_tokens', 'completion_tokens', 'total_tokens')},
           'spend': float(text_cost('company-fast', USAGE))}
    row[field] = value
    with pytest.raises(AssertionError):
        assert_spend_record(row, alias='company-fast', usage=USAGE,
                            request_id='request', user_id='user', team_id='team', token='token')


def test_model_info_and_errors_never_return_credentials(offline_client, json_response):
    offline_client.get.side_effect = None
    offline_client.get.return_value = json_response({'data': [{
        'model_name': 'company-fast', 'litellm_params': {'model': PRICES['company-fast']['upstream'], 'api_key': 'private-key'},
        'model_info': PRICES['company-fast'],
    }]})
    assert offline_client.model_prices() == {'company-fast': PRICES['company-fast']}
    assert 'private-key' not in str(offline_client.model_prices())
    with pytest.raises(AssertionError) as error:
        offline_client.expect_json(json_response({'key': 'private-key'}, status=500))
    assert 'private-key' not in str(error.value)


def test_pytest_container_repr_hides_credentials_but_http_auth_still_works():
    key = RedactedKey('private-key')
    assert 'private-key' not in repr({'virtual_key': key})
    assert LiteLLMClient('http://unused.invalid', key).headers['Authorization'] == 'Bearer private-key'
```

## llm-gateway-e2e/tests/unit/test_suite_validator.py

SHA-256: `30988ed8539270071626e3ff8b2f88266250c3672ea56bdb6395eaf70d2fcfd9`

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

SHA-256: `66d657679e74793e81c0e0606a6859c2527e49bdb471aac8b5b163ac2badd08e`

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
