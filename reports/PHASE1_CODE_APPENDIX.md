> **Laporan historis:** hasil dan potongan source mengikuti sesi yang tercantum, bukan status current setelah migrasi.
> Baca [master aktif](../MASTER_CONTEXT.md) dan [Phase1](../architecture/phase-1.md); path pada blok kode/log bisa merupakan path lama.
> Tautan navigasi disesuaikan saat migrasi; hasil tes dan isi blok kode tidak diubah.

# Lampiran kode Phase 1 — H1 sampai H10D

Kode berikut adalah snapshot source lokal sesudah perbaikan. Secret runtime, backup, release manifest dan file ignored tidak disertakan. Belum commit/push.

Laporan penjelasan: [PHASE1_H1_H10_REPORT.md](PHASE1_H1_H10_REPORT.md).

## llm-gateway-infra/.env.example

Source: [.env.example](../../llm-gateway-infra/.env.example) — SHA256 `c28338adc30eca517bd90b1d4906632d4533729efb7d2446c00f2bd531420b7a`

```text
# =========================
# LiteLLM
# =========================

LITELLM_BASE_URL=http://localhost:4000

LITELLM_MASTER_KEY=
LITELLM_SALT_KEY=

# =========================
# PostgreSQL
# =========================

POSTGRES_DB=litellm
POSTGRES_USER=litellm
POSTGRES_PASSWORD=

DATABASE_URL=

# =========================
# Redis
# =========================

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# =========================
# Providers - later
#
# OpenAI
# =========================

OPENAI_API_KEY=

# =========================
# Gateway Config Repository
# =========================

LLM_GATEWAY_CONFIG_DIR=../llm-gateway-config
LITELLM_CONFIG_PATH=../llm-gateway-config/config/litellm_config.yaml

# =========================
# Healthcheck API Key
# =========================

HEALTHCHECK_API_KEY=
```

## llm-gateway-infra/.github/workflows/validate.yml

Source: [.github/workflows/validate.yml](../../llm-gateway-infra/.github/workflows/validate.yml) — SHA256 `a9512f3f8ff772277129eaae411d480d3b09d6463837d489ab6e78e5a49e2f8e`

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
        run: python -m pip install -r scripts/requirements.txt

      - name: Validate infrastructure
        run: |
          ./scripts/ci/validate.sh
```

## llm-gateway-infra/.gitignore

Source: [.gitignore](../../llm-gateway-infra/.gitignore) — SHA256 `c1b6f65a3342af755840b7f9675fcc3528b8f99746579c2543a453b3778a7703`

```text
# Secrets
.env
.env.*
!.env.example

secrets/
/staging/
/releases/
*.pem
*.key
*.p12
*.pfx

# Database backups
backups/
*.dump
*.sql

# Python
.venv/
__pycache__/
.pytest_cache/
*.pyc

# Logs
*.log

# IDE / OS
.DS_Store
.idea/
.vscode/
```

## llm-gateway-infra/docker-compose.yml

Source: [docker-compose.yml](../../llm-gateway-infra/docker-compose.yml) — SHA256 `2b7d094048fec04c515126b1191af56f8354e23b925dbabce99bd69633fa8e4b`

```yaml
networks:
  llm-backend:
    driver: bridge

services:
  postgres:
    image: postgres:16.15
    container_name: llm-gateway-postgres
    
    networks:
      - llm-backend

    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

    expose:
      - "5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"
        ]
      interval: 5s
      timeout: 5s
      retries: 10

    restart: unless-stopped


  redis:
    image: redis:7.4.11-alpine
    container_name: llm-gateway-redis
    
    networks:
      - llm-backend

    expose:
      - "6379"

    volumes:
      - redis_data:/data

    healthcheck:
      test:
        [
          "CMD",
          "redis-cli",
          "ping"
        ]
      interval: 5s
      timeout: 3s
      retries: 10

    restart: unless-stopped


  litellm:
    image: ghcr.io/berriai/litellm:1.104.0
    container_name: llm-gateway
    
    networks:
      - llm-backend

    ports:
      - "4000:4000"

    env_file:
      - .env

    volumes:
      - type: bind
        source: ${LITELLM_CONFIG_PATH:-../llm-gateway-config/config/litellm_config.yaml}
        target: /app/config.yaml
        read_only: true
        bind:
          create_host_path: false

    command:
      - "--config"
      - "/app/config.yaml"
      - "--port"
      - "4000"

    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

    restart: unless-stopped


volumes:
  postgres_data:
  redis_data:
```

## llm-gateway-infra/scripts/backup/backup-postgres.sh

Source: [scripts/backup/backup-postgres.sh](../../llm-gateway-infra/scripts/backup/backup-postgres.sh) — SHA256 `cf922c138b1a565cd5a541566e439312379cfb59e8342c04477afcf386c87dff`

```bash
#!/usr/bin/env bash
set -euo pipefail
umask 077
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
required_env POSTGRES_DB
required_env POSTGRES_USER
BACKUP_DIR="${BACKUP_DIR:-$REPO_ROOT/backups}"
mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"
BACKUP_FILE="$(mktemp "$BACKUP_DIR/litellm-$(date -u +%Y%m%dT%H%M%SZ)-XXXXXXXX")"
export BACKUP_FILE
complete=false
cleanup() {
  if [ "$complete" != true ]; then
    rm -f "$BACKUP_FILE" "$BACKUP_FILE.json" "$BACKUP_FILE.env"
  fi
}
trap cleanup EXIT

docker exec "$POSTGRES_CONTAINER" pg_dump \
  -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc --no-owner --no-acl > "$BACKUP_FILE"
if [ ! -s "$BACKUP_FILE" ]; then
  echo "ERROR: empty database backup" >&2
  exit 1
fi
# Preserve the salt and environment required to recover encrypted database data.
cp "$ENV_FILE" "$BACKUP_FILE.env"
chmod 600 "$BACKUP_FILE" "$BACKUP_FILE.env"
python3 - "$BACKUP_FILE" "$POSTGRES_DB" "$POSTGRES_CONTAINER" <<'PYCODE'
from datetime import datetime, timezone
import hashlib, json, sys
from pathlib import Path
p = Path(sys.argv[1])
metadata = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "database": sys.argv[2], "container": sys.argv[3],
    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    "environment_sha256": hashlib.sha256(Path(str(p) + ".env").read_bytes()).hexdigest(),
}
Path(str(p) + ".json").write_text(json.dumps(metadata, indent=2) + "\n")
PYCODE
complete=true
echo "Backup completed (dump + checksum + protected environment)." >&2
printf '%s\n' "$BACKUP_FILE"
```

## llm-gateway-infra/scripts/backup/check-restore.sh

Source: [scripts/backup/check-restore.sh](../../llm-gateway-infra/scripts/backup/check-restore.sh) — SHA256 `a7b2a6b2936d2b1c66f430204baf18ea85c5f9e2157ff3fbc849fa1947e3cf67`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/restore-target.sh"
COUNT="$(docker exec "$POSTGRES_CONTAINER" psql -X -v ON_ERROR_STOP=1 \
  -U "$POSTGRES_USER" -d "$RESTORE_DB" -tAc \
  "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public'")"
if [ "$COUNT" -eq 0 ]; then
  echo "ERROR: restored database has no public tables" >&2
  exit 1
fi
echo "Restore verification: PASS ($COUNT public tables)"
```

## llm-gateway-infra/scripts/backup/drill.sh

Source: [scripts/backup/drill.sh](../../llm-gateway-infra/scripts/backup/drill.sh) — SHA256 `480b0bf3c0a2db37c68146234cb857bac9989bb464df258aab3ca3daf447221e`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/restore-target.sh"
if [ "${1:-}" != "--quiesce" ] || [ "$#" -ne 1 ]; then
  echo "Usage: $0 --quiesce (briefly stops the existing gateway; no new container)" >&2
  exit 1
