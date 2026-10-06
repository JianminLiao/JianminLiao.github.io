"""Check the static site's security policy and stage only approved public files.

This catches accidental regressions; it is not an HTML sanitizer or a complete
secret scanner. GitHub secret scanning and push protection remain enabled.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

CSP = "default-src 'none'; script-src 'none'; style-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'"
ORIGIN = "https://jianminliao.github.io"
PRIVATE = {'.handoff', '.git', '.ssh', '.aws', '.codex', '.agents', '.venv',
           'AGENTS.md', 'NOW.md', 'CLAUDE.md'}
SECRET_PATTERNS = [
    rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
    rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{35,}\b',
    rb'\bAIza[0-9A-Za-z_-]{35}\b',
    rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
]


def private_path(name):
    path = PurePosixPath(name)
    return (path.is_absolute() or '..' in path.parts
            or any(p in PRIVATE or p == '.env' or p.startswith('.env.') for p in path.parts)
            or path.suffix.lower() in {'.pem', '.key', '.p12', '.pfx'})


class Page(HTMLParser):
    def __init__(self, name, public):
        super().__init__()
        self.name, self.public = name, public
        self.errors = []
        self.csp, self.referrer = False, False

    def fail(self, reason):
        self.errors.append(f'{self.name}:{self.getpos()[0]}: {reason}')

    def check_url(self, value, resource=False):
        target = urlsplit(urljoin(f'{ORIGIN}/{self.name}', value))
        if target.scheme not in ('https', 'mailto'):
            self.fail('URL must use HTTPS, mailto, or a local path')
        elif target.netloc != urlsplit(ORIGIN).netloc or target.scheme == 'mailto':
            if resource:
                self.fail('page resources must be hosted on this site')
        else:
            name = unquote(target.path).lstrip('/')
            if not name or name.endswith('/'):
                name += 'index.html'
            if name not in self.public:
                self.fail(f'local link is missing from site-files.txt: {name}')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if len(a) != len(attrs):
            self.fail('duplicate HTML attributes')
        if tag in {'script', 'style', 'iframe', 'frame', 'frameset', 'object', 'embed', 'form', 'base'}:
            self.fail(f'<{tag}> is outside the static-site policy')
        if any(k.startswith('on') or k == 'style' for k in a):
            self.fail('inline styles and event handlers are not allowed')
        if tag == 'meta':
            directive = a.get('http-equiv', '').lower()
            if directive == 'content-security-policy':
                if a.get('content') != CSP or self.csp:
                    self.fail('use exactly one copy of the approved CSP')
                self.csp = a.get('content') == CSP
            elif directive:
                self.fail('unexpected http-equiv directive')
            if a.get('name', '').lower() == 'referrer':
                self.referrer = a.get('content') == 'no-referrer'
        if tag in {'link', 'img', 'source', 'body'} and not self.csp:
            self.fail('CSP must precede resources and the body')
        if a.get('href'):
            self.check_url(a['href'], resource=tag == 'link' and a.get('rel') != 'canonical')
        if a.get('src'):
            self.check_url(a['src'], resource=True)
        for candidate in a.get('srcset', '').split(','):
            if candidate.strip():
                self.check_url(candidate.split()[0], resource=True)

    handle_startendtag = handle_starttag


def audit(root, tracked):
    public = {line.strip() for line in (root / 'site-files.txt').read_text().splitlines()
              if line.strip() and not line.lstrip().startswith('#')}
    errors = []
    for name in sorted(set(tracked) | public):
        path = root / name
        if private_path(name):
            errors.append(f'{name}: private project file must not be tracked or published')
            continue
        if path.is_symlink():
            errors.append(f'{name}: symbolic links are not allowed')
            continue
        if name not in tracked or not path.is_file():
            errors.append(f'{name}: public files must exist and be tracked by Git')
            continue
        data = path.read_bytes()
        if any(re.search(pattern, data) for pattern in SECRET_PATTERNS):
            errors.append(f'{name}: possible credential; value withheld')
        if name.startswith('.github/workflows/'):
            for action in re.findall(r'^\s*(?:-\s*)?uses:\s*(\S+)', data.decode(), re.M):
                if not re.fullmatch(r'actions/[a-z0-9-]+@[0-9a-f]{40}', action):
                    errors.append(f'{name}: use official actions pinned to a full commit hash')
        if name not in public:
            if path.suffix in {'.html', '.css', '.svg'}:
                errors.append(f'{name}: add this public asset to site-files.txt')
            continue
        parts = PurePosixPath(name).parts
        if name not in {'.nojekyll', 'index.html', '404.html', 'styles.css'} and parts[0] not in {'assets', 'thoughts'}:
            errors.append(f'{name}: unexpected public location')
        if path.suffix not in {'.html', '.css', '.svg', '.pdf', '.png', '.jpg', '.jpeg', '.webp', '.ico', '.txt', '.tex', '.py', '.json'} and name != '.nojekyll':
            errors.append(f'{name}: unapproved public file type')
        if path.suffix == '.html':
            page = Page(name, public)
            page.feed(data.decode())
            errors.extend(page.errors)
            if not page.csp or not page.referrer:
                errors.append(f'{name}: missing approved CSP or referrer policy')
        elif path.suffix == '.svg':
            if re.search(r'@import|url\(\s*[\"\']?(?!#)[^\s\"\')]', data.decode(), re.I):
                errors.append(f'{name}: external SVG styles are not allowed')
            for element in ET.fromstring(data).iter():
                tag = element.tag.rsplit('}', 1)[-1].lower()
                if tag in {'script', 'foreignobject', 'iframe', 'image', 'a', 'animate', 'set', 'animatetransform', 'animatemotion'}:
                    errors.append(f'{name}: active SVG content is not allowed')
                for key, value in element.attrib.items():
                    key = key.rsplit('}', 1)[-1].lower()
                    if key.startswith('on') or (key in {'href', 'src'} and not value.startswith('#')):
                        errors.append(f'{name}: active or external SVG reference')
        elif path.suffix == '.css':
            if re.search(r'@import|url\s*\(', data.decode(), re.I):
                errors.append(f'{name}: stylesheets must not fetch additional resources')
    return errors, public


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New directory for the checked Pages artifact')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')) - {''}
    errors, public = audit(root, tracked)
    if errors:
        raise SystemExit('\n'.join(errors))
    if args.output:
        args.output.mkdir(parents=True, exist_ok=False)
        for name in sorted(public):
            destination = args.output / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / name, destination)
    print(f'Security checks passed: {len(tracked)} tracked files; {len(public)} approved public files.')


if __name__ == '__main__':
    main()
