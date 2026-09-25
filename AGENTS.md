# AGENTS.md — py-atmos-serial

Passive RS485 listener for an ATMOS boiler bus. Sketch only: the codec is not implemented.

## Project shape

- **Layout**: src-layout, package `src/pyatmos_serial/`, tests in `tests/`.
- **Python**: `>=3.13.2,<3.15`.
- **PyPI distribution**: `py-atmos-serial` (import as `pyatmos_serial`).
- **Build**: hatchling + hatch-vcs. Never hardcode a version in `pyproject.toml`.
- **Sibling**: `py-atmos-wg1000` is the pull client. This package does not import it.

## Architecture

`SerialPortSource` reads bytes. `AtmosSerialFeed` buffers them and calls `decode_frames`. That function raises `ProtocolUnknownError` until the bus is reverse-engineered. The feed then keeps a bounded buffer, counts bytes, and publishes no `RegisterUpdate`. `CODEC_IMPLEMENTED` stays `False`.

Do not invent framing, checksums, baud, or register ids. A decoded update is the only freshness signal the Home Assistant integration may prefer over WG1000.

## Commands

```bash
uv sync --group dev --group test --group docs --locked --python 3.13
uv run --group dev --group test poe validate
```

Pre-commit hooks exist. **pre-push** runs pytest with an 80% project floor and 100% patch coverage vs `origin/main` (`scripts/check_patch_coverage.sh`). CI uploads `coverage.xml` to Codecov when `CODECOV_TOKEN` is set.

Repository rulesets are applied with `scripts/apply_github_hardening.sh`. Required checks on `main`: `secrets (gitleaks)`, `security (pip-audit)`, `quality (lint + typecheck)`, `tests (3.13)`, `docs-verify`, `build`.

## Conventions

English only. mypy `--strict`. Ruff line length 130, Google docstrings. Async-first: serial reads go through `asyncio.to_thread`. No `Any`. Logging via `logging.getLogger(__name__)`; the package root attaches a `NullHandler`.
