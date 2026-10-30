"""Build the public-only static edition. Never changes the working deck or deploys.

Run locally before committing site/dist. The Pages workflow publishes dist only;
the private working deck and this project's work/ sources are not CI inputs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import shutil

PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT / "4PW-journal-club_preview.html"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "dist"
DATA_RE = re.compile(r'(<script id="deck-data" type="application/json">\s*)(.*?)(\s*</script>)', re.S)
LOCAL_URL = re.compile(r'file:(?:/{1,3})[^\s<>"\]\)]+', re.I)
WIN_PATH = re.compile(r'(?<![\w])(?:[A-Za-z]:[\\/])[^\r\n<>"\|]*')
LOOPBACK = re.compile(r'https?://(?:localhost|127\.0\.0\.1|\[::1\])(?=[:/]|$)[^\s<>"\]\)]*', re.I)
RAW_PERSON = re.compile(
    r'(?:consultation|transcript|fieldwork).{0,350}(?:\blines?\s*\d|\bparticipant\b|\bchair\b|\bdirector\b|\b(?:Sep|September)\b)'
    r'|(?:\bparticipant\b|\bchair\b|\bdirector\b).{0,350}(?:consultation|transcript)', re.I | re.S)
SOURCE_RECORD = re.compile(r'consultation|transcript|fieldwork', re.I)
PRIVATE_IDS = {'v27', 'v56', 'protocol4pw', 'cgr_protocol', 'cgr_candidates'}
STUDY_TARGET = '#study-material'
PRIVATE_NOTE = 'Unpublished study material is not included in this public edition.'
REDACTION_NOTE = (
    'Participant-level consultation details are omitted from the public edition. '
    'The working ledger retains the original record. Recorded contribution counts '
    'and review-depth assessments have not been recalculated after this omission; '
    'they are not independent causal validation.'
)
RAW_CANDIDATE_FIELDS = {
    'abstract_as_supplied', 'unlabelled_flag_8', 'unlabelled_flag_9',
    'unlabelled_flag_10', 'unlabelled_flag_12', 'repeated_work_id', 'attachment_line',
}


def sensitive_record(obj: dict) -> bool:
    return bool(SOURCE_RECORD.search(' '.join(str(obj.get(k, '')) for k in ('kind', 'source', 'source_locator'))))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prepare(source: Path, updated_at: str) -> tuple[str, dict, list[str], dict]:
    original = source.read_text(encoding='utf-8')
    match = DATA_RE.search(original)
    if not match:
        raise ValueError('Cannot locate deck-data JSON; no files written.')
    deck = json.loads(match[2])
    scene_ids = [s['id'] for s in deck['scenes']]
    counts = Counter()
    redacted_by_link = {}

    # Raw unpublished consultation rows are withheld, not relabelled as studies.
    for link_id, ledger in deck.get('model_ledger', {}).items():
        rows = ledger.get('selected_rows', [])
        public_rows = [row for row in rows if not sensitive_record(row)]
        withheld = len(rows) - len(public_rows)
        if withheld:
            ledger['selected_rows'] = public_rows
            ledger['public_redacted_selected_records'] = withheld
            ledger['public_redaction_note'] = REDACTION_NOTE
            redacted_by_link[link_id] = withheld
            counts['consultation_selected_records_withheld'] += withheld

    for record in deck.get('cgr_candidate_set', {}).get('records', []):
        for key in RAW_CANDIDATE_FIELDS:
            if key in record:
                if key == 'abstract_as_supplied' and record[key]:
                    counts['raw_abstract_fields_removed'] += 1
                record.pop(key)
                counts['raw_export_fields_removed'] += 1

    # All private references remain labelled as unpublished working materials.
    for ref_id, ref in deck.get('references', {}).items():
        private = ref_id in PRIVATE_IDS or ref.get('working_material') is True
        local_target = any(str(ref.get(k, '')).lower().startswith('file:') for k in ('url', 'original_url'))
        if private:
            ref['url'] = ref['original_url'] = STUDY_TARGET
            ref['working_material'] = True
            ref['presentation_citation'] = False
            ref['public_access_note'] = PRIVATE_NOTE
            counts['working_references_redirected'] += 1
        elif local_target:
            public_url = next((str(ref[k]) for k in ('original_url', 'url') if str(ref.get(k, '')).startswith(('https://', 'http://'))), None)
            ref['url'] = ref['original_url'] = public_url or STUDY_TARGET
            ref['public_access_note'] = ('Public source target retained.' if public_url else
                                        'The locally held source document is not included in this public edition.')
            # A locally held workshop PDF is not thereby an unpublished working
            # model. Preserve its author/year APA metadata and citation status.
            counts['locally_held_source_targets_redirected'] += 1

    def sanitize(value, path=()):
        if isinstance(value, list):
            return [sanitize(item, path + (i,)) for i, item in enumerate(value)]
        if isinstance(value, dict):
            if sensitive_record(value) and any(k in value for k in ('source_locator', 'source', 'context')):
                # Thin index references keep their link/index mapping, never roles,
                # dates, transcript line locators, paraphrases or appraisals.
                identity = {k: value[k] for k in ('link_id', 'evlist_index', 'index_base', 'row_index_0based') if k in value}
                identity.update({'source_locator': 'Unpublished consultation record; participant details withheld',
                                 'url': STUDY_TARGET, 'public_redacted': True})
                counts['private_record_references_redacted'] += 1
                return identity
            output = {}
            for key, item in value.items():
                if key == 'source_json_path':
                    counts['technical_source_paths_removed'] += 1
                    continue
                output[key] = sanitize(item, path + (key,))
            return output
        if not isinstance(value, str):
            return value
        if RAW_PERSON.search(value):
            counts['participant_level_narratives_withheld'] += 1
            return REDACTION_NOTE
        text = value
        if LOCAL_URL.search(text) or LOOPBACK.search(text):
            if text.strip().lower().startswith(('file:', 'http://localhost', 'https://localhost', 'http://127.', 'https://127.')):
                counts['local_source_targets_replaced'] += 1
                return STUDY_TARGET if str(path[-1]).lower().endswith(('url', 'href', 'link')) else PRIVATE_NOTE
            text, n = LOCAL_URL.subn(PRIVATE_NOTE, text)
            counts['inline_local_urls_removed'] += n
            text, n = LOOPBACK.subn(PRIVATE_NOTE, text)
            counts['inline_loopback_urls_removed'] += n
        if WIN_PATH.search(text):
            text, n = WIN_PATH.subn('[local source path omitted]', text)
            counts['absolute_machine_paths_removed'] += n
        return text

    deck = sanitize(deck)
    deck['public_edition'] = {
        'updated_at': updated_at,
        'status': 'Working research presentation',
        'private_material_boundary': PRIVATE_NOTE,
        'consultation_redaction': REDACTION_NOTE,
        'contribution_count_boundary': 'Counts describe the original recorded ledger, including contributions withheld here. They are not independent-study counts.',
    }
    if [s['id'] for s in deck['scenes']] != scene_ids:
        raise ValueError('Scene inventory changed during sanitization.')
    assets = sorted({s['visual']['src'] for s in deck['scenes']
                     if s.get('visual', {}).get('kind') in ('art', 'source-figure')})
    for asset in assets:
        candidate = (source.parent / asset).resolve()
        if not candidate.is_relative_to(source.parent.resolve()) or not candidate.is_file():
            raise ValueError(f'Missing or out-of-project asset: {asset}')
        if candidate.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.svg'}:
            raise ValueError(f'Unexpected public asset type: {asset}')

    encoded = json.dumps(deck, ensure_ascii=False, indent=2).replace('</script', '<\\/script')
    result = original[:match.start(2)] + encoded + original[match.end(2):]
    # Make evidence-drawer counts explicit without changing the source counts.
    old = '`${link.source_contribution_count} non-placeholder contributions in this link ledger; ${rows.length} selected records shown below.`'
    new = ('`${link.source_contribution_count} non-placeholder contributions in the original link ledger; '
           '${rows.length} public selected records shown below.'
           '${link.public_redacted_selected_records?` ${link.public_redacted_selected_records} participant-level selected records withheld from this public edition. Counts and recorded review-depth assessments were not recalculated.`:""}`')
    if old not in result:
        raise ValueError('Evidence count rendering changed; review the public-copy patch before building.')
    result = result.replace(old, new, 1)
    result = result.replace('</head>', make_public_font_css() + '\n</head>', 1)
    # Only runtime-generated source links point at #study-material. A dedicated
    # accessible modal explains this boundary instead of opening an empty tab.
    public_ui = make_public_ui(updated_at)
    if '</body>' not in result:
        raise ValueError('No body closing tag found.')
    result = result.replace('</body>', public_ui + '\n</body>', 1)
    # Initial HTML templates must not conceal machine paths outside deck-data.
    if LOCAL_URL.search(result) or WIN_PATH.search(result) or LOOPBACK.search(result):
        raise ValueError('An absolute/local URL remains in the public copy; no output written.')
    if RAW_PERSON.search(json.dumps(deck, ensure_ascii=False)):
        # Schema labels such as consultation source-kind counts are permitted;
        # participant-level narrative was removed above. Inspect only strings.
        def raw_strings(x):
            if isinstance(x, dict):
                for v in x.values(): yield from raw_strings(v)
            elif isinstance(x, list):
                for v in x: yield from raw_strings(v)
            elif isinstance(x, str): yield x
        safe_notices = {REDACTION_NOTE, 'Unpublished consultation record; participant details withheld'}
        if any(RAW_PERSON.search(x) for x in raw_strings(deck) if x not in safe_notices):
            raise ValueError('A participant-level consultation string remains.')
    report = {
        'source_sha256': digest(source.read_bytes()), 'public_html_sha256': digest(result.encode()),
        'updated_at': updated_at, 'logical_pages': len(scene_ids), 'scene_ids': scene_ids,
        'assets': assets, 'transforms': dict(counts), 'redacted_selected_records_by_link': redacted_by_link,
        'boundary': REDACTION_NOTE,
        'main_source_modified': False, 'deployment_performed': False,
        'font_files_included': False,
    }
    return result, deck, assets, report


def make_public_font_css() -> str:
    # These are local() aliases, never font binaries. DB remains first for Thai.
    # Thai adjustment: three real deck sentences, normal/bold, Edge shaping;
    # exact measurements are retained only in work/public-font-metrics.json.
    return '''<style id="public-font-fallback">
@font-face{font-family:"Journal Public Latin";src:local("Arial"),local("Roboto"),local("Liberation Sans");font-style:normal;font-weight:300 600;font-display:swap;size-adjust:68.5%;unicode-range:U+0000-0DFF,U+0E80-10FFFF}
@font-face{font-family:"Journal Public Latin";src:local("Arial-BoldMT"),local("Arial Bold"),local("Roboto Bold"),local("Liberation Sans Bold");font-style:normal;font-weight:700 900;font-display:swap;size-adjust:67.3%;unicode-range:U+0000-0DFF,U+0E80-10FFFF}
@font-face{font-family:"Journal Public Latin";src:local("Arial-ItalicMT"),local("Arial Italic"),local("Roboto Italic"),local("Liberation Sans Italic");font-style:italic;font-weight:300 600;font-display:swap;size-adjust:68.5%;unicode-range:U+0000-0DFF,U+0E80-10FFFF}
@font-face{font-family:"Journal Public Latin";src:local("Arial-BoldItalicMT"),local("Arial Bold Italic"),local("Roboto Bold Italic"),local("Liberation Sans Bold Italic");font-style:italic;font-weight:700 900;font-display:swap;size-adjust:67.3%;unicode-range:U+0000-0DFF,U+0E80-10FFFF}
@font-face{font-family:"Journal Public Leelawadee";src:local("LeelawadeeUI"),local("Leelawadee UI");font-style:normal;font-weight:300 600;font-display:swap;size-adjust:73.4%;unicode-range:U+0E00-0E7F}
@font-face{font-family:"Journal Public Leelawadee";src:local("LeelawadeeUI-Bold"),local("Leelawadee UI Bold");font-style:normal;font-weight:700 900;font-display:swap;size-adjust:67.4%;unicode-range:U+0E00-0E7F}
@font-face{font-family:"Journal Public Tahoma";src:local("Tahoma");font-style:normal;font-weight:300 600;font-display:swap;size-adjust:67.9%;unicode-range:U+0E00-0E7F}
@font-face{font-family:"Journal Public Tahoma";src:local("Tahoma-Bold"),local("Tahoma Bold");font-style:normal;font-weight:700 900;font-display:swap;size-adjust:64.5%;unicode-range:U+0E00-0E7F}
:root{--font:"Journal Helvetica","Journal Public Latin","Journal DB Helvethaica","Journal Public Leelawadee","Journal Public Tahoma","DB Helvethaica X",Helvetica,Arial,"Thonburi","Noto Sans Thai",sans-serif}
</style>'''


def make_public_ui(updated_at: str) -> str:
    # No external dependency, font redistribution, telemetry or auto reload.
    config = json.dumps({'updated_at': updated_at}, ensure_ascii=False).replace('<', '\\u003c')
    return r'''
<!-- Public-edition source boundary; the working deck is unchanged. -->
<style>
.public-status{display:flex;align-items:center;gap:8px;font:12px/1.2 Arial,sans-serif;color:#6e6e73}.public-status button{font:inherit!important;color:#06c!important;white-space:nowrap}.public-status__update[hidden]{display:none}
.public-material{width:min(760px,calc(100vw - 36px));max-height:calc(100dvh - 50px);overflow:auto;border:1px solid #e5e5ea;border-radius:18px;padding:30px;color:#1d1d1f;background:#fff;font-family:var(--font,Arial,sans-serif)}
.public-material::backdrop{background:rgba(0,0,0,.35)}.public-material h2{font-size:35px;line-height:1.2;margin:0 0 20px}.public-material p{font-size:25px;line-height:1.35}.public-material button{font-size:25px;color:#06c;padding:8px 0}.public-material a{color:#06c}
@media(max-width:700px){.public-status{display:none}.public-material{padding:24px}.public-material p{font-size:23px}}
@media print{.public-status,.public-material{display:none!important}}
</style>
<aside class="public-status" aria-label="Public edition status"><span id="public-release-label"></span><button type="button" id="public-material-open">Source notes</button><span class="public-status__update" hidden><span>New revision available.</span><button type="button" id="public-reload">Reload</button></span></aside>
<dialog class="public-material" id="study-material" aria-labelledby="study-material-title"><h2 id="study-material-title">Study materials and evidence boundary</h2><p>This is a working research presentation. Published sources remain linked to their original public pages where available. The study model, draft review protocols and candidate literature register are unpublished working materials; their original files are not included in this public edition. Some cited workshop documents are locally held and are also not distributed here; their original citation metadata is retained.</p><p>Participant-level consultation records, transcript locators and identifying role/date combinations are withheld. The public presentation retains the recorded model structure, source-contribution counts, support status and review-depth assessments. Those counts and assessments describe the original working ledger, include withheld contributions and have not been recomputed after redaction. They are not independent-study counts or causal validation.</p><p>Candidate references retain their provisional screening and reading-depth labels. This edition omits raw abstract-export fields. The planned reviews and hypotheses remain distinct from completed or independently verified findings.</p><p>Source figures retain their original attribution and the recorded CC BY-NC 4.0 licence. Fonts are requested from the viewer’s device; no font binaries are distributed.</p><p><a href="SOURCE_NOTES.md" target="_blank" rel="noopener noreferrer">Public-edition source notes</a></p><form method="dialog"><button>Close source notes</button></form></dialog>
<script>
(()=>{'use strict';const release=PUBLIC_CONFIG,material=document.getElementById('study-material');let lastCheck=0;
const status=document.querySelector('.public-status');document.querySelector('.controls__tools')?.append(status);
const date=new Date(release.updated_at);document.getElementById('public-release-label').textContent=new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeZone:'Asia/Bangkok'}).format(date);status.title='Working research presentation · Updated '+new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeStyle:'short',timeZone:'Asia/Bangkok'}).format(date)+' ICT';
function openMaterial(){if(!material.open)material.showModal()}
document.getElementById('public-material-open').addEventListener('click',openMaterial);
document.addEventListener('click',e=>{const a=e.target.closest?.('a');if(!a)return;let url;try{url=new URL(a.getAttribute('href'),location.href)}catch{return}if(url.origin===location.origin&&url.pathname===location.pathname&&url.hash==='#study-material'){e.preventDefault();e.stopPropagation();openMaterial()}},true);
document.getElementById('public-reload').addEventListener('click',()=>location.reload());
async function checkRelease(){if(location.protocol==='file:'||Date.now()-lastCheck<60000)return;lastCheck=Date.now();try{const response=await fetch('version.json',{cache:'no-store'});if(!response.ok)return;const latest=await response.json();if(latest.updated_at&&new Date(latest.updated_at)>new Date(release.updated_at))document.querySelector('.public-status__update').hidden=false}catch{}}
window.addEventListener('focus',checkRelease);setInterval(checkRelease,300000);
})();
</script>'''.replace('PUBLIC_CONFIG', config)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--updated-at', help='ISO 8601 release timestamp; defaults to the build time in Asia/Bangkok')
    parser.add_argument('--check', action='store_true', help='Validate and report without writing the bundle')
    args = parser.parse_args()
    updated_at = args.updated_at or datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
    datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
    source = args.source.resolve()
    html, deck, assets, report = prepare(source, updated_at)
    if not args.check:
        output = args.output.resolve()
        if output == source.parent or not output.is_relative_to(PROJECT.resolve()):
            raise ValueError('Output must be a distinct folder inside this project.')
        output.mkdir(parents=True, exist_ok=True)
        (output / 'index.html').write_text(html, encoding='utf-8', newline='\n')
        for relative in assets:
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source.parent / relative, target)
        (output / '.nojekyll').write_text('', encoding='utf-8', newline='\n')
        (output / 'version.json').write_text(json.dumps({'revision': report['public_html_sha256'][:12], 'updated_at': updated_at, 'entry_url': './'}, indent=2) + '\n', encoding='utf-8', newline='\n')
        (output / 'SOURCE_NOTES.md').write_text(
            '# Public edition\n\nWorking research presentation; updated ' + updated_at + '.\n\n' +
            PRIVATE_NOTE + '\n\n' + REDACTION_NOTE + '\n\n' +
            'Published citations link to their original sources. Candidate literature is provisional; screening labels do not establish inclusion or causal support. Original source figures retain their attribution and recorded CC BY-NC 4.0 licence. No private source files, raw candidate abstract exports or font binaries are distributed.\n', encoding='utf-8', newline='\n')
        # The manifest is deliberately public-safe: no paths or withheld content.
        manifest = {'updated_at': updated_at, 'logical_pages': len(deck['scenes']), 'files': []}
        for relative in ['index.html', '.nojekyll', 'version.json', 'SOURCE_NOTES.md', *assets]:
            f = output / relative
            manifest['files'].append({'path': relative, 'sha256': digest(f.read_bytes()), 'bytes': f.stat().st_size})
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
        (Path(__file__).parent / 'public-build-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'check_only': args.check, 'logical_pages': len(deck['scenes']), 'assets': len(assets), 'transforms': report['transforms'], 'source_sha256': report['source_sha256'], 'deployment_performed': False}, ensure_ascii=True))


if __name__ == '__main__':
    main()
