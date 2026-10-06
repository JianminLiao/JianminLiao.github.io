"""Regression tests for failures that must block publication."""
from pathlib import Path
import tempfile
import unittest

from check_site import CSP, UMAMI_CSP, UMAMI_SCRIPT, audit


class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tracked = {'site-files.txt', 'index.html'}
        (self.root / 'site-files.txt').write_text('index.html\n')
        self.html = f'''<!doctype html><html><head>
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="no-referrer">
</head><body><h1>Test page</h1></body></html>'''
        (self.root / 'index.html').write_text(self.html)

    def failures(self):
        return audit(self.root, self.tracked)[0]

    def add(self, name, content, public=False):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.tracked.add(name)
        if public:
            with (self.root / 'site-files.txt').open('a') as f:
                f.write(name + '\n')

    def test_safe_page(self):
        self.assertEqual(self.failures(), [])

    def test_private_file_even_outside_public_manifest(self):
        self.add('.handoff/journal.jsonl', '{}')
        self.assertTrue(any('private project file' in e for e in self.failures()))

    def test_token_even_outside_public_manifest(self):
        self.add('notes.txt', 'ghp_' + 'a' * 36)
        self.assertTrue(any('possible credential' in e for e in self.failures()))
        self.assertFalse(any('a' * 36 in e for e in self.failures()))

    def test_script_and_external_resource(self):
        for content in ('<script>alert(1)</script>', '<img src="https://example.com/x.png">', '<p onclick="alert(1)">x</p>', '<a href="javascript:alert(1)">x</a>'):
            with self.subTest(content=content):
                (self.root / 'index.html').write_text(self.html.replace('</body>', content + '</body>'))
                self.assertTrue(self.failures())

    def test_missing_policy(self):
        (self.root / 'index.html').write_text('<html><body>Hello</body></html>')
        self.assertTrue(any('missing approved CSP' in e for e in self.failures()))

    def test_unlisted_asset_and_broken_link(self):
        self.add('thoughts/new.html', self.html)
        self.assertTrue(any('site-files.txt' in e for e in self.failures()))
        (self.root / 'index.html').write_text(self.html.replace('</body>', '<a href="missing.html">Read</a></body>'))
        self.assertTrue(any('local link is missing' in e for e in self.failures()))

    def test_symlink(self):
        (self.root / 'index.html').unlink()
        (self.root / 'index.html').symlink_to('site-files.txt')
        self.assertTrue(any('symbolic links' in e for e in self.failures()))

    def test_active_svg(self):
        self.add('assets/bad.svg', '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>', public=True)
        self.assertTrue(any('active SVG' in e for e in self.failures()))

    def test_css_import(self):
        self.add('styles.css', '@import "https://example.com/a.css";', public=True)
        self.assertTrue(any('must not fetch' in e for e in self.failures()))

    def test_svg_external_style(self):
        self.add('assets/bad.svg', '<svg xmlns="http://www.w3.org/2000/svg"><style>@import "https://example.com/a.css";</style></svg>', public=True)
        self.assertTrue(any('external SVG styles' in e for e in self.failures()))

    def test_unpinned_action(self):
        self.add('.github/workflows/test.yml', 'steps:\n  - uses: actions/checkout@v6\n')
        self.assertTrue(any('full commit hash' in e for e in self.failures()))

    def test_manifest_cannot_publish_repository_config(self):
        self.add('.github/settings.json', '{}', public=True)
        self.assertTrue(any('unexpected public location' in e for e in self.failures()))

    def umami_html(self):
        tracker = f'<script defer src="{UMAMI_SCRIPT}" data-website-id="00000000-0000-4000-8000-000000000001"></script>'
        return self.html.replace(CSP, UMAMI_CSP).replace('</head>', tracker + '</head>')

    def test_umami_only_allowed_on_homepage(self):
        html = self.umami_html()
        (self.root / 'index.html').write_text(html)
        self.assertEqual(self.failures(), [])
        self.add('thoughts/new.html', html, public=True)
        self.assertTrue(any('thoughts/new.html' in e for e in self.failures()))

    def test_umami_rejects_unreviewed_script_changes(self):
        html = self.umami_html()
        variants = [
            html.replace('00000000-0000-4000-8000-000000000001', '__UMAMI_WEBSITE_ID__'),
            html.replace(' defer ', ' '),
            html.replace(UMAMI_SCRIPT, UMAMI_SCRIPT + '?extra=1'),
            html.replace('<script defer', '<script data-host-url="https://example.com" defer'),
            html.replace('</script>', 'alert(1)</script>'),
            html.replace('</script>', ''),
        ]
        for changed in variants:
            with self.subTest(changed=changed):
                (self.root / 'index.html').write_text(changed)
                self.assertTrue(self.failures())

    def test_umami_policy_requires_one_tracker(self):
        html = self.umami_html()
        tracker = html[html.index('<script'):html.index('</script>') + len('</script>')]
        for changed in (html.replace(tracker, ''), html.replace(tracker, tracker * 2), html.replace(UMAMI_CSP, UMAMI_CSP + "; script-src-attr 'unsafe-inline'")):
            with self.subTest(changed=changed):
                (self.root / 'index.html').write_text(changed)
                self.assertTrue(self.failures())


if __name__ == '__main__':
    unittest.main()
