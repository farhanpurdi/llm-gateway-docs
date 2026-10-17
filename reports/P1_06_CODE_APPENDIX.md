# Kode snapshot P1-06 — 2026-10-12

[Laporan dan batas hasil](P1_06_MODEL_CONTRACT_REPORT.md). Sepuluh file implementasi/tes berikut
adalah snapshot, bukan config runtime baru. Source aktif tetap di repo komponen.

Tes infra yang sudah ada dicantumkan bersama tambahan sesi ini agar file dapat dibaca utuh.

## llm-gateway-config/scripts/ci/model_contract.py

[Source aktif](../../llm-gateway-config/scripts/ci/model_contract.py) · SHA256 `b2b7c84e945d38388c1c745e324a5f9d5e320ff2b826d6df9bb97209e61f12ce`

```python
"""Offline Phase 1 contract shared by the config validator entrypoints."""
from pathlib import Path

import yaml


# Approved decisions must not be inferred from mutable catalogs.
PHASE1_MODELS = {
    "company-fast": "gpt-5.6-terra",
    "company-coding": "gpt-5.6-sol",
}
ENV_REFS = {
    "master_key": "os.environ/LITELLM_MASTER_KEY",
    "database_url": "os.environ/DATABASE_URL",
}
ROUTING_OVERRIDES = {
    "fallbacks", "default_fallbacks", "context_window_fallbacks",
    "content_policy_fallbacks", "model_group_alias", "default_model",
}


class ContractError(ValueError):
    """Invalid or inconsistent Phase 1 configuration."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than silently accepting the last value."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                if key in keys:
                    raise ContractError("duplicate YAML mapping key")
                keys.add(key)
            except TypeError as exc:
                raise ContractError("YAML mapping keys must be scalar values") from exc
        return super().construct_mapping(node, deep=deep)


def load_yaml(path):
    try:
        with Path(path).open(encoding="utf-8") as stream:
            data = yaml.load(stream, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError, ContractError) as exc:
        # Never echo YAML values: malformed files might contain credentials.
        raise ContractError(f"{path}: unreadable or invalid YAML ({type(exc).__name__})") from exc
    return mapping(data, str(path))


def mapping(value, location):
    if not isinstance(value, dict):
        raise ContractError(f"{location}: must be a YAML object")
    return value


def exact_aliases(names, location):
    if any(not isinstance(name, str) for name in names):
        raise ContractError(f"{location}: aliases must be strings")
    if len(names) != len(set(names)):
        raise ContractError(f"{location}: duplicate logical alias")
    if set(names) != set(PHASE1_MODELS):
        raise ContractError(f"{location}: expected exactly company-fast and company-coding")


def validate_runtime(config):
    config = mapping(config, "runtime config")
    models = config.get("model_list")
    if not isinstance(models, list):
        raise ContractError("model_list: must be a list")
    names = [mapping(item, f"model_list[{index}]").get("model_name")
             for index, item in enumerate(models)]
    exact_aliases(names, "model_list")
    routes = {}
    for item in models:
        name = item["model_name"]
        params = mapping(item.get("litellm_params"), f"{name}.litellm_params")
        expected = f"openai/{PHASE1_MODELS[name]}"
        if params.get("model") != expected:
            raise ContractError(f"{name}: upstream must be {expected}")
        if params.get("api_key") != "os.environ/OPENAI_API_KEY":
            raise ContractError(f"{name}: credential must use os.environ/OPENAI_API_KEY")
        if params.get("custom_llm_provider", "openai") != "openai":
            raise ContractError(f"{name}: provider override is not approved")
        if any(field in params for field in ("api_base", "base_url", "api_type")):
            raise ContractError(f"{name}: endpoint/type override requires an approved contract")
        routes[name] = params["model"]
    general = mapping(config.get("general_settings"), "general_settings")
    for field, expected in ENV_REFS.items():
        if general.get(field) != expected:
            raise ContractError(f"general_settings.{field}: must use {expected}")
    # Extra routing can bypass an otherwise correct model_list. Empty defaults are OK.
    for location, settings in [("config", config)] + [
        (key, mapping(config[key], key))
        for key in ("litellm_settings", "router_settings", "general_settings")
        if key in config
    ]:
        for field in ROUTING_OVERRIDES:
            if field in settings and settings[field] not in (None, [], {}):
                raise ContractError(f"{location}.{field}: alternate routing is not approved")
    return routes


def yaml_files(directory):
    if not directory.is_dir():
        raise ContractError(f"{directory}: directory not found")
    return sorted(set(directory.glob("*.yaml")) | set(directory.glob("*.yml")))


def validate_repository(root):
    """Require runtime, model files and provider catalog to agree with the ADRs."""
    root = Path(root)
    routes = validate_runtime(load_yaml(root / "config/litellm_config.yaml"))
    model_files = yaml_files(root / "models")
    exact_aliases([path.stem for path in model_files], "model catalog filenames")
    for path in model_files:
        name = path.stem  # Filename remains the logical identity.
        if path.name != f"{name}.yaml":
            raise ContractError(f"{path}: expected the approved .yaml filename")
        model = load_yaml(path)
        if "logical_name" in model:
            raise ContractError(f"{path}: logical identity must come from the filename")
        if "name" in model and model["name"] != name:
            raise ContractError(f"{path}: descriptive name differs from filename")
        if model.get("status") != "active":
            raise ContractError(f"{path}: approved model must be active")
        routing = mapping(model.get("routing"), f"{path}.routing")
        if set(routing) != {"primary"}:
            raise ContractError(f"{path}: only the approved primary route is allowed")
        primary = mapping(routing["primary"], f"{path}.routing.primary")
        if primary != {"provider": "openai", "model": PHASE1_MODELS[name]}:
            raise ContractError(f"{path}: primary route differs from the approved contract")
        if routes[name] != f"{primary['provider']}/{primary['model']}":
            raise ContractError(f"{path}: route differs from runtime")

    provider_files = yaml_files(root / "providers")
    if [path.name for path in provider_files] != ["openai.yaml"]:
        raise ContractError("provider catalog: expected only providers/openai.yaml")
    provider = load_yaml(provider_files[0])
    if provider.get("provider") != "openai" or provider.get("enabled") is not True:
        raise ContractError("provider catalog: OpenAI must be the only enabled provider")
    credential = mapping(provider.get("credential"), "provider.credential")
    if credential != {"type": "environment", "environment_variable": "OPENAI_API_KEY"}:
        raise ContractError("provider credential: must reference environment OPENAI_API_KEY")
    entries = provider.get("logical_models")
    if not isinstance(entries, list):
        raise ContractError("provider.logical_models: must be a list")
    names = [mapping(item, "provider.logical_models entry").get("logical_name")
             for item in entries]
    exact_aliases(names, "provider.logical_models")
    for item in entries:
        name = item["logical_name"]
        if item.get("enabled") is not True:
            raise ContractError(f"provider.{name}: approved route must be enabled")
        if item.get("provider_model") != PHASE1_MODELS[name]:
            raise ContractError(f"provider.{name}: upstream differs from runtime/model catalog")
    return routes


def cli(label):
    import sys
    try:
        routes = validate_repository(Path.cwd())
    except ContractError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for name, upstream in sorted(routes.items()):
        print(f"  {name} -> {upstream}")
    print(f"{label}: PASS (runtime + model catalog + OpenAI provider contract)")
    return 0
```

