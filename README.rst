py-atmos-serial
===============

Async Python library for a **passive RS485 listen** on an ATMOS boiler bus.
It is the push-side data layer for the Home Assistant integration in
``ha-atmos``. The gateway library ``py-atmos-wg1000`` remains the pull side.

**PyPI name:** ``py-atmos-serial``. Import as ``import pyatmos_serial``.

**Status:** ``2026.9.0a1`` sketch, published to reserve the PyPI name. The port, the byte buffer, and the update bus exist.
Frame layout, checksum, baud, and the register map have not been
reverse-engineered. :func:`pyatmos_serial.protocol.decode_frames` raises
:class:`pyatmos_serial.errors.ProtocolUnknownError` for any non-empty buffer.
:data:`pyatmos_serial.CODEC_IMPLEMENTED` is ``False``.

What works today
----------------

* :class:`pyatmos_serial.SerialSettings` checks the port name and baud rate.
  8N1 is only a UART placeholder, not a captured bus setting.
* :class:`pyatmos_serial.SerialPortSource` opens a serial port and reads it
  without blocking the event loop.
* :class:`pyatmos_serial.AtmosSerialFeed` counts bytes and would publish
  :class:`pyatmos_serial.RegisterUpdate` when a decoder emits a frame.
  Until then it publishes nothing and keeps the listen loop alive.

What this library does not do
-----------------------------

It does not guess opcodes, CRC polynomials, or register ids. It does not
transmit on the bus. Home Assistant should treat raw bytes as "the port is
alive", and a decoded register update as the only signal that serial data is
fresh enough to prefer over the WG1000 poll.

Development
-----------

Python 3.13. Version comes from git tags (``hatch-vcs``), with fallback
``0.0.0`` until the first tag.

.. code-block:: bash

   uv sync --group dev --group test
   uv run --group dev --group test poe validate
