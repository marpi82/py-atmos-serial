"""Library exceptions."""

from __future__ import annotations


class AtmosError(Exception):
    """Base error for py-atmos-serial."""


class ProtocolError(AtmosError):
    """A caller passed a value this library can already reject."""


class ProtocolUnknownError(AtmosError):
    """RS485 framing has not been reverse-engineered yet."""


class NotOpenError(AtmosError):
    """A read or close was attempted before the port was opened."""
