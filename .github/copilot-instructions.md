# py-atmos-serial Copilot Instructions

## Critical AI Guidelines

### Core Principles
1. **Always refer to the latest documentation** — Check `docs/` and `AGENTS.md` for current architecture and patterns
2. **100% English code** — All files, comments, docstrings must be in English
3. **Base on existing files** — Never create code blindly. When uncertain, ask instead of guessing
4. **Home Assistant focus** — This library is the push (listen) side. `py-atmos-wg1000` is the pull side

### Language & Type Requirements (Python 3.13.2+)

- Complete type annotations; pass `mypy --strict`
- Follow PEP 621 for `pyproject.toml`
- Tooling: uv, Hatch/Hatchling, Ruff, Sphinx + Google-style docstrings
- Serial reads go through `asyncio.to_thread`

## Project Overview

**py-atmos-serial** passively listens on an ATMOS boiler RS485 bus.

- The port, buffer, and `RegisterUpdate` bus exist
- `decode_frames` raises `ProtocolUnknownError` for any non-empty buffer
- `CODEC_IMPLEMENTED` is `False`

Do not invent framing, checksums, baud, or register ids.

## Key modules

- `src/pyatmos_serial/port.py` — serial settings and the threaded port
- `src/pyatmos_serial/feed.py` — listen loop, store, bus
- `src/pyatmos_serial/protocol/frame.py` — unimplemented codec

## Do not

- Transmit on the bus
- Commit `.env` or live captures
- Treat raw bytes as a decoded register
- Hardcode a package version in `pyproject.toml`
