#!/usr/bin/env python3
"""Validate documentation locally; no network, Docker, provider, or runtime writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


def prose_lines(text):
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        match = re.match(r'(`{3,}|~{3,})', stripped)
        if match:
            delimiter = match.group(1)
            if fence is None:
                fence = delimiter
            elif delimiter[0] == fence[0] and len(delimiter) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield line
    if fence:
        raise ValueError('unclosed code fence')


def anchors(path):
    seen = {}
    result = set()
    for line in prose_lines(path.read_text()):
        match = re.match(r'^#{1,6}\s+(.+?)(?:\s+#+)?$', line)
        if not match:
            continue
        slug = re.sub(r'[^\w\- ]', '', match.group(1).lower()).replace(' ', '-')
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if count == 0 else f'{slug}-{count}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', action='store_true', help='Require sibling source repositories and validate their entrypoint links too')
    args = parser.parse_args()
    errors, skipped = [], set()
    required = [
        'README.md', 'MASTER_CONTEXT.md', 'architecture/overview.md',
        'architecture/phase-1.md', 'architecture/phase-2.md', 'architecture/phase-3.md',
        'adr/README.md', 'adr/INDEX.md', 'operations/README.md',
        'operations/deployment.md', 'operations/backup.md', 'operations/incident.md',
        'operations/rollback.md', 'operations/lifecycle.md', 'operations/phase1-checklist.md',
        'developer/opencode.md', 'developer/api.md', 'developer/model-catalog.md',
        'developer/compatibility.md', 'handover/AI_CONTINUATION.md',
        'handover/HUMAN_HANDOVER.md', 'handover/WORK_LOG.md', 'reports/README.md',
        'reports/docs-migration/migration-manifest.json', 'archive/README.md',
    ]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append(f'Missing required document: {name}')
    for number in range(1, 18):
        if len(list((ROOT / 'adr').glob(f'{number:03}-*.md'))) != 1:
            errors.append(f'ADR-{number:03}: expected exactly one document')
    for phase, count in [(1, 19), (2, 13), (3, 10)]:
        path = ROOT / f'architecture/phase-{phase}.md'
        if path.is_file():
            text = path.read_text()
            for task in range(count):
                if f'P{phase}-{task:02}' not in text:
                    errors.append(f'Missing roadmap ID P{phase}-{task:02}')
    docs = sorted(ROOT.rglob('*.md'))
    if args.workspace:
        for repo in ['llm-gateway-infra', 'llm-gateway-config', 'llm-gateway-e2e']:
            readme = WORKSPACE / repo / 'README.md'
            if readme.is_file():
                docs.append(readme)
            else:
                errors.append(f'Sibling repository README missing: {repo}')
        for name in ['PROJECT_CONTEXT_MASTER.md', 'PROJECT_MASTER_CONTEXT.md', 'LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md']:
            if (WORKSPACE / name).exists():
                docs.append(WORKSPACE / name)
    checked = 0
    for doc in docs:
        try:
            lines = list(prose_lines(doc.read_text()))
            for line in lines:
                for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', line):
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', raw):
                        continue
                    raw = unquote(raw.strip('<>'))
                    location, _, fragment = raw.partition('#')
                    target = (doc.parent / location).resolve() if location else doc.resolve()
                    internal = target == ROOT or ROOT in target.parents
                    if not internal and not args.workspace:
                        skipped.add(str(target))
                        continue
                    if not target.exists():
                        errors.append(f'{doc.relative_to(WORKSPACE)}: broken link {raw}')
                    elif fragment and target.suffix == '.md' and fragment not in anchors(target):
                        errors.append(f'{doc.relative_to(WORKSPACE)}: missing anchor {raw}')
                    checked += 1
        except (ValueError, OSError) as error:
            errors.append(f'{doc}: {error}')
    manifest = ROOT / 'reports/docs-migration/migration-manifest.json'
    preserved = 0
    if manifest.exists():
        for item in json.loads(manifest.read_text())['files']:
            target = ROOT / item['to'].removeprefix('llm-gateway-docs/')
            if not target.is_file():
                errors.append(f'Migrated file missing: {target}')
            elif item['kind'] == 'historical-evidence':
                if hashlib.sha256(target.read_bytes()).hexdigest() != item['source_sha256']:
                    errors.append(f'Historical evidence changed: {target}')
                preserved += 1
    if errors:
        print('\n'.join('ERROR: ' + error for error in errors), file=sys.stderr)
        return 1
    print(f'DOCS VALIDATION: PASS ({len(docs)} Markdown files; {checked} local links; {preserved} historical evidence files unchanged)')
    print('Roadmap P1/P2/P3 and ADR001-017: PASS')
    if skipped:
        print(f'Skipped {len(skipped)} external workspace targets; use --workspace with sibling repos for full verification')
    return 0


if __name__ == '__main__':
    sys.exit(main())
