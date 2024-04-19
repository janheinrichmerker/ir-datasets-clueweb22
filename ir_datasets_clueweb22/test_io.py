from io import BytesIO

from ir_datasets_clueweb22.io import OffsetIOWrapper


def test_offset_io_wrapper() -> None:
    alphabet = b"abcdefghijklmnopqrstuvwxyz"
    alphabet_offset = alphabet[0:1] + alphabet[4:6] + alphabet[10:]

    alphabet_io = BytesIO(alphabet)
    alphabet_offset_io = OffsetIOWrapper(
        alphabet_io,
        [
            (0, 1),
            (4, 6),
            (10, -1),
        ]
    )

    assert alphabet_offset_io.read() == alphabet_offset
