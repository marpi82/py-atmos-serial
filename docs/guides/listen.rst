Listening
=========

Open a port only when you have an adapter on the bus. This does not transmit.

.. code-block:: python

   import asyncio

   from pyatmos_serial import AtmosSerialFeed, SerialPortSource, SerialSettings

   async def main() -> None:
       settings = SerialSettings(port="/dev/ttyUSB0", baudrate=9600)
       source = SerialPortSource(settings)
       await source.open()
       feed = AtmosSerialFeed(source)
       feed.start()
       await asyncio.sleep(2)
       await feed.stop()

   asyncio.run(main())

``feed.bytes_seen`` increases when the adapter delivers bytes. No
``RegisterUpdate`` is published while the codec is unknown. Do not treat raw
bytes as a temperature.