fi
TEMP_DIR="$(mktemp -d)"
restart_needed=false
cleanup() {
  if [ "$restart_needed" = true ]; then
    docker start "$GATEWAY_CONTAINER" >/dev/null
  fi
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT
if [ "$(docker inspect -f '{{.State.Running}}' "$GATEWAY_CONTAINER")" != true ]; then
  echo "ERROR: gateway must be running before the drill" >&2
  exit 1
fi
# Stop only the existing gateway so no test/inference writes race the comparison.
restart_needed=true
docker stop --time 30 "$GATEWAY_CONTAINER" >/dev/null
BACKUP_FILE="$("$SCRIPT_DIR/backup-postgres.sh")"
python3 "$SCRIPT_DIR/fingerprint.py" "$POSTGRES_CONTAINER" "$POSTGRES_USER" "$POSTGRES_DB" > "$TEMP_DIR/before.json"
"$SCRIPT_DIR/restore-postgres-test.sh" "$BACKUP_FILE"
"$SCRIPT_DIR/check-restore.sh"
python3 "$SCRIPT_DIR/fingerprint.py" "$POSTGRES_CONTAINER" "$POSTGRES_USER" "$RESTORE_DB" > "$TEMP_DIR/after.json"
python3 - "$TEMP_DIR/before.json" "$TEMP_DIR/after.json" <<'PYCODE'
import json, sys
a, b = [json.load(open(p)) for p in sys.argv[1:]]
if not a or a != b:
    sys.exit("ERROR: restored row counts/data fingerprints differ from source")
print(f"Restore data comparison: PASS ({len(a)} tables; counts and fingerprints identical)")
PYCODE
docker start "$GATEWAY_CONTAINER" >/dev/null
restart_needed=false
echo "BACKUP / RESTORE DRILL: PASS"
echo "Backup: $BACKUP_FILE"
```

## llm-gateway-infra/scripts/backup/fingerprint.py

Source: [scripts/backup/fingerprint.py](../../llm-gateway-infra/scripts/backup/fingerprint.py) — SHA256 `1bd4ff4936896c9274fd78b2404e24d0e7993e6628f2bfaa4400d02400487074`

```python
#!/usr/bin/env python3
"""Compare database data without emitting rows, keys, or spend details."""
import json
import subprocess
import sys

container, user, database = sys.argv[1:]

def query(sql):
    return subprocess.check_output(
        ["docker", "exec", container, "psql", "-X", "-v", "ON_ERROR_STOP=1",
         "-U", user, "-d", database, "-tAc", sql], text=True,
    ).strip()

tables = json.loads(query("SELECT coalesce(json_agg(tablename ORDER BY tablename),'[]') FROM pg_tables WHERE schemaname='public'"))
result = {}
for table in tables:
    quoted = '"' + table.replace('"', '""') + '"'
    result[table] = query(
        "SELECT count(*)::text || ':' || md5(coalesce(string_agg(row_to_json(t)::text, E'\\n' ORDER BY row_to_json(t)::text), '')) "
        f"FROM public.{quoted} t"
    )
print(json.dumps(result, sort_keys=True))
```

## llm-gateway-infra/scripts/backup/restore-postgres-test.sh

Source: [scripts/backup/restore-postgres-test.sh](../../llm-gateway-infra/scripts/backup/restore-postgres-test.sh) — SHA256 `64687492d4c4aec7a8e859480627f093aa39fcb4174ed7c3fbec9fcc90e4b65e`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/restore-target.sh"
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <backup.dump>" >&2
  exit 1
fi
"$SCRIPT_DIR/verify-backup.sh" "$1"
# Check the backup's identity before touching the dedicated test database.
python3 - "$1.json" "$POSTGRES_DB" <<'PYCODE'
import json, sys
if json.load(open(sys.argv[1]))["database"] != sys.argv[2]:
    sys.exit("ERROR: backup belongs to a different source database")
PYCODE
docker exec "$POSTGRES_CONTAINER" dropdb -U "$POSTGRES_USER" --if-exists "$RESTORE_DB"
docker exec "$POSTGRES_CONTAINER" createdb -U "$POSTGRES_USER" "$RESTORE_DB"
docker exec -i "$POSTGRES_CONTAINER" pg_restore \
  -U "$POSTGRES_USER" -d "$RESTORE_DB" --exit-on-error --no-owner --no-acl < "$1"
echo "Restore completed into dedicated test database: $RESTORE_DB"
```

## llm-gateway-infra/scripts/backup/restore-postgres.sh

Source: [scripts/backup/restore-postgres.sh](../../llm-gateway-infra/scripts/backup/restore-postgres.sh) — SHA256 `f400aa44c427f6c636aabb4ac440cd6ab39f3cfe538fc8886d4d8c3e3c91d497`

```bash
#!/usr/bin/env bash
# Compatibility entrypoint: this script restores ONLY the dedicated test DB.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/restore-postgres-test.sh" "$@"
```

## llm-gateway-infra/scripts/backup/verify-backup.sh

Source: [scripts/backup/verify-backup.sh](../../llm-gateway-infra/scripts/backup/verify-backup.sh) — SHA256 `0dbc5a6458afdf667a9df556654a7c94c01e3eaec566d8d5d0f23e2c626187ec`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
if [ "$#" -ne 1 ] || [ ! -s "$1" ]; then
  echo "Usage: $0 <non-empty-backup.dump>" >&2
  exit 1
fi
python3 - "$1" <<'PYCODE'
import hashlib, json, sys
from pathlib import Path
p = Path(sys.argv[1])
try:
    data = json.loads(Path(str(p) + ".json").read_text())
    for file, field in ((p, "sha256"), (Path(str(p) + ".env"), "environment_sha256")):
        if hashlib.sha256(file.read_bytes()).hexdigest() != data[field]:
            sys.exit("ERROR: backup checksum mismatch")
except (OSError, ValueError, KeyError):
    sys.exit("ERROR: backup metadata or protected environment is missing/invalid")
print("Backup checksums: PASS")
PYCODE
docker exec -i "$POSTGRES_CONTAINER" pg_restore --list < "$1" > /dev/null
echo "Backup archive readable: PASS"
```

## llm-gateway-infra/scripts/ci/test-operations.py

Source: [scripts/ci/test-operations.py](../../llm-gateway-infra/scripts/ci/test-operations.py) — SHA256 `c88ff5568af5cd1193d1f407f2062fa72619133c614c969fc54b4dafd8c1ad23`

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

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('release_manager', ROOT / 'scripts/release/manage.py')
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)
CONFIG = b'''model_list:
- model_name: company-fast
  litellm_params: {api_key: os.environ/OPENAI_API_KEY}
- model_name: company-coding
  litellm_params: {api_key: os.environ/OPENAI_API_KEY}
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

## llm-gateway-infra/scripts/ci/validate-compose.py

Source: [scripts/ci/validate-compose.py](../../llm-gateway-infra/scripts/ci/validate-compose.py) — SHA256 `b2fa0778022465925f23aa1071ba90a8f29585dde5f7787044147379a32780c6`

```python
#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    sys.exit(1)


if len(sys.argv) != 3:
    fail(
        "Usage: "
        "validate-compose.py "
        "<base|dev> <compose-json|->"
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


if (
    config_mount.get("type") != "bind"
    or config_mount.get("bind", {}).get("create_host_path") is not False
):
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

## llm-gateway-infra/scripts/ci/validate.sh

Source: [scripts/ci/validate.sh](../../llm-gateway-infra/scripts/ci/validate.sh) — SHA256 `3eb5ceec4b5572b6bb9d133ef5f7870c6ed5bd8e1efad3ff1b979811b1105e28`

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

## llm-gateway-infra/scripts/health/dependencies.sh

Source: [scripts/health/dependencies.sh](../../llm-gateway-infra/scripts/health/dependencies.sh) — SHA256 `1f321ff68ade931b4829d65fea6d6fd2db7aa0230b4e09a95a145a540317585b`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/../lib/common.sh"

required_env POSTGRES_USER
required_env POSTGRES_DB

echo "======================================"
echo "Dependency Health"
echo "======================================"

echo
echo "[1/2] PostgreSQL"

docker exec \
    "$POSTGRES_CONTAINER" \
    pg_isready \
        -U "$POSTGRES_USER" \
        -d "$POSTGRES_DB"

echo "PostgreSQL: OK"


echo
echo "[2/2] Redis"

REDIS_RESULT="$(
    docker exec \
        "$REDIS_CONTAINER" \
        redis-cli ping
)"

if [ "$REDIS_RESULT" != "PONG" ]; then
    echo "Redis: FAILED"
    exit 1
fi

echo "Redis: OK"

echo
echo "All dependencies: OK"
```

## llm-gateway-infra/scripts/health/functional.sh

Source: [scripts/health/functional.sh](../../llm-gateway-infra/scripts/health/functional.sh) — SHA256 `a2a55e07d4eb914c526bcab85e5030019e851b227d5c39921900b1714f3111da`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/../lib/common.sh"

required_env HEALTHCHECK_API_KEY

echo "Checking authenticated model catalog..."

RESPONSE="$(
    curl \
        --fail \
        --connect-timeout 5 \
        --max-time 15 \
        --silent \
        --show-error \
        "${LITELLM_BASE_URL}/v1/models" \
        -H "Authorization: Bearer ${HEALTHCHECK_API_KEY}"
)"

python3 - "$RESPONSE" <<'PY'
import json
import sys

data = json.loads(sys.argv[1])

models = {
    item["id"]
    for item in data.get("data", [])
}

required = {
    "company-fast",
    "company-coding",
}

missing = required - models

if missing:
    print(
        "Functional health FAILED. "
        f"Missing models: {sorted(missing)}",
        file=sys.stderr,
    )
    sys.exit(1)

print("Functional health: OK")
print("Available required models:")
for model in sorted(required):
    print(f"  - {model}")
PY
```

## llm-gateway-infra/scripts/health/liveness.sh

Source: [scripts/health/liveness.sh](../../llm-gateway-infra/scripts/health/liveness.sh) — SHA256 `4a78ad3858c472f2d2b8c60330111b23870e5e8163d94e26554c5634970d1612`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/../lib/common.sh"

echo "Checking LiteLLM liveness..."

curl \
    --fail \
    --silent \
    --show-error \
    --connect-timeout 5 \
    --max-time 10 \
    "${LITELLM_BASE_URL}/health/liveliness" \
    >/dev/null

echo "LiteLLM liveness: OK"
```

## llm-gateway-infra/scripts/health/readiness.sh

Source: [scripts/health/readiness.sh](../../llm-gateway-infra/scripts/health/readiness.sh) — SHA256 `7bb8d073f2749444d2904d0cf2b7a0183722a4253daa6809cb7c6016fe3efd3a`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/../lib/common.sh"

echo "Checking LiteLLM readiness..."

curl \
    --fail \
    --silent \
    --show-error \
    --connect-timeout 5 \
    --max-time 10 \
    "${LITELLM_BASE_URL}/health/readiness" \
    >/dev/null

# HTTP readiness may return a cached 200 while a dependency is down.
"$SCRIPT_DIR/dependencies.sh" >/dev/null
echo "LiteLLM readiness (HTTP + dependencies): OK"
```

## llm-gateway-infra/scripts/lib/common.sh

Source: [scripts/lib/common.sh](../../llm-gateway-infra/scripts/lib/common.sh) — SHA256 `c0d674fe2f838013748acb4a507aaf841aa675f996fda0d64f000b136301b82a`

```bash
#!/usr/bin/env bash

set -euo pipefail

COMMON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$COMMON_DIR/../.." && pwd)"

ENV_FILE="${LLM_GATEWAY_ENV_FILE:-$REPO_ROOT/.env}"

if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: .env not found at:"
    echo "$ENV_FILE"
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-llm-gateway-postgres}"
REDIS_CONTAINER="${REDIS_CONTAINER:-llm-gateway-redis}"
GATEWAY_CONTAINER="${GATEWAY_CONTAINER:-llm-gateway}"
export POSTGRES_CONTAINER REDIS_CONTAINER GATEWAY_CONTAINER


required_env() {
    local name="$1"

    if [ -z "${!name:-}" ]; then
        echo "ERROR: required environment variable '$name' is missing."
        exit 1
    fi
}


required_env LITELLM_BASE_URL
required_env LITELLM_MASTER_KEY


CONFIG_DIR_RAW="${LLM_GATEWAY_CONFIG_DIR:-../llm-gateway-config}"

if [[ "$CONFIG_DIR_RAW" = /* ]]; then
    LLM_GATEWAY_CONFIG_DIR="$CONFIG_DIR_RAW"
else
    LLM_GATEWAY_CONFIG_DIR="$REPO_ROOT/$CONFIG_DIR_RAW"
fi

if [ ! -d "$LLM_GATEWAY_CONFIG_DIR" ]; then
    echo "ERROR: config repository not found:"
    echo "$LLM_GATEWAY_CONFIG_DIR"
    exit 1
fi


litellm_admin_request() {
    local method="$1"
    local path="$2"
    local body="${3:-}"

    if [ -n "$body" ]; then
        curl --fail-with-body -sS --connect-timeout 5 --max-time 60 \
        -X "$method" \
        "${LITELLM_BASE_URL}${path}" \
        -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
        -H "Content-Type: application/json" \
        -d "$body"
    else
        curl --fail-with-body -sS --connect-timeout 5 --max-time 60 \
        -X "$method" \
        "${LITELLM_BASE_URL}${path}" \
        -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"
    fi
}
```

## llm-gateway-infra/scripts/lib/restore-target.sh

Source: [scripts/lib/restore-target.sh](../../llm-gateway-infra/scripts/lib/restore-target.sh) — SHA256 `2f236b25e1bc983160b441e7b445563acf623c056190921c94746357fe29d193`

```bash
#!/usr/bin/env bash
# Source after common.sh. Never allow the active database as a restore-test target.
required_env POSTGRES_DB
required_env POSTGRES_USER
RESTORE_DB="${RESTORE_DB:-${POSTGRES_DB}_restore_test}"
if [ "${#RESTORE_DB}" -gt 63 ] || \
   [[ ! "$RESTORE_DB" =~ ^[a-zA-Z0-9_]+$ ]] || \
   [ "$RESTORE_DB" != "${POSTGRES_DB}_restore_test" ] || \
   [ "$RESTORE_DB" = "$POSTGRES_DB" ]; then
  echo "ERROR: restore target must be the dedicated <POSTGRES_DB>_restore_test database." >&2
  exit 1
fi
export RESTORE_DB
```

## llm-gateway-infra/scripts/onboard-developer.sh

Source: [scripts/onboard-developer.sh](../../llm-gateway-infra/scripts/onboard-developer.sh) — SHA256 `2161e59d87ba26ca5c92389336b2ef8b50255d8d7a1c77df0f6f063fbdec1f85`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -ne 3 ]; then
    echo "Usage:"
    echo "  $0 <user-id> <team-id> <team-policy-name>"
    exit 1
