"""Serial port opened for a passive listen.

8N1 is a UART placeholder. Baud rate is required because the bus speed is
not known yet.
"""

from __future__ import annotations

import asyncio
from typing import Protocol, cast

from pydantic import BaseModel, ConfigDict, Field

from pyatmos_serial.errors import NotOpenError, ProtocolError


class _OpenedPort(Protocol):
    """The slice of ``serial.Serial`` this source uses."""

    def read(self, size: int = 1) -> bytes:
        """Read up to ``size`` bytes."""

    def close(self) -> None:
        """Close the port."""


class SerialSettings(BaseModel):
    """How to open the adapter.

    ``bytesize``, ``parity``, and ``stopbits`` default to 8N1 only so the
    port can be opened. They are not a captured ATMOS setting.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    port: str = Field(min_length=1)
    baudrate: int = Field(gt=0)
    bytesize: int = Field(default=8, ge=5, le=8)
    parity: str = Field(default="N", pattern="^[NEOMS]$")
    stopbits: int = Field(default=1, ge=1, le=2)
    timeout: float = Field(default=1.0, gt=0)


class SerialPortSource:
    """Blocking pyserial port wrapped in ``asyncio.to_thread``."""

    def __init__(self, settings: SerialSettings) -> None:
        """Store settings. The port stays closed until :meth:`open`."""
        self._settings = settings
        self._port: _OpenedPort | None = None

    async def open(self) -> None:
        """Open the port. A second call does nothing."""
        if self._port is not None:
            return
        self._port = await asyncio.to_thread(_open_port, self._settings)

    async def read(self, max_bytes: int) -> bytes:
        """Read up to ``max_bytes``. Empty bytes mean the timeout elapsed.

        Args:
            max_bytes: Maximum number of bytes to return.

        Raises:
            NotOpenError: :meth:`open` has not been called.
            ProtocolError: ``max_bytes`` is not positive.
        """
        port = self._port
        if port is None:
            raise NotOpenError("serial port is not open")
        if max_bytes <= 0:
            raise ProtocolError("read size must be positive")
        return await asyncio.to_thread(port.read, max_bytes)

    async def close(self) -> None:
        """Close the port. Safe to call more than once."""
        port = self._port
        self._port = None
        if port is not None:
            await asyncio.to_thread(port.close)


def _open_port(settings: SerialSettings) -> _OpenedPort:
    import serial

    if not settings.port.strip():
        raise ProtocolError("serial port is empty")
    opened = serial.Serial(
        port=settings.port,
        baudrate=settings.baudrate,
        bytesize=settings.bytesize,
        parity=settings.parity,
        stopbits=settings.stopbits,
        timeout=settings.timeout,
    )
    return cast(_OpenedPort, opened)
