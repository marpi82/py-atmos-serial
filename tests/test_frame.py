"""The codec refuses every non-empty buffer."""

from __future__ import annotations

import pytest

from pyatmos_serial.errors import ProtocolUnknownError
from pyatmos_serial.protocol.frame import CODEC_IMPLEMENTED, decode_frames


def test_codec_flag_stays_off_until_reverse_engineering() -> None:
    """Callers branch on this flag instead of catching the error."""
    assert CODEC_IMPLEMENTED is False


def test_empty_buffer_decodes_to_nothing() -> None:
    """An idle read is not a protocol failure."""
    assert decode_frames(b"") == ((), b"")


def test_any_payload_is_rejected() -> None:
    """No start byte or checksum is assumed."""
    with pytest.raises(ProtocolUnknownError, match="not been reverse-engineered"):
        decode_frames(b"\x00\x01\x02")
