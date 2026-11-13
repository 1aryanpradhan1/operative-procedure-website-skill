#!/usr/bin/env python3
"""Copy the PR #1 reference and expose its editable runtime, styles and JSON data."""
import argparse
import gzip
import json
import re
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.skill_dir.resolve() / 'assets/source'
    dest = args.output.resolve()
    if dest.exists():
        raise SystemExit('Choose a new empty project path; existing projects are never overwritten.')
    html = (source / 'index.html').read_text()
    loader = (source / 'assets/loader.js').read_text()
    match = re.search(r'const files\s*=\s*(\[.*?\])\s*,\s*message\s*=', loader, re.S)
    if not match:
        raise SystemExit('Unexpected reference loader; inspect its anatomy chunk list.')
    pieces = []
    for name in json.loads(match.group(1)):
        path = (source / name).resolve()
        if not path.is_relative_to(source):
            raise SystemExit('Invalid retained asset path.')
        pieces.append(path.read_bytes())
    meshes = json.loads(gzip.decompress(b''.join(pieces)))
    manifest = json.loads((source / 'data/manifest.json').read_text())
    if not isinstance(meshes, list) or len(meshes) != manifest['structure_count']:
        raise SystemExit('Retained anatomy and manifest counts disagree.')
    payloads = {'mesh-data': meshes, 'manifest-data': manifest}
    runtime = (source / 'assets/app.js').read_text()
    old = 'const { meshes, manifest } = window.__PTERIONAL_DATA__;'
    new = "const guideData = window.__GUIDE_DATA__;\n    const meshes = guideData?.['mesh-data'] ?? JSON.parse($('#mesh-data').textContent);\n    const manifest = guideData?.['manifest-data'] ?? JSON.parse($('#manifest-data').textContent);"
    if runtime.count(old) != 1:
        raise SystemExit('Unexpected reference runtime; inspect its data reader before adapting.')
    runtime = runtime.replace(old, new)
    stylesheet = '<link rel="stylesheet" href="assets/styles.css">'
    runtime_tag = '<script defer src="assets/loader.js"></script>'
    if html.count(stylesheet) != 1 or html.count(runtime_tag) != 1:
        raise SystemExit('Unexpected reference stylesheet or runtime insertion point.')
    # Keep the upstream CSS exact; inline it for the existing offline/hosted packager.
    html = html.replace(stylesheet, '<style>\n' + (source / 'assets/styles.css').read_text() + '\n</style>')
    html = html.replace(runtime_tag, '<!-- GUIDE_DATA -->\n<!-- GUIDE_RUNTIME -->')
    html = re.sub(r'<div id="anatomy-loading".*?</div>', '', html, count=1, flags=re.S)
    html = re.sub(r'<noscript>.*?</noscript>', '', html, count=1, flags=re.S)
    for folder in ['src', 'data', 'research', 'static']:
        (dest / folder).mkdir(parents=True)
    shutil.copytree(source, dest / 'baseline')
    (dest / 'src/index.html').write_text(html)
    (dest / 'src/app.js').write_text(runtime)
    for key, value in payloads.items():
        (dest / 'data' / f'{key}.json').write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')))
    shutil.copy2(source / 'ATTRIBUTION.md', dest / 'ATTRIBUTION.md')
    shutil.copy2(source / 'reference-revision.json', dest / 'reference-revision.json')
    (dest / 'adaptation-status.json').write_text(json.dumps({
        'referenceCase': 'Pterional Craniotomy', 'status': 'unadapted reference',
        'required': 'Replace procedure content, sources, anatomy, masks, markers, instruments, laterality logic and all case-specific runtime branches before delivering another procedure.'
    }, indent=2))
    print(json.dumps({'project': str(dest), 'meshCount': len(meshes), 'dataIds': sorted(payloads),
                      'status': 'Editable reference copied; no new procedure has been generated.'}))


if __name__ == '__main__':
    main()