fi

USER_ID="$1"
TEAM_ID="$2"
POLICY_NAME="$3"

KEY_ALIAS="$(
python3 - "$USER_ID" <<'PY'
import re
import sys

value = sys.argv[1].lower()
value = re.sub(r'[^a-z0-9]+', '-', value)
value = value.strip('-')

print(f"{value}-opencode")
PY
)"

echo "======================================"
echo "Developer onboarding"
echo "======================================"
echo
echo "User:"
echo "  $USER_ID"
echo
echo "Team:"
echo "  $TEAM_ID"
echo

"$SCRIPT_DIR/users/create-user.sh" \
    "$USER_ID"

echo
echo "Adding user to team..."
echo

"$SCRIPT_DIR/teams/add-member.sh" \
    "$TEAM_ID" \
    "$USER_ID" \
    "$POLICY_NAME"

echo
echo "Creating developer key..."
echo

"$SCRIPT_DIR/keys/create-key.sh" \
    "$USER_ID" \
    "$TEAM_ID" \
    "$KEY_ALIAS"
```

## llm-gateway-infra/scripts/release/manage.py

Source: [scripts/release/manage.py](../../llm-gateway-infra/scripts/release/manage.py) — SHA256 `88cd68228c47ab394028c89ad8e4ff80d97ab7790f8c7863852363ef1c125ecd`

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
    config = yaml.safe_load(data)
    if not isinstance(config, dict):
        raise ValueError('Config must be a mapping')
    models = config.get('model_list', [])
    if {m['model_name'] for m in models} != {'company-fast', 'company-coding'}:
        raise ValueError('Required logical aliases must be preserved')
    for model in models:
        key = model['litellm_params'].get('api_key', '')
        if not key.startswith('os.environ/'):
            raise ValueError('Provider key must reference an environment variable')
    general = config.get('general_settings', {})
    for key in ('master_key', 'database_url'):
        if not str(general.get(key, '')).startswith('os.environ/'):
            raise ValueError(f'{key} must reference an environment variable')


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

## llm-gateway-infra/scripts/release/release.sh

Source: [scripts/release/release.sh](../../llm-gateway-infra/scripts/release/release.sh) — SHA256 `27045814d1be748a9b0f51c2d012595951f6ad6423f041ee02ae5ebea61c7216`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
export REPO_ROOT LLM_GATEWAY_CONFIG_DIR ENV_FILE
exec python3 "$SCRIPT_DIR/manage.py" "$@"
```

## llm-gateway-infra/scripts/security/audit-python.sh

Source: [scripts/security/audit-python.sh](../../llm-gateway-infra/scripts/security/audit-python.sh) — SHA256 `3f30152fc3182b923e047b2f11fa72be5e8ed607626f57376da6008832c4e0d2`

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

if [ "$#" -ne 1 ]; then
  echo "Usage:"
  echo "  $0 <requirements-file>"
  exit 1
fi

REQUIREMENTS_FILE="$1"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "ERROR: requirements file not found:"
  echo "$REQUIREMENTS_FILE"
  exit 1
fi

# Reuse an installed auditor when available; CI retains isolated-tool fallback.
if [ -n "${PIP_AUDIT_BIN:-}" ]; then
  "$PIP_AUDIT_BIN" -r "$REQUIREMENTS_FILE"
  exit 0
fi

PIP_AUDIT_VERSION="${PIP_AUDIT_VERSION:-2.10.1}"

TEMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

echo
echo "======================================"
echo "Python Dependency Audit"
echo "======================================"

echo
echo "Requirements:"
echo "  $REQUIREMENTS_FILE"

echo
echo "pip-audit:"
echo "  $PIP_AUDIT_VERSION"

python3 \
  -m venv \
  "$TEMP_DIR/venv"

"$TEMP_DIR/venv/bin/python" \
  -m pip \
  install \
  --quiet \
  --upgrade pip

"$TEMP_DIR/venv/bin/python" \
  -m pip \
  install \
  --quiet \
  "pip-audit==$PIP_AUDIT_VERSION"

"$TEMP_DIR/venv/bin/pip-audit" \
  -r "$REQUIREMENTS_FILE"

