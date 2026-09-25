Architecture
============

The library is the push side of the ATMOS data layer. ``py-atmos-wg1000``
remains the pull side. Home Assistant prefers a decoded serial sample and
falls back to the gateway.

Listen path
-----------

:class:`pyatmos_serial.port.SerialPortSource` opens a serial adapter and
reads it with ``asyncio.to_thread``. :class:`pyatmos_serial.feed.AtmosSerialFeed`
counts those bytes and calls :func:`pyatmos_serial.protocol.decode_frames`.

Until the bus is reverse-engineered, a non-empty buffer raises
:class:`pyatmos_serial.errors.ProtocolUnknownError`. The feed keeps a bounded
buffer, logs once, and publishes nothing.
:data:`pyatmos_serial.protocol.frame.CODEC_IMPLEMENTED` stays ``False``.

What a future decoder will publish
----------------------------------

:class:`pyatmos_serial.feed.RegisterUpdate` is one raw register word.
:class:`pyatmos_serial.feed.ValueStore` keeps the last word.
:class:`pyatmos_serial.feed.EventBus` yields the update to subscribers.

8N1 is a UART placeholder. Baud rate is a required setting because the bus
speed is not known.
