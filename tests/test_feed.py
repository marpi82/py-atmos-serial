"""Listen loop counts bytes and publishes nothing while the codec is unknown."""

from __future__ import annotations

import asyncio

import pytest

from pyatmos_serial.errors import ProtocolError
from pyatmos_serial.feed import AtmosSerialFeed, RegisterUpdate
from pyatmos_serial.protocol.frame import BusFrame, decode_frames


class _Memory:
    def __init__(self, chunks: list[bytes]) -> None:
        self._chunks = list(chunks)
        self.closed = False

    async def read(self, max_bytes: int) -> bytes:
        del max_bytes
        if not self._chunks:
            await asyncio.sleep(3600)
            return b""
        return self._chunks.pop(0)

    async def close(self) -> None:
        self.closed = True


def test_read_size_must_be_positive() -> None:
    """A zero read would spin."""
    with pytest.raises(ProtocolError, match="read size"):
        AtmosSerialFeed(_Memory([]), read_size=0)


async def test_unknown_codec_counts_bytes_and_publishes_nothing() -> None:
    """Raw traffic is not turned into a register value."""
    seen: list[int] = []
    source = _Memory([b"\x10\x20", b"\x30"])
    feed = AtmosSerialFeed(source, on_bytes=seen.append)

    assert await feed.read_once() == 0
    assert await feed.read_once() == 0
    assert feed.bytes_seen == 3
    assert seen == [2, 1]
    assert feed.store.get(1) is None


async def test_listen_task_survives_unknown_frames_until_stopped() -> None:
    """The loop logs the missing codec once and keeps reading."""
    source = _Memory([b"\xaa", b"\xbb"])
    feed = AtmosSerialFeed(source)
    task = feed.start()
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    assert feed.bytes_seen == 2
    assert not task.done()
    await feed.stop()
    assert source.closed
    assert task.cancelled() or task.done()


async def test_publish_path_skips_a_repeated_value(monkeypatch: pytest.MonkeyPatch) -> None:
    """When a decoder exists, the bus stays quiet if the word did not change."""

    def _decode(buffer: bytes) -> tuple[tuple[BusFrame, ...], bytes]:
        if not buffer:
            return (), b""
        return (BusFrame(register_id=7, value=buffer[0]),), b""

    monkeypatch.setattr("pyatmos_serial.feed.decode_frames", _decode)
    source = _Memory([b"\x05", b"\x05", b"\x09"])
    feed = AtmosSerialFeed(source)
    found: list[RegisterUpdate] = []

    async def collect() -> None:
        async for update in feed.bus.subscribe():
            found.append(update)
            if len(found) == 2:
                return

    collector = asyncio.create_task(collect())
    await asyncio.sleep(0)
    assert await feed.read_once() == 1
    assert await feed.read_once() == 0
    assert await feed.read_once() == 1
    await collector
    assert [item.value for item in found] == [5, 9]
    assert feed.store.get(7) == 9
    assert decode_frames(b"") == ((), b"")


def test_value_store_round_trip() -> None:
    """The store is a plain map of raw words."""
    feed = AtmosSerialFeed(_Memory([]))
    assert feed.store.get(3) is None
    feed.store.upsert(3, 11)
    assert feed.store.get(3) == 11
