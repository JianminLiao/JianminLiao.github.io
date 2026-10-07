# Website security and publishing

This is a public, static academic website with no forms or login. The homepage
has one reviewed exception for the deferred Umami Cloud analytics tracker;
other pages retain the script-free policy. Review any additional external
resources explicitly before changing the policy.

## Every update

1. Work on a branch and add intended files to Git.
2. Add new public pages or assets to `site-files.txt`. Local notes, credentials,
   workflow files, and maintenance scripts never belong in that list.
3. Run `python3 -m unittest discover -s scripts -p 'test_*.py'` and
   `python3 scripts/check_site.py`.
4. Open a pull request, wait for **Security checks**, then merge. The owner can
   merge their own passing PR; another person's approval is not required.
5. Confirm that the **Website** workflow deployed successfully.

The workflow stages only approved files into a fresh `_site/` directory. A failed
check prevents deployment and leaves the previous site online. An ignored file
can still be added with `git add -f`; the checks also reject tracked local
coordination files. Never disable a check just to make a publication pass.

All HTML pages must include the CSP and referrer policy defined in
`scripts/check_site.py`, before loading any resources. Use external local CSS,
not inline styles. SVGs must remain passive illustrations. Existing mathematical
source files and simulation scripts are intentionally public downloads; GitHub
Pages does not execute those Python files.

## Umami Cloud exception

Only `index.html` may load `https://cloud.umami.is/script.js`. Its CSP permits
that exact script path and connections to `https://gateway.umami.is`, the Cloud
collection endpoint documented in the [official changelog](https://docs.umami.is/docs/cloud/changelog).
Do not allow all HTTPS scripts, inline JavaScript, or extra script attributes.
The checks require one deferred tracker, a website UUID, no inline script body,
and no collection-host override. An unfilled Website ID blocks publication.

The Website ID is public tracking configuration, not an account password or
API key. Account credentials stay in Chrome's password manager. The account's
private statistics must not be exposed through a shared/public dashboard unless
the owner explicitly requests it. The script is hosted and updated by Umami;
the narrow CSP does not remove that third-party trust requirement.

This integration covers only the homepage. Article pages, downloads, and outbound
link clicks are not explicitly instrumented. No user IDs, custom visitor data,
session replay, or heatmap configuration is added. The default tracker can send
page URLs (including query parameters) and available referrer information, so
never put private data in public URLs. Cookie-free analytics still undercounts
visitors using blocking tools; visitor counts are approximate.

## Dependencies and permissions

The checker uses the Python standard library. Browser pages need no runtime
packages. GitHub Actions use official actions pinned to complete commit hashes;
Dependabot proposes weekly version updates through PRs, which run the same checks.
Review these updates before merging; there is no automatic merge.

Checks run with a read-only repository token and no saved checkout credentials.
Only the deployment job receives Pages/OIDC permissions, and it only runs for
main in the `github-pages` environment. Keep that environment restricted to main.
Keep GitHub secret scanning, push protection, and HTTPS enforcement enabled.

Keep main protected against force pushes and deletion, with a PR and the
**Security checks** result required before merging. Repository administrators
can still change protection settings, so these checks do not replace account
security. Use a passkey or security key for GitHub and grant integrations only
the access they need. Never commit credentials, even temporarily: public Git
history is public too.

## Public documents and limitations

Before adding or replacing a PDF, inspect its text, metadata, links, attachments,
and active actions. Remove private phone numbers and local paths; do not upload
unreviewed third-party PDFs. The lightweight CI scanner recognizes common key
formats in repository files, but does not unpack PDFs or archives and is not a
complete secret scanner or malware detector.

The HTML CSP blocks unapproved JavaScript and external resources. The meta form cannot
set `frame-ancestors`, so it does not prevent another site from embedding a page.
Full response-header controls would require a hosting/proxy change. The current
site has no authenticated or sensitive actions that could be clickjacked.

## Recovery

If a publication fails, fix it in a new PR; do not bypass the gate. If an update
breaks the site, revert the offending commit through a PR and let the checks
deploy the previous content. Keep the last successful deployment available while
investigating. If a credential is exposed, revoke/rotate it first; removing it
from the latest version does not remove it from public history.
