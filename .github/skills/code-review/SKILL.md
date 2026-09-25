---
name: code-review
description: Review checklist for py-atmos-serial pull requests. Use when reviewing PRs to verify the listen path stays passive, the codec is not invented, async safety, mypy strict compliance, public API stability, tests, and security.
---

# Code Review — py-atmos-serial

Review procedure for pull requests to this library. Work through every section; only comment on real issues, with file/line references and a concrete suggested fix.

## 1. Correctness — bus and codec

- [ ] The library still only listens. No transmit path was added without an explicit decision.
- [ ] `decode_frames` still refuses unknown bytes, unless the PR includes a captured frame and a test.
- [ ] `CODEC_IMPLEMENTED` flips to `True` only in the same change as a real decoder.
- [ ] Raw bytes are not published as `RegisterUpdate`.

## 2. Async & concurrency

- [ ] Serial I/O uses `asyncio.to_thread`.
- [ ] The listen task logs failures and does not die silently. Suppress only expected cancellation.

## 3. Typing & style gates

- [ ] mypy `--strict`-clean; new `Any`/`cast`/`type: ignore` justified.
- [ ] Ruff: line length 130, Google docstrings on new public objects.
- [ ] Pydantic v2 idioms only.
- [ ] English-only code, comments, docstrings.

## 4. Public API & versioning

- [ ] `pyatmos_serial.__all__` unchanged, or the breaking change is explicit in the PR.
- [ ] No version string edited in `pyproject.toml` (hatch-vcs/CalVer from git tags).
- [ ] New dependencies justified and added via uv.

## 5. Error handling

- [ ] Unknown framing surfaces as `ProtocolUnknownError`.
- [ ] No broad `except Exception` without logging.

## 6. Tests

- [ ] New behavior covered; suite passes without hardware.
- [ ] Coverage gate (80%) not weakened.

## 7. Security & secrets

- [ ] No credentials or bus captures with private data in code, tests, or logs.

## 8. Docs

- [ ] Public behavior changes reflected in `docs/` (Sphinx `-W`).
- [ ] README still says the codec is unimplemented, until that stops being true.

## How to report

- One comment per issue. Prioritize blockers (invented protocol, transmit, crash), then majors (CI gate, typing, missing tests), then minors (style, docs).
- Prefer the smallest change that fits existing patterns.
