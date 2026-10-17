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
