"""Frame boundary for the boiler RS485 bus.

The layout is unknown. This module refuses to guess a start byte, a length
field, a checksum, or a register encoding.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyatmos_serial.errors import ProtocolUnknownError

# Flipped to True only when decode_frames parses captured traffic.
CODEC_IMPLEMENTED: bool = False


@dataclass(frozen=True)
class BusFrame:
    """One decoded register observation.

    ``register_id`` and ``value`` stay raw until a codec defines them.
    """

    register_id: int
    value: int


def decode_frames(buffer: bytes) -> tuple[tuple[BusFrame, ...], bytes]:
    """Split ``buffer`` into frames and the unconsumed tail.

    Args:
        buffer: Bytes read from the bus since the previous call.

    Returns:
        An empty frame tuple and an empty tail when ``buffer`` is empty.

    Raises:
        ProtocolUnknownError: ``buffer`` is not empty. Framing is not known,
            so the bytes are not consumed by this function.
    """
    if not buffer:
        return (), b""
    raise ProtocolUnknownError("RS485 framing, checksum, and register map have not been reverse-engineered")