echo
echo "======================================"
echo "PYTHON DEPENDENCY AUDIT: PASSED"
echo "======================================"
```

## llm-gateway-infra/scripts/security/scan-containers.sh

Source: [scripts/security/scan-containers.sh](../../llm-gateway-infra/scripts/security/scan-containers.sh) — SHA256 `b6dce88d908dd63bd832cf8e3754e7b5cd5be41f49f638d24a7a9743ba20e5ba`

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

TRIVY_IMAGE="${TRIVY_IMAGE:-aquasec/trivy:0.74.0}"
REPORT_ONLY="${REPORT_ONLY:-0}"

trivy_run() {
  if [ -n "${TRIVY_BIN:-}" ]; then
    "$TRIVY_BIN" "$@"
  else
    docker run --rm --volume trivy-cache:/root/.cache/ "$TRIVY_IMAGE" "$@"
  fi
}

BASELINE_FILE="$SCRIPT_DIR/container-high-baseline.json"

TEMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TEMP_DIR"
}

trap cleanup EXIT


echo
echo "======================================"
echo "Container Vulnerability Scan"
echo "======================================"

echo
echo "Scanner:"
echo "  $TRIVY_IMAGE"

echo
echo "Policy:"
echo "  CRITICAL/HIGH fixable: reviewed per-image baseline"
echo "  Baselines are never increased automatically"

if [ "$REPORT_ONLY" = "1" ]; then
  echo
  echo "Mode:"
  echo "  REPORT ONLY"
fi


#
# --------------------------------------------------
# Preflight
# --------------------------------------------------
#

echo
echo "[1/4] Preflight"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is required."
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required."
  exit 1
fi

if [ "$REPORT_ONLY" != "1" ] && \
   [ ! -f "$BASELINE_FILE" ]; then
  echo "ERROR: baseline file not found:"
  echo "  $BASELINE_FILE"
  exit 1
fi

echo "Preflight: PASS"


#
# --------------------------------------------------
# Scanner availability
# --------------------------------------------------
#

echo
echo "[2/4] Scanner availability"

trivy_run version

echo "Scanner availability: PASS"


#
# --------------------------------------------------
# Resolve images
# --------------------------------------------------
#

echo
echo "[3/4] Resolve runtime images"

IMAGES="$(
  docker compose \
    config \
    --images \
    | sort \
    -u
)"

if [ -z "$IMAGES" ]; then
  echo "ERROR: no container images found."
  exit 1
fi

echo
echo "Runtime images:"

while IFS= read -r image; do
  if [ -n "$image" ]; then
    echo "  - $image"
  fi
done <<< "$IMAGES"


#
# --------------------------------------------------
# Scan
# --------------------------------------------------
#

echo
echo "[4/4] Vulnerability policy evaluation"

SCAN_FAILED=0


while IFS= read -r image; do

  if [ -z "$image" ]; then
    continue
  fi

  SAFE_NAME="$(
    printf '%s' "$image" \
      | tr '/:' '__'
  )"

  REPORT_FILE="$TEMP_DIR/$SAFE_NAME.json"

  echo
  echo "======================================"
  echo "Scanning:"
  echo "  $image"
  echo "======================================"

  #
  # Trivy itself does NOT make the policy
  # decision here.
  #
  # We only request fixable HIGH/CRITICAL
  # findings and evaluate them below.
  #

  if ! trivy_run image \
      --no-progress \
      --skip-version-check \
      --scanners vuln \
      --severity HIGH,CRITICAL \
      --ignore-unfixed \
      --format json \
      "$image" \
      > "$REPORT_FILE"
  then
    echo
    echo "ERROR: Trivy failed to scan:"
    echo "  $image"

    SCAN_FAILED=1
    continue
  fi


  #
  # Count unique findings.
  #
  # A finding is uniquely identified using:
  #
  # target
  # vulnerability ID
  # package
  # installed version
  #

  CRITICAL_COUNT="$(
    jq '
      [
        .Results[]? as $result
        |
        $result.Vulnerabilities[]?
        |
        select(.Severity == "CRITICAL")
        |
        (
          ($result.Target // "")
          + "|"
          + (.VulnerabilityID // "")
          + "|"
          + (.PkgName // "")
          + "|"
          + (.InstalledVersion // "")
        )
      ]
      | unique
      | length
    ' "$REPORT_FILE"
  )"


  HIGH_COUNT="$(
    jq '
      [
        .Results[]? as $result
        |
        $result.Vulnerabilities[]?
        |
        select(.Severity == "HIGH")
        |
        (
          ($result.Target // "")
          + "|"
          + (.VulnerabilityID // "")
          + "|"
          + (.PkgName // "")
          + "|"
          + (.InstalledVersion // "")
        )
      ]
      | unique
      | length
    ' "$REPORT_FILE"
  )"


  echo
  echo "Results:"
  echo "  CRITICAL: $CRITICAL_COUNT"
  echo "  HIGH:     $HIGH_COUNT"


  #
  # Report-only mode is used to establish
  # the initial approved baseline.
  #

  if [ "$REPORT_ONLY" = "1" ]; then
    echo
    echo "Suggested baseline entry:"
    printf '  "%s": %s\n' \
      "$image" \
      "$HIGH_COUNT"

    if [ "$CRITICAL_COUNT" -gt 0 ]; then
      echo
      echo "WARNING:"
      echo "  $CRITICAL_COUNT fixable CRITICAL finding(s)"
      echo "  were detected."
      echo
      echo "  CRITICAL findings must NOT be added"
      echo "  to the approved baseline."
    fi

    continue
  fi


  #
  # Every image must have an explicitly
  # approved HIGH baseline.
  #

  if ! jq \
    --exit-status \
    --arg image "$image" \
    'has($image)' \
    "$BASELINE_FILE" \
    >/dev/null
  then
    echo
    echo "ERROR: image has no approved baseline:"
    echo "  $image"
    echo
    echo "Run:"
    echo
    echo "Suggested baseline entry:"
    echo "\"$image\": {"
    echo "  \"critical\": $CRITICAL_COUNT,"
    echo "  \"high\": $HIGH_COUNT"
    echo "}"

    SCAN_FAILED=1
    continue
  fi


  MAX_CRITICAL="$(
    jq \
      --raw-output \
      --arg image "$image" \
      '.[$image].critical' \
      "$BASELINE_FILE"
  )"

  MAX_HIGH="$(
    jq \
      --raw-output \
      --arg image "$image" \
      '.[$image].high' \
      "$BASELINE_FILE"
  )"


  if ! [[ "$MAX_CRITICAL" =~ ^[0-9]+$ ]]; then
    echo
    echo "ERROR: invalid CRITICAL baseline for:"
    echo "  $image"
    echo "Value:"
    echo "  $MAX_CRITICAL"

    SCAN_FAILED=1
    continue
  fi

  if ! [[ "$MAX_HIGH" =~ ^[0-9]+$ ]]; then
    echo
    echo "ERROR: invalid HIGH baseline for:"
    echo "  $image"
    echo "Value:"
    echo "  $MAX_HIGH"

    SCAN_FAILED=1
    continue
  fi


  echo
  echo "Approved policy:"
  echo "  CRITICAL <= $MAX_CRITICAL"
  echo "  HIGH     <= $MAX_HIGH"


  IMAGE_FAILED=0


  #
  # CRITICAL tolerance is explicitly scoped to each reviewed image.
  #

  if [ "$CRITICAL_COUNT" -gt "$MAX_CRITICAL" ]; then
    echo
    echo "ERROR:"
    echo "  CRITICAL vulnerability baseline exceeded."
    echo
    echo "Approved:"
    echo "  $MAX_CRITICAL"
    echo
    echo "Current:"
    echo "  $CRITICAL_COUNT"

    IMAGE_FAILED=1
  fi


  #
  # HIGH may not exceed the approved
  # per-image baseline.
  #

  if [ "$HIGH_COUNT" -gt "$MAX_HIGH" ]; then
    echo
    echo "ERROR:"
    echo "  HIGH vulnerability baseline exceeded."
    echo
    echo "Approved:"
    echo "  $MAX_HIGH"
    echo
    echo "Current:"
    echo "  $HIGH_COUNT"

    IMAGE_FAILED=1
  fi


  #
  # If security posture improved, CI still
  # passes, but we ask the maintainer to
  # lower the baseline.
  #

  if [ "$CRITICAL_COUNT" -lt "$MAX_CRITICAL" ]; then
    echo
    echo "NOTICE:"
    echo "  CRITICAL vulnerability count improved."
    echo
    echo "Current:"
    echo "  $CRITICAL_COUNT"
    echo
    echo "Approved baseline:"
    echo "  $MAX_CRITICAL"
    echo
    echo "Consider lowering the CRITICAL baseline."
  fi

  if [ "$HIGH_COUNT" -lt "$MAX_HIGH" ]; then
    echo
    echo "NOTICE:"
    echo "  HIGH vulnerability count improved."
    echo
    echo "Current:"
    echo "  $HIGH_COUNT"
    echo
    echo "Approved baseline:"
    echo "  $MAX_HIGH"
    echo
    echo "Consider lowering the HIGH baseline."
  fi


  if [ "$IMAGE_FAILED" -ne 0 ]; then

    echo
    echo "Relevant findings:"
    echo

    jq \
      --raw-output \
      '
        .Results[]? as $result
        |
        $result.Vulnerabilities[]?
        |
        select(
          .Severity == "HIGH"
          or
          .Severity == "CRITICAL"
        )
        |
        [
          .Severity,
          .VulnerabilityID,
          .PkgName,
          .InstalledVersion,
          (.FixedVersion // ""),
          ($result.Target // "")
        ]
        |
        @tsv
      ' \
      "$REPORT_FILE"

    SCAN_FAILED=1

  else

    echo
    echo "Policy evaluation:"
    echo "  PASS"

  fi

done <<< "$IMAGES"


#
# --------------------------------------------------
# Final status
# --------------------------------------------------
#

if [ "$REPORT_ONLY" = "1" ]; then
  echo
  echo "======================================"
  echo "REPORT-ONLY SCAN COMPLETE"
  echo "======================================"
  exit 0
fi


if [ "$SCAN_FAILED" -ne 0 ]; then
  echo
  echo "======================================"
  echo "CONTAINER VULNERABILITY SCAN: FAILED"
  echo "======================================"
  exit 1
fi


echo
echo "======================================"
echo "CONTAINER VULNERABILITY SCAN: PASSED"
echo "======================================"
```

## llm-gateway-infra/scripts/security/scan-secrets.sh

Source: [scripts/security/scan-secrets.sh](../../llm-gateway-infra/scripts/security/scan-secrets.sh) — SHA256 `032cceed19a1b385dd7d4fea7e965c98a59f70da3e82bbc818674d9b52ede7c2`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
GITLEAKS_IMAGE="${GITLEAKS_IMAGE:-ghcr.io/gitleaks/gitleaks:v8.28.0}"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
scanner() {
  if [ -n "${GITLEAKS_BIN:-}" ]; then
    "$GITLEAKS_BIN" "$@"
  else
    docker run --rm --interactive --network=none \
      --volume "$TEMP_DIR:$TEMP_DIR:ro" "$GITLEAKS_IMAGE" "$@"
  fi
}
scanner version
cat > "$TEMP_DIR/canary.toml" <<'CANARY'
title = "LLM Gateway Gitleaks Canary"
[[rules]]
id = "llm-gateway-canary"
regex = '''COMPANY_GITLEAKS_CANARY_[A-Z0-9]{24}'''
CANARY
set +e
printf '%s\n' 'COMPANY_GITLEAKS_CANARY_ABCDEF1234567890ABCDEFGH' \
  | scanner --config="$TEMP_DIR/canary.toml" --redact --exit-code=42 stdin >/dev/null 2>&1
