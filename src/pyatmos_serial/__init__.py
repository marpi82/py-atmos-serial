"""Passive RS485 listener for an ATMOS boiler bus."""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from pyatmos_serial.errors import AtmosError, NotOpenError, ProtocolError, ProtocolUnknownError
from pyatmos_serial.feed import AtmosSerialFeed, ByteSource, EventBus, RegisterUpdate, ValueStore
from pyatmos_serial.port import SerialPortSource, SerialSettings
from pyatmos_serial.protocol import CODEC_IMPLEMENTED, BusFrame, decode_frames

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    __version__ = version("py-atmos-serial")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "CODEC_IMPLEMENTED",
    "AtmosError",
    "AtmosSerialFeed",
    "BusFrame",
    "ByteSource",
    "EventBus",
    "NotOpenError",
    "ProtocolError",
    "ProtocolUnknownError",
    "RegisterUpdate",
    "SerialPortSource",
    "SerialSettings",
    "ValueStore",
    "__version__",
    "decode_frames",
]
