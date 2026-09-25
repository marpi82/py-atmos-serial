"""RS485 codec.

The public names are the shape a future decoder will fill. Nothing here
parses a captured frame.
"""

from pyatmos_serial.protocol.frame import CODEC_IMPLEMENTED, BusFrame, decode_frames

__all__ = ["CODEC_IMPLEMENTED", "BusFrame", "decode_frames"]
