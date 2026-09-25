---
applyTo: "src/pyatmos_serial/protocol/**"
---

# Protocol

The RS485 frame layout, checksum, and register map are unknown.

- `decode_frames` returns an empty result only for an empty buffer.
- Any other buffer raises `ProtocolUnknownError` and does not consume the bytes.
- `CODEC_IMPLEMENTED` stays `False` until a decoder is backed by a captured frame and a test.
- Do not add a CRC polynomial, start byte, or baud constant presented as fact.