CANARY_STATUS=$?
set -e
if [ "$CANARY_STATUS" -ne 42 ]; then
  echo "ERROR: scanner canary failed ($CANARY_STATUS, expected 42)" >&2
  exit 1
fi
echo "Scanner engine self-test: PASS"
echo "Repository history scan"
git log -p --all --full-history --no-renames | scanner --redact stdin
echo "Current tracked and non-ignored files scan"
# Include uncommitted and new source files, but never ignored .env/backups.
python3 - <<'PYCODE' | scanner --redact stdin
from pathlib import Path
import subprocess, sys
names = subprocess.check_output(['git', 'ls-files', '-c', '-o', '--exclude-standard', '-z']).split(b'\0')
for name in sorted(set(names)):
    if not name:
        continue
    path = Path(name.decode())
    if path.is_file() and not path.is_symlink():
        sys.stdout.buffer.write(b'\nFILE: ' + name + b'\n' + path.read_bytes() + b'\n')
PYCODE
echo "SECRET SCAN: PASSED"
```

## llm-gateway-config/clients/opencode/opencode.jsonc

Source: [clients/opencode/opencode.jsonc](../../llm-gateway-config/clients/opencode/opencode.jsonc) — SHA256 `d0c219008a1d54d5b59ebf5ed4307b38bca1b12c89e81921caae65dbf8308bde`

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

## llm-gateway-config/config/litellm_config.yaml

Source: [config/litellm_config.yaml](../../llm-gateway-config/config/litellm_config.yaml) — SHA256 `5bc327e951ebd02c9f33934e09940c91a66cd2233bb056efeb58f80be2d75a9b`

```yaml
model_list:

  # ==========================================
  # COMPANY FAST
  # ==========================================
  - model_name: company-fast
    litellm_params:
      model: openai/gpt-5.6-terra
      api_key: os.environ/OPENAI_API_KEY
      timeout: 120


  # ==========================================
  # COMPANY CODING
  # ==========================================
  - model_name: company-coding
    litellm_params:
      model: openai/gpt-5.6-sol
      api_key: os.environ/OPENAI_API_KEY
      timeout: 180


# ============================================
# LITELLM
# ============================================
litellm_settings:
  num_retries: 2
  request_timeout: 180

  set_verbose: false
  json_logs: true


# ============================================
# GENERAL
# ============================================
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
```

## llm-gateway-config/policies/teams/engineering.yaml

Source: [policies/teams/engineering.yaml](../../llm-gateway-config/policies/teams/engineering.yaml) — SHA256 `47f4c2f6511a5258f114a9f76b351784446cf3a9f3b762ac547fe5ff23544efc`

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

## llm-gateway-config/scripts/ci/validate-yaml.py

Source: [scripts/ci/validate-yaml.py](../../llm-gateway-config/scripts/ci/validate-yaml.py) — SHA256 `b3a18c160e8d61af2be7ce7355b3cf4a9fbf33defe6f909b79e90fdc02f5f500`

```python
#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

import yaml


ROOT = Path(".")


def fail(message: str) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    sys.exit(1)


yaml_files = sorted(
    list(ROOT.rglob("*.yaml"))
    + list(ROOT.rglob("*.yml"))
)


if not yaml_files:
    fail("no YAML files found")


print(
    f"Found {len(yaml_files)} YAML file(s)"
)


for path in yaml_files:
    if not path.is_file():
        fail(f"expected YAML file, found directory: {path}")
    print(f"Checking: {path}")

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as f:
            yaml.safe_load(f)

    except yaml.YAMLError as exc:
        fail(
            f"invalid YAML in {path}: {exc}"
        )


print("YAML syntax: PASS")
```

## llm-gateway-config/scripts/security/audit-python.sh

Source: [scripts/security/audit-python.sh](../../llm-gateway-config/scripts/security/audit-python.sh) — SHA256 `3f30152fc3182b923e047b2f11fa72be5e8ed607626f57376da6008832c4e0d2`

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

if [ "$#" -ne 1 ]; then
  echo "Usage:"
  echo "  $0 <requirements-file>"
  exit 1
fi

REQUIREMENTS_FILE="$1"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "ERROR: requirements file not found:"
  echo "$REQUIREMENTS_FILE"
  exit 1
fi

# Reuse an installed auditor when available; CI retains isolated-tool fallback.
if [ -n "${PIP_AUDIT_BIN:-}" ]; then
  "$PIP_AUDIT_BIN" -r "$REQUIREMENTS_FILE"
  exit 0
fi

PIP_AUDIT_VERSION="${PIP_AUDIT_VERSION:-2.10.1}"

TEMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

echo
echo "======================================"
echo "Python Dependency Audit"
echo "======================================"

echo
echo "Requirements:"
echo "  $REQUIREMENTS_FILE"

echo
echo "pip-audit:"
echo "  $PIP_AUDIT_VERSION"

python3 \
  -m venv \
  "$TEMP_DIR/venv"

"$TEMP_DIR/venv/bin/python" \
  -m pip \
  install \
  --quiet \
  --upgrade pip

"$TEMP_DIR/venv/bin/python" \
  -m pip \
  install \
  --quiet \
  "pip-audit==$PIP_AUDIT_VERSION"

"$TEMP_DIR/venv/bin/pip-audit" \
  -r "$REQUIREMENTS_FILE"

echo
echo "======================================"
echo "PYTHON DEPENDENCY AUDIT: PASSED"
echo "======================================"
```

## llm-gateway-config/scripts/security/scan-secrets.sh

Source: [scripts/security/scan-secrets.sh](../../llm-gateway-config/scripts/security/scan-secrets.sh) — SHA256 `032cceed19a1b385dd7d4fea7e965c98a59f70da3e82bbc818674d9b52ede7c2`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
GITLEAKS_IMAGE="${GITLEAKS_IMAGE:-ghcr.io/gitleaks/gitleaks:v8.28.0}"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
scanner() {
  if [ -n "${GITLEAKS_BIN:-}" ]; then
    "$GITLEAKS_BIN" "$@"
  else
    docker run --rm --interactive --network=none \
      --volume "$TEMP_DIR:$TEMP_DIR:ro" "$GITLEAKS_IMAGE" "$@"
  fi
}
scanner version
cat > "$TEMP_DIR/canary.toml" <<'CANARY'
title = "LLM Gateway Gitleaks Canary"
[[rules]]
id = "llm-gateway-canary"
regex = '''COMPANY_GITLEAKS_CANARY_[A-Z0-9]{24}'''
CANARY
set +e
printf '%s\n' 'COMPANY_GITLEAKS_CANARY_ABCDEF1234567890ABCDEFGH' \
  | scanner --config="$TEMP_DIR/canary.toml" --redact --exit-code=42 stdin >/dev/null 2>&1
CANARY_STATUS=$?
set -e
if [ "$CANARY_STATUS" -ne 42 ]; then
  echo "ERROR: scanner canary failed ($CANARY_STATUS, expected 42)" >&2
  exit 1
fi
echo "Scanner engine self-test: PASS"
echo "Repository history scan"
git log -p --all --full-history --no-renames | scanner --redact stdin
echo "Current tracked and non-ignored files scan"
# Include uncommitted and new source files, but never ignored .env/backups.
python3 - <<'PYCODE' | scanner --redact stdin
from pathlib import Path
import subprocess, sys
names = subprocess.check_output(['git', 'ls-files', '-c', '-o', '--exclude-standard', '-z']).split(b'\0')
for name in sorted(set(names)):
    if not name:
        continue
    path = Path(name.decode())
    if path.is_file() and not path.is_symlink():
        sys.stdout.buffer.write(b'\nFILE: ' + name + b'\n' + path.read_bytes() + b'\n')
PYCODE
echo "SECRET SCAN: PASSED"
```

## llm-gateway-e2e/.github/workflows/live.yml

Source historis: [.github/workflows/live.yml — snapshot di bawah](#llm-gateway-e2egithubworkflowsliveyml) — SHA256 `836c4bbd99a07e518d1cc6c0502bb3af83ab70292a7dbc3277b42d67e1d919ff`

File aktif dihapus sesuaiO-08 pada17Oktober2026; kode snapshot historis berikut tetap
dipertahankan dan bukan workflow yang harus dihidupkan kembali.

```yaml
name: Live Gateway E2E

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  live:
    name: Live Gateway E2E
    runs-on: ubuntu-latest

    environment:
      staging

    timeout-minutes: 20

    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"

          cache: "pip"
          cache-dependency-path: requirements.txt

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run smoke tests
        env:
          LITELLM_BASE_URL: ${{ secrets.STAGING_LITELLM_BASE_URL }}
          LITELLM_MASTER_KEY: ${{ secrets.STAGING_LITELLM_MASTER_KEY }}
        run: |
          python -m pytest \
            -v \
            -m "not live and not unit"

      - name: Run live tests
        env:
          LITELLM_BASE_URL: ${{ secrets.STAGING_LITELLM_BASE_URL }}
          LITELLM_MASTER_KEY: ${{ secrets.STAGING_LITELLM_MASTER_KEY }}
        run: |
          python -m pytest \
            -v \
            -m "live"
