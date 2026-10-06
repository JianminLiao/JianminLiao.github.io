# Website security and publishing

This is a public, static academic website. Its browser pages have no scripts,
forms, login, analytics, or third-party resources. Keep that small attack surface
unless a new feature has been deliberately reviewed.

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

The HTML CSP disables JavaScript and external resources. The meta form cannot
set `frame-ancestors`, so it does not prevent another site from embedding a page.
Full response-header controls would require a hosting/proxy change. The current
site has no authenticated or sensitive actions that could be clickjacked.

## Recovery

If a publication fails, fix it in a new PR; do not bypass the gate. If an update
breaks the site, revert the offending commit through a PR and let the checks
deploy the previous content. Keep the last successful deployment available while
investigating. If a credential is exposed, revoke/rotate it first; removing it
from the latest version does not remove it from public history.
