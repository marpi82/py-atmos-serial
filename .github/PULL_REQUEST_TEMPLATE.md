## Summary

<!-- What does this PR change and why? Link related issues with "Fixes #N" / "Closes #N" when applicable. -->

## Type of change

<!-- Check all that apply. -->

- [ ] Bug fix (non-breaking)
- [ ] New feature / enhancement (non-breaking)
- [ ] Breaking change to the **public API** (`AtmosSerialFeed`, `SerialPortSource`, `RegisterUpdate`, or other symbols in `pyatmos_serial.__all__`)
- [ ] Docs only
- [ ] Tests / CI / tooling / chore

## Checklist

- [ ] Commits are signed off (`git commit -s`) — [DCO](https://developercertificate.org/)
- [ ] English only in code, comments, and docs; Google-style docstrings
- [ ] `uv run --group dev --group test poe validate` passes locally
- [ ] Tests added / updated where practical. No real serial device required
- [ ] Docs updated when public behavior changes (`docs/` + Sphinx `-W` clean)
- [ ] No secrets, credentials, or private bus captures committed
- [ ] Frame layout was not invented. A new decoder includes a captured fixture and sets `CODEC_IMPLEMENTED` only then

## Test plan

```bash
uv run --group dev ruff check .
uv run --group dev poe typecheck
uv run --group dev --group test poe test
```