```

## llm-gateway-e2e/pytest.ini

Source: [pytest.ini](../../llm-gateway-e2e/pytest.ini) — SHA256 `3be885723488b7c3e20d0284a219b4d526093e035f716e85ee59c5de3eb54952`

```text
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
```

## llm-gateway-e2e/scripts/ci/validate-suite.py

Source: [scripts/ci/validate-suite.py](../../llm-gateway-e2e/scripts/ci/validate-suite.py) — SHA256 `43417e713a454812eb06ad522e3239f919ab1605b0514b81660ca44e1dda0c0c`

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

## llm-gateway-e2e/scripts/ci/validate.sh

Source: [scripts/ci/validate.sh](../../llm-gateway-e2e/scripts/ci/validate.sh) — SHA256 `033dd3d80518c046ef55786640624f1c5520c531444d0b92382469e3366de5cf`

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
echo "LLM Gateway E2E Validation"
echo "======================================"

echo
echo "[1/8] Bash syntax"

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
echo "[2/8] ShellCheck"

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
echo "[3/8] Python syntax"

python3 \
  -m compileall \
  -q \
  tests \
  scripts/ci

echo "Python syntax: PASS"


echo
echo "[4/8] Python dependency health"

python3 -m pip check

echo "Python dependencies: PASS"


echo
echo "[5/8] Regression suite structure"

python3 \
  scripts/ci/validate-suite.py


echo
echo "[6/8] Pytest collection"

python3 \
  -m pytest \
  --collect-only \
  -q

echo "Pytest collection: PASS"


echo
echo "[7/8] Offline regression tests"

"$REPO_ROOT/scripts/run-unit.sh"

echo "Offline regression tests: PASS"

echo
echo "[8/8] Git safety"

if git ls-files \
    | grep -qE '(^|/)\.env$'; then

    echo "ERROR: .env is tracked by Git."
    exit 1
fi

if git ls-files \
    | grep -qE '\.(pem|key|p12|pfx)$'; then

    echo "ERROR: credential file "
    echo "is tracked by Git."
    exit 1
fi

echo "Git safety: PASS"

echo
echo "======================================"
echo "E2E VALIDATION: PASSED"
echo "======================================"
```

## llm-gateway-e2e/scripts/run-all.sh

Source: [scripts/run-all.sh](../../llm-gateway-e2e/scripts/run-all.sh) — SHA256 `abe581c9ac1fe3faee37221e439e29ef6b9ff6062a576cb6ee902a1fb898739b`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")" &&
    pwd
)"

"$SCRIPT_DIR/run-unit.sh"
"$SCRIPT_DIR/run-smoke.sh"
"$SCRIPT_DIR/run-live.sh"
```

## llm-gateway-e2e/scripts/run-live.sh

Source: [scripts/run-live.sh](../../llm-gateway-e2e/scripts/run-live.sh) — SHA256 `0eea8e8059627f02de7328deb99c209519a117f2ec8d6c657078f9c43ae2541e`

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
    -m "live" \
    "$@"
```

## llm-gateway-e2e/scripts/run-smoke.sh

Source: [scripts/run-smoke.sh](../../llm-gateway-e2e/scripts/run-smoke.sh) — SHA256 `1e2060b21c63c2278dfd416c839d10365105575455dae3d05d1b103ab7ee71d5`

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

python3 -m pytest \
    -v \
    -m "not live and not unit"
```

## llm-gateway-e2e/scripts/run-unit.sh

Source: [scripts/run-unit.sh](../../llm-gateway-e2e/scripts/run-unit.sh) — SHA256 `94683e2e4dcdd8d18f930a2908133926544c713724bbd8c66fc6180e7053da50`

```bash
#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

python3 -m pytest -v -m "unit" "$@"
```

## llm-gateway-e2e/scripts/security/audit-python.sh

Source: [scripts/security/audit-python.sh](../../llm-gateway-e2e/scripts/security/audit-python.sh) — SHA256 `3f30152fc3182b923e047b2f11fa72be5e8ed607626f57376da6008832c4e0d2`

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

if [ "$#" -ne 1 ]; then
  echo "Usage:"
  echo "  $0 <requirements-file>"
  exit 1
fi

REQUIREMENTS_FILE="$1"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "ERROR: requirements file not found:"
  echo "$REQUIREMENTS_FILE"
  exit 1
fi

# Reuse an installed auditor when available; CI retains isolated-tool fallback.
if [ -n "${PIP_AUDIT_BIN:-}" ]; then
  "$PIP_AUDIT_BIN" -r "$REQUIREMENTS_FILE"
  exit 0
fi

PIP_AUDIT_VERSION="${PIP_AUDIT_VERSION:-2.10.1}"

TEMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

echo
echo "======================================"
echo "Python Dependency Audit"
echo "======================================"

echo
echo "Requirements:"
echo "  $REQUIREMENTS_FILE"

echo
echo "pip-audit:"
echo "  $PIP_AUDIT_VERSION"

python3 \
  -m venv \
  "$TEMP_DIR/venv"

"$TEMP_DIR/venv/bin/python" \
  -m pip \
  install \
  --quiet \
  --upgrade pip

"$TEMP_DIR/venv/bin/python" \
  -m pip \
  install \
  --quiet \
  "pip-audit==$PIP_AUDIT_VERSION"

"$TEMP_DIR/venv/bin/pip-audit" \
  -r "$REQUIREMENTS_FILE"

echo
echo "======================================"
echo "PYTHON DEPENDENCY AUDIT: PASSED"
echo "======================================"
```

## llm-gateway-e2e/scripts/security/scan-secrets.sh

Source: [scripts/security/scan-secrets.sh](../../llm-gateway-e2e/scripts/security/scan-secrets.sh) — SHA256 `032cceed19a1b385dd7d4fea7e965c98a59f70da3e82bbc818674d9b52ede7c2`

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
GITLEAKS_IMAGE="${GITLEAKS_IMAGE:-ghcr.io/gitleaks/gitleaks:v8.28.0}"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
scanner() {
  if [ -n "${GITLEAKS_BIN:-}" ]; then
    "$GITLEAKS_BIN" "$@"
  else
    docker run --rm --interactive --network=none \
      --volume "$TEMP_DIR:$TEMP_DIR:ro" "$GITLEAKS_IMAGE" "$@"
  fi
}
scanner version
cat > "$TEMP_DIR/canary.toml" <<'CANARY'
title = "LLM Gateway Gitleaks Canary"
[[rules]]
id = "llm-gateway-canary"
regex = '''COMPANY_GITLEAKS_CANARY_[A-Z0-9]{24}'''
CANARY
set +e
printf '%s\n' 'COMPANY_GITLEAKS_CANARY_ABCDEF1234567890ABCDEFGH' \
  | scanner --config="$TEMP_DIR/canary.toml" --redact --exit-code=42 stdin >/dev/null 2>&1
CANARY_STATUS=$?
set -e
if [ "$CANARY_STATUS" -ne 42 ]; then
  echo "ERROR: scanner canary failed ($CANARY_STATUS, expected 42)" >&2
  exit 1
fi
echo "Scanner engine self-test: PASS"
echo "Repository history scan"
git log -p --all --full-history --no-renames | scanner --redact stdin
echo "Current tracked and non-ignored files scan"
# Include uncommitted and new source files, but never ignored .env/backups.
python3 - <<'PYCODE' | scanner --redact stdin
from pathlib import Path
import subprocess, sys
names = subprocess.check_output(['git', 'ls-files', '-c', '-o', '--exclude-standard', '-z']).split(b'\0')
for name in sorted(set(names)):
    if not name:
        continue
    path = Path(name.decode())
    if path.is_file() and not path.is_symlink():
        sys.stdout.buffer.write(b'\nFILE: ' + name + b'\n' + path.read_bytes() + b'\n')
PYCODE
echo "SECRET SCAN: PASSED"
```

## llm-gateway-e2e/tests/client.py

Source: [tests/client.py](../../llm-gateway-e2e/tests/client.py) — SHA256 `090a767f294d18e4cb3af10c7d37aad8f9a6e9227e7eb41250e151151a2959d7`

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

Source: [tests/conftest.py](../../llm-gateway-e2e/tests/conftest.py) — SHA256 `633557354777d9a046be61ed4608b9716a9abbcfcf037f22bf31a31b1d4d0bf1`

```python
from __future__ import annotations

import os
import uuid

import pytest

from tests.client import LiteLLMClient


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
```

## llm-gateway-e2e/tests/test_inference.py

Source: [tests/test_inference.py](../../llm-gateway-e2e/tests/test_inference.py) — SHA256 `4b9f18da5f798d29f7f3f279313b8f91c9e6fc593ea947816c2bd4e060d077d6`

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
def test_streaming(
    user_client,
    fast_model,
):
    response = user_client.post(
        "/v1/chat/completions",
        stream=True,
        json={
            "model": fast_model,
            "stream": True,
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

## llm-gateway-e2e/tests/test_lifecycle.py

Source: [tests/test_lifecycle.py](../../llm-gateway-e2e/tests/test_lifecycle.py) — SHA256 `cb08ff2ac3738021783467460bd92781b92146cc9b4aaf4d52b6aad0d2341388`

```python
import pytest
import time

from tests.client import LiteLLMClient
from datetime import datetime, timedelta, timezone


@pytest.mark.live
def test_multiple_user_keys_work_before_offboarding(
    admin_client: LiteLLMClient,
    multi_key_identity: dict,
    multi_key_clients: dict[str, LiteLLMClient],
    fast_model: str,
):
    keys = multi_key_identity["keys"]

    assert set(keys) == {
        "developer-laptop",
        "developer-ci",
    }
    assert set(multi_key_clients) == set(keys)

    distinct_keys = (
        keys["developer-laptop"]["virtual_key"]
        != keys["developer-ci"]["virtual_key"]
    )

    assert distinct_keys, "Expected two distinct virtual keys"

    for usage, client in multi_key_clients.items():
        key_alias = keys[usage]["key_alias"]

        response = admin_client.get(
            "/key/info",
            params={
                "key": keys[usage]["virtual_key"],
            },
        )

        assert response.status_code == 200, (
            f"Cannot read key info for {key_alias}: "
            f"HTTP {response.status_code}"
        )

        info = response.json()["info"]

        same_user = (
            info.get("user_id")
            == multi_key_identity["user_id"]
        )
        same_team = (
            info.get("team_id")
            == multi_key_identity["team_id"]
        )

        assert same_user, f"Unexpected user for {key_alias}"
        assert same_team, f"Unexpected team for {key_alias}"

        response = client.post(
            "/v1/chat/completions",
            json={
                "model": fast_model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Reply with exactly: ok",
                    },
                ],
                "max_tokens": 8,
            },
        )

        print(
            f"{key_alias}: HTTP {response.status_code}"
        )

        assert response.status_code == 200, (
            f"Key should work before offboarding: {key_alias}, "
            f"HTTP {response.status_code}"
        )

        content = (
            response.json()["choices"][0]
            ["message"]["content"]
        )

        assert isinstance(content, str) and content.strip(), (
            f"Expected non-empty inference content for {key_alias}"
        )


