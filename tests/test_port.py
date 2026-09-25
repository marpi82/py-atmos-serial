"""Port settings are validated before any device is opened."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from pyatmos_serial.errors import NotOpenError, ProtocolError
from pyatmos_serial.port import SerialPortSource, SerialSettings


class _FakePort:
    def __init__(self) -> None:
        self.closed = False

    def read(self, size: int = 1) -> bytes:
        del size
        return b""

    def close(self) -> None:
        self.closed = True


def test_settings_require_a_port_and_a_positive_baud() -> None:
    """Baud is not defaulted, because the bus speed is unknown."""
    settings = SerialSettings(port="/dev/ttyUSB0", baudrate=9600)
    assert settings.bytesize == 8
    assert settings.parity == "N"
    assert settings.stopbits == 1
    with pytest.raises(ValidationError):
        SerialSettings(port="", baudrate=9600)
    with pytest.raises(ValidationError):
        SerialSettings(port="/dev/ttyUSB0", baudrate=0)


async def test_read_before_open_fails() -> None:
    """The source does not open the device implicitly."""
    source = SerialPortSource(SerialSettings(port="/dev/ttyUSB0", baudrate=9600))
    with pytest.raises(NotOpenError):
        await source.read(8)


async def test_non_positive_read_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """A zero-length read is rejected after the port is open."""
    fake = _FakePort()
    monkeypatch.setattr("pyatmos_serial.port._open_port", lambda _settings: fake)
    source = SerialPortSource(SerialSettings(port="/dev/ttyUSB0", baudrate=9600))
    await source.open()
    with pytest.raises(ProtocolError, match="read size"):
        await source.read(0)
    await source.close()
    assert fake.closed
