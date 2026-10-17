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