## llm-gateway-config/scripts/ci/validate-runtime-config.py

[Source aktif](../../llm-gateway-config/scripts/ci/validate-runtime-config.py) · SHA256 `579a15188a2838d0b4739bd0ca302ed6f040ae1d83c0f6a42938efd5a3f37ab6`

```python
#!/usr/bin/env python3
"""Validate the approved Phase 1 routing and its catalog consistency."""
from model_contract import cli


if __name__ == "__main__":
    raise SystemExit(cli("LiteLLM runtime config"))
```

## llm-gateway-config/scripts/ci/validate-model-catalog.py

[Source aktif](../../llm-gateway-config/scripts/ci/validate-model-catalog.py) · SHA256 `19e9ce9857b4441ae1f5650658dd162e058b9346aeadee3b20838d0fc5641f4e`

```python
#!/usr/bin/env python3
"""Validate filename identities, provider metadata and runtime routing together."""
from model_contract import cli


if __name__ == "__main__":
    raise SystemExit(cli("Model catalog validation"))
```

## llm-gateway-config/scripts/ci/test-model-contract.py

[Source aktif](../../llm-gateway-config/scripts/ci/test-model-contract.py) · SHA256 `452612fd5f4703be79a5c6097c619cb9d612586336abdaf7168ad5bcded4fdeb`

