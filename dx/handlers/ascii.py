from ..handler import handler, TypeConstraint
import codecs


@handler
def ascii(data: bytes) -> str:
    yield data.decode('ascii')


@handler
def rot13(data: str) -> str:
    yield codecs.decode(data, 'rot13')


class ByteableInteger(TypeConstraint):
    type_ = int
    validate = lambda x: x < 128


@handler
def i2bytes(data: [ByteableInteger, ...]) -> bytes:
    yield bytes(data)
