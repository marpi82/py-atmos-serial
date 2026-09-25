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
uv sync --group dev --group test
uv run --group dev --group test poe validate
```

## Conventions

English only. mypy `--strict`. Ruff line length 130, Google docstrings. Async-first: serial reads go through `asyncio.to_thread`. No `Any`. Logging via `logging.getLogger(__name__)`; the package root attaches a `NullHandler`.
