---
applyTo: "src/pyatmos_serial/**"
---

# Library core

- English only. mypy `--strict`. Ruff line length 130. Google docstrings.
- Async-first. Blocking serial calls go through `asyncio.to_thread`.
- Public names belong in `pyatmos_serial.__all__`.
- Do not invent RS485 framing. Unknown bytes raise `ProtocolUnknownError`.
- Logging uses `logging.getLogger(__name__)`. Do not configure logging here.
