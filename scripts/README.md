# Scripts

- `check_patch_coverage.sh` — pre-push gate: 80% project coverage and 100% patch coverage against `origin/main`.
- `apply_github_hardening.sh` — repository settings, secret scanning, vulnerability alerts, and rulesets. Requires `gh` with admin rights.

```bash
scripts/apply_github_hardening.sh
```