@pytest.mark.live
@pytest.mark.spend
def test_user_offboarding_blocks_all_keys(
    admin_client: LiteLLMClient,
    multi_key_identity: dict,
    multi_key_clients: dict[str, LiteLLMClient],
    fast_model: str,
):
    user_id = multi_key_identity["user_id"]

    history_start = (
        datetime.now(timezone.utc) - timedelta(minutes=1)
    ).strftime("%Y-%m-%d %H:%M:%S")

    # 1. Temukan key melalui gateway.
    before = admin_client.list_user_keys(
        user_id=user_id,
        page_size=1,
    )

    expected_aliases = {
        item["key_alias"]
        for item in multi_key_identity["keys"].values()
    }

    actual_aliases = {
        item["key_alias"]
        for item in before
    }

    assert len(before) == 2
    assert actual_aliases == expected_aliases

    # 2. Buktikan kedua credential bisa digunakan.
    for usage, client in multi_key_clients.items():
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": fast_model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Reply with exactly: ok",
                    },
                ],
                "max_tokens": 8,
            },
        )

        print(
            f"before offboarding: {usage}, "
            f"HTTP {response.status_code}"
        )

        assert response.status_code == 200, (
            f"{usage} should work before offboarding"
        )

        content = (
            response.json()["choices"][0]
            ["message"]["content"]
        )

        assert isinstance(content, str) and content.strip()

    # Tunggu spend kedua key dan user tercatat.
    deadline = time.monotonic() + 20

    key_spend_before = {}
    user_spend_before = 0.0
    spend_ready = False

    while time.monotonic() < deadline:
        snapshot = admin_client.list_user_keys(
            user_id=user_id,
            page_size=1,
        )

        same_keys = (
            {item["token"] for item in snapshot}
            == {item["token"] for item in before}
        )

        assert same_keys, (
            "Key records changed while waiting for spend"
        )

        key_spend_before = {
            item["token"]: float(item.get("spend") or 0)
            for item in snapshot
        }

        response = admin_client.get(
            "/user/info",
            params={
                "user_id": user_id,
            },
        )

        assert response.status_code == 200, (
            "Cannot read user spend: "
            f"HTTP {response.status_code}"
        )

        user_info = response.json().get("user_info", {})

        user_spend_before = float(
            user_info.get("spend") or 0
        )

        spend_ready = (
            len(key_spend_before) == 2
            and all(
                spend > 0
                for spend in key_spend_before.values()
            )
            and user_spend_before > 0
        )

        if spend_ready:
            break

        time.sleep(1)

    assert spend_ready, (
        "Spend was not recorded for both keys and user "
        "within the polling window"
    )

    print(
        "before offboarding: "
        f"keys_with_spend={len(key_spend_before)}, "
        f"user_spend={user_spend_before:.8f}"
    )

    history_end = (
        datetime.now(timezone.utc) + timedelta(minutes=1)
    ).strftime("%Y-%m-%d %H:%M:%S")

    expected_tokens = set(key_spend_before)
    history_before = {}
    deadline = time.monotonic() + 20

    while time.monotonic() < deadline:
        history_page = admin_client.list_user_spend_logs_page(
            user_id=user_id,
            start_date=history_start,
            end_date=history_end,
        )

        rows = history_page["data"]

        # Fixture ini hanya menghasilkan sedikit request.
        # Jangan diam-diam mengabaikan halaman tambahan.
        assert not history_page.get("total_is_capped", False)
        assert history_page["total"] == len(rows), (
            "History exceeds one page; pagination is required"
        )

        history_before = {}

        for row in rows:
            spend = float(row.get("spend") or 0)

            if spend <= 0:
                continue

            request_id = row.get("request_id")
            assert isinstance(request_id, str) and request_id, (
                "Paid history record has no request identifier"
            )

            known_key = row.get("api_key") in expected_tokens
            same_user = row.get("user") == user_id
            same_team = (
                row.get("team_id")
                == multi_key_identity["team_id"]
            )

            assert known_key, "Unexpected key in paid history"
            assert same_user, "Unexpected user in paid history"
            assert same_team, "Unexpected team in paid history"
            assert request_id not in history_before, (
                "Duplicate request identifier in paid history"
            )

            history_before[request_id] = {
                "api_key": row["api_key"],
                "user": row["user"],
                "team_id": row["team_id"],
                "spend": spend,
            }

        covered_tokens = {
            row["api_key"]
            for row in history_before.values()
        }

        if covered_tokens == expected_tokens:
            break

        time.sleep(1)

    all_keys_covered = (
        {
            row["api_key"]
            for row in history_before.values()
        }
        == expected_tokens
    )

    assert all_keys_covered, (
        "Paid history was not recorded for both keys "
        "within the polling window"
    )

    print(
        "history before offboarding: "
        f"paid_records={len(history_before)}, "
        f"keys_covered={len(expected_tokens)}"
    )

    # 3. Offboard berdasarkan user_id saja.
    result = admin_client.offboard_user_keys(
        user_id=user_id,
        page_size=1,
    )

    assert result["discovered_count"] == 2
    assert result["blocked_count"] == 2

    # 4. Baca ulang status yang tersimpan.
    after = admin_client.list_user_keys(
        user_id=user_id,
        page_size=1,
    )

    assert len(after) == 2

    same_keys = (
        {item["token"] for item in before}
        == {item["token"] for item in after}
    )

    assert same_keys, "Key records changed during offboarding"

    for item in after:
        key_alias = item["key_alias"]
        blocked = item.get("blocked")

        print(
            f"after offboarding: {key_alias}, "
            f"blocked={blocked}"
        )

        assert blocked is True, (
            f"Key is not blocked: {key_alias}"
        )

    # 5. Credential lama harus ditolak setelah offboarding.
    rejected_statuses = {}

    for usage, client in multi_key_clients.items():
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": fast_model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Reply with exactly: ok",
                    },
                ],
                "max_tokens": 8,
            },
        )

        rejected_statuses[usage] = response.status_code

        print(
            f"after offboarding: {usage}, "
            f"HTTP {response.status_code}"
        )

    assert len(rejected_statuses) == 2

    for usage, status in rejected_statuses.items():
        assert status in {401, 403}, (
            f"Old key should be rejected: {usage}, "
            f"HTTP {status}"
        )

    # 6. Periksa retensi spend dan atribusi setelah offboarding.
    retained_keys = admin_client.list_user_keys(
        user_id=user_id,
        page_size=1,
    )

    same_keys = (
        {item["token"] for item in retained_keys}
        == set(key_spend_before)
    )

    assert same_keys, (
        "Key records were lost or replaced after offboarding"
    )

    for item in retained_keys:
        key_alias = item["key_alias"]

        same_user = item.get("user_id") == user_id
        same_team = (
            item.get("team_id")
            == multi_key_identity["team_id"]
        )

        assert same_user, f"User attribution changed: {key_alias}"
        assert same_team, f"Team attribution changed: {key_alias}"

        spend_before = key_spend_before[item["token"]]
        spend_after = float(item.get("spend") or 0)

        assert spend_after >= spend_before, (
            f"Key spend decreased after offboarding: {key_alias}, "
            f"before={spend_before}, after={spend_after}"
        )

        print(
            f"retained: {key_alias}, "
            f"spend_before={spend_before:.8f}, "
            f"spend_after={spend_after:.8f}"
        )

    response = admin_client.get(
        "/user/info",
        params={
            "user_id": user_id,
        },
    )

    assert response.status_code == 200, (
        "User record is unavailable after offboarding: "
        f"HTTP {response.status_code}"
    )

    user_info_after = response.json().get("user_info", {})

    same_user_record = (
        user_info_after.get("user_id") == user_id
    )

    assert same_user_record, "Unexpected user record after offboarding"

    user_spend_after = float(
        user_info_after.get("spend") or 0
    )

    assert user_spend_after >= user_spend_before, (
        "User spend decreased after offboarding: "
        f"before={user_spend_before}, after={user_spend_after}"
    )

    print(
        "retained user spend: "
        f"before={user_spend_before:.8f}, "
        f"after={user_spend_after:.8f}"
    )

        # 7. Histori request sebelum offboarding harus tetap utuh.
    history_page_after = admin_client.list_user_spend_logs_page(
        user_id=user_id,
        start_date=history_start,
        end_date=history_end,
    )

    rows_after = history_page_after["data"]

    assert not history_page_after.get("total_is_capped", False)
    assert history_page_after["total"] == len(rows_after), (
        "History exceeds one page; pagination is required"
    )

    history_after = {}

    for row in rows_after:
        request_id = row.get("request_id")

        # Hanya bandingkan request yang sudah ada pada baseline.
        if request_id not in history_before:
            continue

        assert request_id not in history_after, (
            "Duplicate baseline request in retained history"
        )

        history_after[request_id] = row

    all_requests_retained = (
        set(history_after) == set(history_before)
    )

    assert all_requests_retained, (
        "Historical requests disappeared after offboarding: "
        f"expected={len(history_before)}, "
        f"found={len(history_after)}"
    )

    for request_id, original in history_before.items():
        retained = history_after[request_id]

        same_attribution = all(
            retained.get(field) == original[field]
            for field in ("api_key", "user", "team_id")
        )

        assert same_attribution, (
            "Historical key/user/team attribution changed "
            "after offboarding"
        )

        spend_after = float(retained.get("spend") or 0)

        assert spend_after == original["spend"], (
            "Historical request spend changed after offboarding: "
            f"before={original['spend']}, "
            f"after={spend_after}"
        )

    print(
        "history retained: "
        f"requests={len(history_after)}, "
        "attribution_unchanged=True, "
        "spend_unchanged=True"
    )