```python
#!/usr/bin/env python3
"""Exercise real validator CLIs against temporary, secret-free config copies."""
import copy
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = "config/litellm_config.yaml"
FAST = "models/company-fast.yaml"
CODING = "models/company-coding.yaml"
PROVIDER = "providers/openai.yaml"
PARAMS = ("model_list", 0, "litellm_params")
CASES = [
    ("runtime_empty", RUNTIME, (), {}),
    ("runtime_scalar", RUNTIME, (), "invalid"),
    ("runtime_models_null", RUNTIME, ("model_list",), None),
    ("runtime_models_empty", RUNTIME, ("model_list",), []),
    ("runtime_models_object", RUNTIME, ("model_list",), {}),
    ("runtime_entry_scalar", RUNTIME, ("model_list", 0), "invalid"),
    ("runtime_alias_not_string", RUNTIME, ("model_list", 0, "model_name"), ["company-fast"]),
    ("runtime_alias_unknown", RUNTIME, ("model_list", 0, "model_name"), "other"),
    ("runtime_alias_wildcard", RUNTIME, ("model_list", 0, "model_name"), "*"),
    ("runtime_alias_duplicate", RUNTIME, ("model_list", 1, "model_name"), "company-fast"),
    ("runtime_params_null", RUNTIME, PARAMS, None),
    ("runtime_wrong_fast", RUNTIME, PARAMS + ("model",), "openai/unapproved"),
    ("runtime_wrong_coding", RUNTIME, ("model_list", 1, "litellm_params", "model"), "openai/unapproved"),
    ("runtime_provider_other", RUNTIME, PARAMS + ("model",), "anthropic/unapproved"),
    ("runtime_no_provider_prefix", RUNTIME, PARAMS + ("model",), "gpt-5.6-terra"),
    ("runtime_credential_other_env", RUNTIME, PARAMS + ("api_key",), "os.environ/OTHER_KEY"),
    ("runtime_credential_inline", RUNTIME, PARAMS + ("api_key",), "test-placeholder"),
    ("runtime_provider_override", RUNTIME, PARAMS + ("custom_llm_provider",), "anthropic"),
    ("runtime_endpoint_override", RUNTIME, PARAMS + ("api_base",), "https://example.invalid/v1"),
    ("runtime_base_url_override", RUNTIME, PARAMS + ("base_url",), "https://example.invalid/v1"),
    ("runtime_api_type_override", RUNTIME, PARAMS + ("api_type",), "azure"),
    ("runtime_master_other_env", RUNTIME, ("general_settings", "master_key"), "os.environ/OTHER_KEY"),
    ("runtime_database_other_env", RUNTIME, ("general_settings", "database_url"), "os.environ/OTHER_DATABASE"),
    ("runtime_general_null", RUNTIME, ("general_settings",), None),
    ("runtime_settings_null", RUNTIME, ("litellm_settings",), None),
    ("runtime_fallback", RUNTIME, ("litellm_settings", "fallbacks"), [{"company-fast": ["other"]}]),
    ("runtime_router_alias", RUNTIME, ("router_settings",), {"model_group_alias": {"extra": "company-fast"}}),
    ("runtime_top_fallback", RUNTIME, ("fallbacks",), [{"company-fast": ["other"]}]),
    ("runtime_general_default", RUNTIME, ("general_settings", "default_model"), "other"),
    ("catalog_fast_provider", FAST, ("routing", "primary", "provider"), "anthropic"),
    ("catalog_fast_upstream", FAST, ("routing", "primary", "model"), "unapproved"),
    ("catalog_coding_upstream", CODING, ("routing", "primary", "model"), "unapproved"),
    ("catalog_name_disagrees", FAST, ("name",), "company-coding"),
    ("catalog_logical_name", FAST, ("logical_name",), "company-fast"),
    ("catalog_inactive", FAST, ("status",), "disabled"),
    ("catalog_routing_null", FAST, ("routing",), None),
    ("catalog_primary_null", FAST, ("routing", "primary"), None),
    ("catalog_fallback", FAST, ("routing", "fallback"), {"provider": "other", "model": "other"}),
    ("catalog_extra_endpoint", FAST, ("routing", "primary", "api_base"), "https://example.invalid"),
    ("provider_wrong_identity", PROVIDER, ("provider",), "anthropic"),
    ("provider_disabled", PROVIDER, ("enabled",), False),
    ("provider_enabled_string", PROVIDER, ("enabled",), "true"),
    ("provider_credential_type", PROVIDER, ("credential", "type"), "inline"),
    ("provider_credential_env", PROVIDER, ("credential", "environment_variable"), "OTHER_KEY"),
    ("provider_inline_credential", PROVIDER, ("credential", "value"), "test-placeholder"),
    ("provider_models_null", PROVIDER, ("logical_models",), None),
    ("provider_models_empty", PROVIDER, ("logical_models",), []),
    ("provider_entry_scalar", PROVIDER, ("logical_models", 0), "invalid"),
    ("provider_alias_duplicate", PROVIDER, ("logical_models", 1, "logical_name"), "company-fast"),
    ("provider_alias_unknown", PROVIDER, ("logical_models", 0, "logical_name"), "other"),
    ("provider_fast_upstream", PROVIDER, ("logical_models", 0, "provider_model"), "unapproved"),
    ("provider_coding_upstream", PROVIDER, ("logical_models", 1, "provider_model"), "unapproved"),
    ("provider_route_disabled", PROVIDER, ("logical_models", 0, "enabled"), False),
    ("provider_route_enabled_string", PROVIDER, ("logical_models", 0, "enabled"), "true"),
]


class ContractValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "config-repo"
        self.root.mkdir()
        self.env = dict(os.environ, PATH=f"{Path(sys.executable).parent}:{os.environ['PATH']}")
        for directory in ("config", "models", "providers", "scripts/ci", "policies", "clients"):
            shutil.copytree(ROOT / directory, self.root / directory, dirs_exist_ok=True)
        shutil.copy2(ROOT / "scripts/validate.sh", self.root / "scripts/validate.sh")
        shutil.copy2(ROOT / "README.md", self.root / "README.md")

    def change(self, file, keys, value):
        path = self.root / file
        doc = yaml.safe_load(path.read_text())
        if not keys:
            doc = value
        else:
            target = doc
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = value
        path.write_text(yaml.safe_dump(doc, sort_keys=False))

    def check(self, valid):
        for script in ("validate-runtime-config.py", "validate-model-catalog.py"):
            with self.subTest(entrypoint=script):
                result = subprocess.run([sys.executable, str(self.root / "scripts/ci" / script)],
                                        cwd=self.root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if valid else 1, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertIn("PASS" if valid else "ERROR:", result.stdout + result.stderr)

    def test_approved_config(self):
        self.check(True)

    def test_timeout_comment_and_order_changes_are_allowed(self):
        self.change(RUNTIME, PARAMS + ("timeout",), 181)
        for file, field in ((RUNTIME, "model_list"), (PROVIDER, "logical_models")):
            values = yaml.safe_load((self.root / file).read_text())[field]
            self.change(file, (field,), list(reversed(values)))
        with (self.root / RUNTIME).open("a") as stream:
            stream.write("\n# harmless comment\n")
        self.check(True)

    def test_model_identity_without_descriptive_name(self):
        path = self.root / FAST
        doc = yaml.safe_load(path.read_text())
        del doc["name"]
        path.write_text(yaml.safe_dump(doc))
        self.check(True)

    def test_runtime_extra_alias(self):
        models = yaml.safe_load((self.root / RUNTIME).read_text())["model_list"]
        extra = copy.deepcopy(models[0])
        extra["model_name"] = "extra"
        self.change(RUNTIME, ("model_list",), models + [extra])
        self.check(False)

    def test_provider_extra_alias(self):
        entries = yaml.safe_load((self.root / PROVIDER).read_text())["logical_models"]
        extra = copy.deepcopy(entries[0])
        extra["logical_name"] = "extra"
        self.change(PROVIDER, ("logical_models",), entries + [extra])
        self.check(False)

    def test_coordinated_wrong_route_in_all_three_sources_is_rejected(self):
        self.change(RUNTIME, PARAMS + ("model",), "openai/unapproved")
        self.change(FAST, ("routing", "primary", "model"), "unapproved")
        self.change(PROVIDER, ("logical_models", 0, "provider_model"), "unapproved")
        self.check(False)

    def test_missing_and_extra_catalog_files(self):
        for file in (FAST, CODING, PROVIDER):
            with self.subTest(file=file):
                path = self.root / file
                original = path.read_bytes()
                path.unlink()
                self.check(False)
                path.write_bytes(original)
        for file in ("models/extra.yaml", "providers/other.yml", "models/company-fast.yml"):
            with self.subTest(file=file):
                path = self.root / file
                path.write_text("{}\n")
                self.check(False)
                path.unlink()

    def test_yaml_duplicate_keys_and_malformed_content(self):
        for file in (RUNTIME, FAST, PROVIDER):
            path = self.root / file
            original = path.read_bytes()
            for content in ("duplicate: 1\nduplicate: 2\n" + original.decode(), "[broken", ""):
                with self.subTest(file=file,content=content[:10]):
                    path.write_text(content)
                    self.check(False)
            path.write_bytes(original)

    def test_both_shell_entrypoints_reject_wrong_routes(self):
        self.change(RUNTIME, PARAMS + ("model",), "openai/unapproved")
        for entrypoint in ("scripts/validate.sh", "scripts/ci/validate.sh"):
            with self.subTest(entrypoint=entrypoint):
                result = subprocess.run(["bash", str(self.root / entrypoint)], cwd=self.root,
                                        env=self.env, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("upstream must be", result.stderr)
                self.assertNotIn("CONFIG VALIDATION: PASSED", result.stdout)


def mutation_test(file, keys, value):
    def test(self):
        self.change(file, keys, value)
        self.check(False)
    return test


for name, file, keys, value in CASES:
    setattr(ContractValidation, f"test_{name}", mutation_test(file, keys, value))


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## llm-gateway-config/scripts/ci/validate.sh

[Source aktif](../../llm-gateway-config/scripts/ci/validate.sh) · SHA256 `36932f3876179fc032a431087b003866c62971216da0f4ab5e9f39b50031a738`

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
echo "LLM Gateway Config Validation"
echo "======================================"

echo
echo "[1/7] Required repository structure"

required_files=(
  "config/litellm_config.yaml"
  "models/company-fast.yaml"
  "models/company-coding.yaml"
  "providers/openai.yaml"
  "clients/opencode/opencode.jsonc"
  "README.md"
)

for file in "${required_files[@]}"; do

  if [ ! -f "$file" ]; then
    echo "ERROR: missing required file:"
    echo "$file"
    exit 1
  fi

  echo "OK: $file"

done

echo "Repository structure: PASS"


echo
echo "[2/7] YAML syntax"

python3 \
  scripts/ci/validate-yaml.py


echo
echo "[3/7] Logical model catalog and provider consistency"

python3 \
  scripts/ci/validate-model-catalog.py


echo
echo "[4/7] LiteLLM runtime contract"

python3 \
  scripts/ci/validate-runtime-config.py


echo
echo "[5/7] Team policies"

python3 \
  scripts/ci/validate-policies.py


echo
echo "[6/7] Offline contract regression tests"

python3 scripts/ci/test-model-contract.py

echo
echo "[7/7] Git safety"

if git ls-files \
  | grep -qE '(^|/)\.env$'; then

  echo "ERROR: .env is tracked by Git."
  exit 1
fi


if git ls-files \
  | grep -qE \
  '\.(pem|key|p12|pfx|dump|sql)$'; then

  echo "ERROR: sensitive file "
  echo "is tracked by Git."
  exit 1
fi


echo "Git safety: PASS"


echo
echo "======================================"
echo "CONFIG VALIDATION: PASSED"
echo "======================================"
```

