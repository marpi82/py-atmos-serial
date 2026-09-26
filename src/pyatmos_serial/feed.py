"""Push feed for a passive RS485 listen.

The feed reads bytes and publishes :class:`RegisterUpdate` only after the
codec returns a frame. Today the codec raises, the loop stays up, and no
register value is invented.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncGenerator, Callable
from contextlib import suppress
from dataclasses import dataclass, field, replace
from typing import Protocol

from pyatmos_serial.errors import ProtocolError, ProtocolUnknownError
from pyatmos_serial.protocol.frame import BusFrame, decode_frames

logger = logging.getLogger(__name__)

_BUFFER_LIMIT = 4096


async def _await_cancelled(task: asyncio.Task[None]) -> None:
    """Wait for a cancelled task without ``contextlib.suppress``."""
    try:
        await task
    except asyncio.CancelledError:
        return


class ByteSource(Protocol):
    """The read call :class:`AtmosSerialFeed` needs from a port."""

    async def read(self, max_bytes: int) -> bytes:
        """Return the next chunk. Empty bytes mean the read timed out."""

    async def close(self) -> None:
        """Release the source. Safe to call more than once."""


@dataclass(frozen=True)
class RegisterUpdate:
    """One raw register value decoded from the bus."""

    register_id: int
    value: int
    ts: float = field(default_factory=time.time)
    seq: int = 0


class EventBus:
    """Multicast bus for :class:`RegisterUpdate` only."""

    def __init__(self) -> None:
        """Create an empty subscriber list."""
        self._subs: list[asyncio.Queue[RegisterUpdate]] = []
        self._seq = 0
        self._lock = asyncio.Lock()

    async def publish(self, update: RegisterUpdate) -> None:
        """Publish ``update`` to every current subscriber.

        Args:
            update: The change to broadcast. ``seq`` is assigned here.
        """
        async with self._lock:
            event = replace(update, seq=self._seq)
            self._seq += 1
            targets = tuple(self._subs)
        for queue in targets:
            await queue.put(event)

    async def subscribe(self) -> AsyncGenerator[RegisterUpdate]:
        """Yield later updates until the consumer is cancelled.

        Yields:
            Register changes published after this call.
        """
        queue: asyncio.Queue[RegisterUpdate] = asyncio.Queue()
        async with self._lock:
            self._subs.append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            async with self._lock:
                with suppress(ValueError):
                    self._subs.remove(queue)


class ValueStore:
    """Raw register values observed on the bus."""

    def __init__(self) -> None:
        """Start with an empty map."""
        self._values: dict[int, int] = {}

    def upsert(self, register_id: int, value: int) -> None:
        """Store ``value`` for ``register_id``.

        Args:
            register_id: Wire register id, once a codec defines one.
            value: Raw word from that register.
        """
        self._values[register_id] = value

    def get(self, register_id: int) -> int | None:
        """Return the last raw value, or ``None`` when it was never stored.

        Args:
            register_id: Wire register id.
        """
        return self._values.get(register_id)


class AtmosSerialFeed:
    """Listen on a byte source and publish decoded changes.

    Args:
        source: Open byte source. This object does not open the port.
        read_size: Maximum bytes requested from each read.
        on_bytes: Called with the size of each non-empty chunk, including
            chunks the codec cannot decode.
    """

    def __init__(
        self,
        source: ByteSource,
        *,
        read_size: int = 256,
        on_bytes: Callable[[int], None] | None = None,
    ) -> None:
        """Store the source. Nothing is read until :meth:`read_once` or :meth:`start`."""
        if read_size <= 0:
            raise ProtocolError("read size must be positive")
        self._source = source
        self._read_size = read_size
        self._on_bytes = on_bytes
        self._buffer = bytearray()
        self._warned = False
        self._task: asyncio.Task[None] | None = None
        self.bytes_seen = 0
        self.bus = EventBus()
        self.store = ValueStore()

    async def read_once(self) -> int:
        """Read one chunk and publish any decoded changes.

        Returns:
            How many updates were published. Zero while the codec is unknown.
        """
        chunk = await self._source.read(self._read_size)
        if not chunk:
            return 0
        self.bytes_seen += len(chunk)
        if self._on_bytes is not None:
            self._on_bytes(len(chunk))
        self._buffer.extend(chunk)
        try:
            frames, remainder = decode_frames(bytes(self._buffer))
        except ProtocolUnknownError:
            self._trim_buffer()
            if not self._warned:
                logger.info("RS485 codec is not implemented; bytes are counted and not decoded")
                self._warned = True
            return 0
        self._buffer = bytearray(remainder)
        return await self._publish(frames)

    def start(self) -> asyncio.Task[None]:
        """Start the listen loop as a task.

        Returns:
            The running task. A second call returns the same task.
        """
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._loop(), name="atmos-serial-feed")
        return self._task

    async def stop(self) -> None:
        """Cancel the listen loop and close the source."""
        task = self._task
        self._task = None
        if task is not None:
            task.cancel()
            await _await_cancelled(task)
        await self._source.close()

    async def _publish(self, frames: tuple[BusFrame, ...]) -> int:
        published = 0
        for frame in frames:
            if self.store.get(frame.register_id) == frame.value:
                continue
            self.store.upsert(frame.register_id, frame.value)
            await self.bus.publish(RegisterUpdate(register_id=frame.register_id, value=frame.value))
            published += 1
        return published

    def _trim_buffer(self) -> None:
        extra = len(self._buffer) - _BUFFER_LIMIT
        if extra > 0:
            del self._buffer[:extra]

    async def _loop(self) -> None:
        try:
            while True:
                await self.read_once()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("RS485 listen failed")
            raise