```

## llm-gateway-e2e/tests/unit/conftest.py

Source: [tests/unit/conftest.py](../../llm-gateway-e2e/tests/unit/conftest.py) — SHA256 `b0ff707ac0cd10c5c3a7961328b96d0b038d1b20cc61a193e237a938fad70af5`

```python
import json
from unittest.mock import Mock

import pytest
import requests

from tests.client import LiteLLMClient


@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    def reject(*args, **kwargs):
        raise AssertionError("Unit tests must not send HTTP requests")

    monkeypatch.setattr(requests.sessions.Session, "request", reject)


@pytest.fixture()
def json_response():
    def make(data, status=200):
        response = requests.Response()
        response.status_code = status
        response._content = json.dumps(data).encode("utf-8")
        return response

    return make


@pytest.fixture()
def offline_client():
    client = LiteLLMClient("http://unused.invalid", "unit-placeholder")
    client.get = Mock(side_effect=AssertionError("Unexpected GET"))
    client.post = Mock(side_effect=AssertionError("Unexpected POST"))
    return client
```

## llm-gateway-e2e/tests/unit/test_history_retention.py

Source: [tests/unit/test_history_retention.py](../../llm-gateway-e2e/tests/unit/test_history_retention.py) — SHA256 `e9892a0614221a7d881b34f76aac700d8044c6c996d06ecc9db65a2e42350c99`

```python
from copy import deepcopy
from unittest.mock import Mock

import pytest

from tests.test_lifecycle import (
    test_user_offboarding_blocks_all_keys as assert_lifecycle,
)


pytestmark = pytest.mark.unit


@pytest.mark.parametrize(("mutation", "message"), [
    (None, None),
    ("missing-request", "Historical requests disappeared"),
    ("api_key", "Historical key/user/team attribution changed"),
    ("user", "Historical key/user/team attribution changed"),
    ("team_id", "Historical key/user/team attribution changed"),
    ("spend", "Historical request spend changed"),
], ids=["intact", "missing-request", "changed-key", "changed-user",
        "changed-team", "changed-spend"])
def test_lifecycle_assertions_detect_history_regression(
    offline_client, json_response, mutation, message,
):
    identity = {
        "user_id": "unit-user", "team_id": "unit-team",
        "keys": {
            usage: {"key_alias": usage}
            for usage in ("developer-laptop", "developer-ci")
        },
    }
    keys = [
        {
            "token": f"unit-token-{index}", "key_alias": usage,
            "user_id": identity["user_id"], "team_id": identity["team_id"],
            "spend": 0.01, "blocked": False,
        }
        for index, usage in enumerate(identity["keys"])
    ]
    blocked = [{**key, "blocked": True} for key in keys]
    before = [
        {
            "request_id": f"request-{index}", "api_key": key["token"],
            "user": identity["user_id"], "team_id": identity["team_id"],
            "spend": 0.01,
        }
        for index, key in enumerate(keys)
    ]
    after = deepcopy(before)
    if mutation == "missing-request":
        after.pop()
    elif mutation:
        after[0][mutation] = 0.005 if mutation == "spend" else "changed"

    admin = offline_client
    # Initial discovery, spend baseline, helper discovery, status, retention.
    admin.list_user_keys = Mock(side_effect=[keys, keys, keys, blocked, blocked])
    admin.post.side_effect = [json_response(key) for key in blocked]
    admin.get.side_effect = [
        json_response({"user_info": {"user_id": identity["user_id"], "spend": 0.02}})
        for _ in range(2)
    ]
    admin.list_user_spend_logs_page = Mock(side_effect=[
        {"data": before, "total": len(before), "total_is_capped": False},
        {"data": after, "total": len(after), "total_is_capped": False},
    ])
    clients = {}
    for usage in identity["keys"]:
        client = Mock()
        client.post.side_effect = [
            json_response({"choices": [{"message": {"content": "ok"}}]}),
            json_response({}, 401),
        ]
        clients[usage] = client

    # Exercise the actual H9D assertions; do not duplicate their logic here.
    if message:
        with pytest.raises(AssertionError, match=message):
            assert_lifecycle(admin, identity, clients, "company-fast")
    else:
        assert_lifecycle(admin, identity, clients, "company-fast")

    assert admin.post.call_count == 2
    assert all(client.post.call_count == 2 for client in clients.values())
```

## llm-gateway-e2e/tests/unit/test_offboarding_client.py

Source: [tests/unit/test_offboarding_client.py](../../llm-gateway-e2e/tests/unit/test_offboarding_client.py) — SHA256 `86509618acd3b59d5d430496ddf0d65af597d715a96eff938fcc1a1b35c023a2`

```python
from unittest.mock import Mock, call

import pytest


pytestmark = pytest.mark.unit

USER = "unit-user"
KEYS = [
    {"token": "unit-token-a", "user_id": USER},
    {"token": "unit-token-b", "user_id": USER},
]


def page(number, keys, total=2, pages=2):
    return {
        "current_page": number,
        "keys": keys,
        "total_count": total,
        "total_pages": pages,
    }


def test_offboarding_discovers_every_page_before_blocking(
    offline_client, json_response,
):
    client = offline_client
    client.get.side_effect = [
        json_response(page(1, [KEYS[0]])),
        json_response(page(2, [KEYS[1]])),
    ]

    def block(path, *, json):
        assert client.get.call_count == 2
        assert path == "/key/block"
        return json_response({
            "token": json["key"], "user_id": USER, "blocked": True,
        })

    client.post.side_effect = block
    result = client.offboard_user_keys(user_id=USER, page_size=1)

    assert result == {
        "user_id": USER, "discovered_count": 2, "blocked_count": 2,
    }
    assert client.post.call_args_list == [
        call("/key/block", json={"key": key["token"]}) for key in KEYS
    ]
    for number, request in enumerate(client.get.call_args_list, start=1):
        assert request == call("/key/list", params={
            "user_id": USER, "page": number, "size": 1,
            "return_full_object": "true",
            "include_team_keys": "false",
            "include_created_by_keys": "false",
        })


@pytest.mark.parametrize(("pages", "message"), [
    ([page(1, [KEYS[0]]), page(2, [{**KEYS[1], "user_id": "other"}])],
     "another user's key"),
    ([page(1, [KEYS[0]]), page(2, [KEYS[0]])], "Duplicate key"),
    ([page(1, [KEYS[0]]), page(2, [KEYS[1]], total=3)], "Key count changed"),
    ([page(1, [KEYS[0]], pages=1)], "Incomplete key discovery"),
    ([page(2, [KEYS[0]])], "Unexpected key-list page"),
    ([page(1, [])], "Empty page"),
    ([page(1, [{**KEYS[0], "token": ""}])], "no token identifier"),
], ids=["other-user", "duplicate", "changed-count", "incomplete",
        "wrong-page", "empty-page", "missing-token"])
def test_invalid_discovery_never_blocks_any_key(
    offline_client, json_response, pages, message,
):
    offline_client.get.side_effect = [json_response(p) for p in pages]

    with pytest.raises(AssertionError, match=message):
        offline_client.offboard_user_keys(user_id=USER, page_size=1)

    offline_client.post.assert_not_called()


@pytest.mark.parametrize("failure", [
    "http", "exception", "wrong-token", "wrong-user", "not-blocked",
])
def test_partial_block_failure_continues_and_reports_failure(
    offline_client, json_response, failure,
):
    client = offline_client
    client.list_user_keys = Mock(return_value=KEYS)
    first = {**KEYS[0], "blocked": True}
    status = 200
    if failure == "http":
        status = 500
    elif failure == "wrong-token":
        first["token"] = "different-token"
    elif failure == "wrong-user":
        first["user_id"] = "other-user"
    elif failure == "not-blocked":
        first["blocked"] = False

    first_response = (
        RuntimeError("private-response-placeholder") if failure == "exception"
        else json_response(first, status)
    )
    client.post.side_effect = [
        first_response,
        json_response({**KEYS[1], "blocked": True}),
    ]

    with pytest.raises(AssertionError, match="Offboarding incomplete") as error:
        client.offboard_user_keys(user_id=USER)

    assert client.post.call_args_list == [
        call("/key/block", json={"key": key["token"]}) for key in KEYS
    ]
    assert "confirmed=1/2" in str(error.value)
    assert "private-response-placeholder" not in str(error.value)
    assert all(key["token"] not in str(error.value) for key in KEYS)
```

## llm-gateway-e2e/tests/unit/test_suite_validator.py

Source: [tests/unit/test_suite_validator.py](../../llm-gateway-e2e/tests/unit/test_suite_validator.py) — SHA256 `6afa75cd9997beb0e599f8abe206fb27c6c56ad8671ec2fd1479380aeaf420d9`

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
], ids=["complete", "missing-multi-key", "missing-offboarding"])
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
        assert replaced, "Lifecycle test was already missing from the real suite"
        assert result.returncode != 0
        assert "required regression test(s) missing" in result.stderr
        assert missing in result.stderr
```