## llm-gateway-config/scripts/validate.sh

[Source aktif](../../llm-gateway-config/scripts/validate.sh) · SHA256 `2524d8dc811d3ada7f2dc218e70efc09c42665919b054d52db7ee87341b213c9`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Keep the historical command while running the same complete checks as CI.
exec "$SCRIPT_DIR/ci/validate.sh" "$@"
```

## llm-gateway-infra/scripts/release/manage.py

[Source aktif](../../llm-gateway-infra/scripts/release/manage.py) · SHA256 `6ac0a3cd3455e8e7f17685f3b64d2580bbe46b08ef8009d24a3c80ef31514496`

```python
#!/usr/bin/env python3
"""Config releases on the SAME existing container. Never creates containers."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import yaml

ROOT = Path(__file__).resolve().parents[2]
RELEASES = ROOT / 'releases'


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                if key in keys:
                    raise ValueError('Duplicate YAML mapping key')
                keys.add(key)
            except TypeError as exc:
                raise ValueError('YAML mapping keys must be scalar values') from exc
        return super().construct_mapping(node, deep=deep)


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def release_dir(name):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', name):
        raise ValueError('Invalid release ID')
    path = RELEASES / name
    if path.is_symlink():
        raise ValueError('Release directory must not be a symlink')
    return path


def runtime():
    names = [os.environ.get(key, default) for key, default in (
        ('GATEWAY_CONTAINER', 'llm-gateway'),
        ('POSTGRES_CONTAINER', 'llm-gateway-postgres'),
        ('REDIS_CONTAINER', 'llm-gateway-redis'))]
    info = json.loads(run('docker', 'inspect', *names, capture_output=True).stdout)
    if not all(item['State']['Running'] for item in info):
        raise ValueError('All three existing containers must be running')
    gateway = info[0]
    mounts = [m for m in gateway['Mounts'] if m['Destination'] == '/app/config.yaml']
    if len(mounts) != 1 or mounts[0]['Type'] != 'bind' or mounts[0]['RW']:
        raise ValueError('Expected a read-only config bind mount')
    source = Path(mounts[0]['Source'])
    expected = Path(os.environ['LLM_GATEWAY_CONFIG_DIR']) / 'config/litellm_config.yaml'
    if source.resolve() != expected.resolve() or not source.is_file():
        raise ValueError('Config mount differs from the configured repository')
    if os.environ['LITELLM_BASE_URL'].rstrip('/') not in (
        'http://localhost:4000', 'http://127.0.0.1:4000'):
        raise ValueError('This procedure is limited to the existing local port 4000')
    ports = gateway['NetworkSettings']['Ports'].get('4000/tcp') or []
    if not any(p['HostPort'] == '4000' for p in ports):
        raise ValueError('Existing gateway is not published on port 4000')
    return {
        'containers': {n: {'id': c['Id'], 'image_id': c['Image'],
                            'image_tag': c['Config']['Image']} for n, c in zip(names, info)},
        'config_path': str(source), 'gateway': names[0],
    }


def validate_config(data):
    try:
        config = yaml.load(data, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError('Release config contains invalid YAML') from exc
    if not isinstance(config, dict):
        raise ValueError('Config must be a mapping')
    expected = {'company-fast': 'openai/gpt-5.6-terra',
                'company-coding': 'openai/gpt-5.6-sol'}
    models = config.get('model_list')
    if not isinstance(models, list) or any(not isinstance(m, dict) for m in models):
        raise ValueError('model_list must be a list of mappings')
    names = [m.get('model_name') for m in models]
    if (any(not isinstance(name, str) for name in names)
            or len(names) != len(set(names)) or set(names) != set(expected)):
        raise ValueError('Expected exactly two unique approved logical aliases')
    for model in models:
        params = model.get('litellm_params')
        if not isinstance(params, dict):
            raise ValueError('litellm_params must be a mapping')
        if params.get('model') != expected[model['model_name']]:
            raise ValueError('Upstream model differs from the approved Phase 1 contract')
        if params.get('api_key') != 'os.environ/OPENAI_API_KEY':
            raise ValueError('Provider key must reference os.environ/OPENAI_API_KEY')
        if params.get('custom_llm_provider', 'openai') != 'openai':
            raise ValueError('Provider override is not approved')
        if any(field in params for field in ('api_base', 'base_url', 'api_type')):
            raise ValueError('Endpoint/type override requires an approved contract')
    general = config.get('general_settings')
    if not isinstance(general, dict):
        raise ValueError('general_settings must be a mapping')
    for key, value in {'master_key': 'os.environ/LITELLM_MASTER_KEY',
                       'database_url': 'os.environ/DATABASE_URL'}.items():
        if general.get(key) != value:
            raise ValueError(f'{key} must reference {value}')
    overrides = ('fallbacks', 'default_fallbacks', 'context_window_fallbacks',
                 'content_policy_fallbacks', 'model_group_alias', 'default_model')
    settings = [('config', config)] + [(key, config[key]) for key in
        ('litellm_settings', 'router_settings', 'general_settings') if key in config]
    for location, value in settings:
        if not isinstance(value, dict):
            raise ValueError(f'{location} must be a mapping')
        if any(field in value and value[field] not in (None, [], {}) for field in overrides):
            raise ValueError('Alternate routing is not approved in Phase 1')


def revisions():
    result = {}
    for repo in ('llm-gateway-infra', 'llm-gateway-config', 'llm-gateway-e2e'):
        path = ROOT.parent / repo
        head = run('git', '-C', str(path), 'rev-parse', 'HEAD', capture_output=True).stdout.strip()
        status = run('git', '-C', str(path), 'status', '--porcelain', capture_output=True).stdout
        paths = run('git', '-C', str(path), 'ls-files', '-c', '-o', '--exclude-standard', '-z',
                    capture_output=True).stdout.split('\0')
        files = {name: digest((path / name).read_bytes()) for name in sorted(set(paths))
                 if name and (path / name).is_file()}
        result[repo] = {'head': head, 'dirty': bool(status), 'source_sha256': files}
    return result


def capture(name, config=None):
    state = runtime()
    data = Path(config or state['config_path']).read_bytes()
    validate_config(data)
    path = release_dir(name)
    path.mkdir(mode=0o700)  # Never overwrite an existing release.
    (path / 'config.yaml').write_bytes(data)
    manifest = {**state, 'created_at': datetime.now(timezone.utc).isoformat(),
                'config_sha256': digest(data), 'repositories': revisions()}
    (path / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Captured release: {name}')


def load_release(name, state):
    path = release_dir(name)
    manifest = json.loads((path / 'manifest.json').read_text())
    data = (path / 'config.yaml').read_bytes()
    if digest(data) != manifest['config_sha256']:
        raise ValueError('Release checksum mismatch')
    for key in ('containers', 'config_path', 'gateway'):
        if manifest[key] != state[key]:
            raise ValueError(f'Runtime changed ({key}); config-only rollback is unsafe')
    validate_config(data)
    return data


def write_config(path, data):
    # Write the existing inode: atomic rename would leave a file bind mount stale.
    with Path(path).open('r+b') as stream:
        stream.write(data)
        stream.truncate()
        stream.flush()
        os.fsync(stream.fileno())


def verify(state, data):
    deadline = time.monotonic() + 120
    while True:
        result = subprocess.run([str(ROOT / 'scripts/health/readiness.sh')],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            break
        if time.monotonic() >= deadline:
            raise RuntimeError('Gateway readiness timed out')
        time.sleep(2)
    mounted = subprocess.check_output(['docker', 'exec', state['gateway'], 'cat', '/app/config.yaml'])
    if digest(mounted) != digest(data):
        raise ValueError('Container is reading a stale config mount')
    run(str(ROOT / 'scripts/health/check-all.sh'))
    env = dict(os.environ, E2E_ENV_FILE=os.environ['ENV_FILE'])
    run(str(ROOT.parent / 'llm-gateway-e2e/scripts/run-smoke.sh'), env=env)


def apply_release(name):
    state = runtime()
    data = load_release(name, state)
    original = Path(state['config_path']).read_bytes()
    backup = run(str(ROOT / 'scripts/backup/backup-postgres.sh'), capture_output=True).stdout.strip()
    record = {'release': name, 'started_at': datetime.now(timezone.utc).isoformat(),
              'before_sha256': digest(original), 'target_sha256': digest(data), 'backup': backup}
    operation = RELEASES / ('operation-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
    # Save recovery bytes BEFORE the first write; these survive a killed process.
    recovery = operation.with_suffix('.config.yaml')
    recovery.write_bytes(original)
    record.update(status='in_progress', recovery_config=str(recovery))
    operation.write_text(json.dumps(record, indent=2) + '\n')
    try:
        write_config(state['config_path'], data)
        run('docker', 'restart', state['gateway'], stdout=subprocess.DEVNULL)
        verify(state, data)
        if runtime() != state:
            raise ValueError('Container identity changed during release')
        record['status'] = 'passed'
    except BaseException:
        record['status'] = 'failed'
        try:
            write_config(state['config_path'], original)
            run('docker', 'restart', state['gateway'], stdout=subprocess.DEVNULL)
            verify(state, original)
            record['recovery'] = 'passed'
        except BaseException:
            record['recovery'] = 'failed; use saved recovery config and backup'
        raise
    finally:
        operation.write_text(json.dumps(record, indent=2) + '\n')
    print(f'Release verification: PASS ({name}); same container IDs/images')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    capture_parser = sub.add_parser('capture')
    capture_parser.add_argument('name')
    capture_parser.add_argument('--config')
    for command in ('deploy', 'rollback'):
        sub.add_parser(command).add_argument('name')
    args = parser.parse_args()
    os.umask(0o077)
    RELEASES.mkdir(mode=0o700, exist_ok=True)
    with (RELEASES / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.command == 'capture':
            capture(args.name, args.config)
        else:
            apply_release(args.name)


if __name__ == '__main__':
    main()
```

## llm-gateway-infra/scripts/ci/test-operations.py

[Source aktif](../../llm-gateway-infra/scripts/ci/test-operations.py) · SHA256 `f074363184c6542cc084155f7e83e608face36e390955f0d48db3a77741e25b2`

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

## llm-gateway-e2e/tests/test_models.py

[Source aktif](../../llm-gateway-e2e/tests/test_models.py) · SHA256 `1a009528145be3ebc6c5b83ae785d6c57655801a49c509ee6e5b7673012825c9`

```python
def test_user_can_see_expected_models(
    user_client,
    fast_model,
    coding_model,
):
    response = user_client.get(
        "/v1/models"
    )

    assert response.status_code == 200

    data = response.json()

    model_ids = {
        model["id"]
        for model in data["data"]
    }

    assert model_ids == {fast_model, coding_model}
    assert len(data["data"]) == len(model_ids), "Duplicate logical models exposed"
```

## llm-gateway-e2e/tests/unit/test_model_contract.py

[Source aktif](../../llm-gateway-e2e/tests/unit/test_model_contract.py) · SHA256 `f51d19e018f3c7aade9a682870f79ee52ab753cdf9e1c055a40909b76c078038`

```python
"""Offline checks of the same assertion used by the live /v1/models test."""
from types import SimpleNamespace

import pytest

from tests.test_models import test_user_can_see_expected_models as check_exposed_models


@pytest.mark.unit
@pytest.mark.parametrize("ids", [
    ["company-fast", "company-coding"],
    ["company-coding", "company-fast"],
])
def test_exact_model_exposure_accepts_both_approved_aliases(ids):
    response = SimpleNamespace(status_code=200, json=lambda: {"data": [{"id": name} for name in ids]})
    client = SimpleNamespace(get=lambda _path: response)
    check_exposed_models(client, "company-fast", "company-coding")


@pytest.mark.unit
@pytest.mark.parametrize("ids", [
    ["company-fast"],
    ["company-fast", "company-coding", "extra"],
    ["company-fast", "company-coding", "company-fast"],
    ["company-fast", "openai/gpt-5.6-sol"],
    [],
])
def test_exact_model_exposure_rejects_incomplete_or_extra_aliases(ids):
    response = SimpleNamespace(status_code=200, json=lambda: {"data": [{"id": name} for name in ids]})
    client = SimpleNamespace(get=lambda _path: response)
    with pytest.raises(AssertionError):
        check_exposed_models(client, "company-fast", "company-coding")
```
