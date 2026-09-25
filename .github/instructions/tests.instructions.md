---
applyTo: "tests/**"
---

# Tests

- Offline only. Do not open a real serial device.
- Inject a `ByteSource` or monkeypatch `_open_port`.
- A test that decodes a frame must patch `decode_frames` and must not claim the patch is the bus format.
- Docstrings on tests. `S101` is ignored in `tests/`.
