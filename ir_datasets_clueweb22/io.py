from io import BytesIO, UnsupportedOperation
from itertools import tee, chain
from types import TracebackType
from typing import (
    IO, Iterable, Iterator, Optional, Tuple, Sequence, Type, TypeVar,
    Container, List
)
from typing_extensions import Buffer

_OffsetIOWrapperSelf = TypeVar("_OffsetIOWrapperSelf", bound="OffsetIOWrapper")


class OffsetIOWrapper(IO[bytes]):
    """
    Basic read-only file wrapper to read a file's content
    only inside specific offset ranges.

    For example, if multiple files are concatenated on disk,
    we can access specific subsets of these files without reading
    the others from disk.

    File positions outside the specified ranges are automatically skipped
    by seeking to the next offset.
    """
    _file: IO[bytes]
    _file_position: int = 0
    _offset_ranges: Sequence[Tuple[int, int]]
    _offset_range_position: int = 0

    def __init__(
            self,
            file: IO[bytes],
            offset_ranges: Sequence[Tuple[int, int]],
    ) -> None:
        self._file = file
        self._offset_ranges = offset_ranges

    @classmethod
    def from_offsets(
            cls: Type[_OffsetIOWrapperSelf],
            file: IO[bytes],
            offsets: Iterator[int],
            indices: Container[int],
    ) -> _OffsetIOWrapperSelf:
        # Create start and end offset iterators by copying
        # the original offsets iterator and shifting the end offset iterator
        # so that it points to the next index's start
        # (i.e., the current index end offset + 1).
        offsets_start, offsets_end = tee(offsets)
        next(offsets_end, None)  # Remove first.
        offsets_end = chain(offsets_end, (-1,))  # Append empty offset (-1).

        # Combine offsets to offset ranges.
        offset_ranges: Iterable[tuple[int, int]] = zip(
            offsets_start, offsets_end)

        # Create sequence of offset ranges, sorted by start offset.
        offset_ranges = sorted((
            offset_range
            for index, offset_range in enumerate(offset_ranges)
            if index in indices
        ), key=lambda offset_range: offset_range[0])
        return cls(file, offset_ranges)

    def close(self) -> None:
        self._file.close()

    def fileno(self) -> int:
        return self._file.fileno()

    def flush(self) -> None:
        self._file.flush()

    def isatty(self) -> bool:
        return self._file.isatty()

    def read(self, n: int = -1) -> bytes:
        with BytesIO() as buffer:
            while (n != 0 and
                   self._offset_range_position < len(self._offset_ranges)):
                offset_range = self._offset_ranges[self._offset_range_position]
                offset_start, offset_end = offset_range
                offset_n: int
                if offset_end >= 0:
                    offset_n = offset_end - offset_start
                    if self._file_position > offset_start:
                        offset_n -= self._file_position - offset_start
                else:
                    offset_n = -1

                # Advance to current offset range.
                if self._file_position < offset_start:
                    self._file.seek(offset_start)
                    self._file_position = offset_start

                # Do not read more bytes than in the current offset range.
                max_n: int
                if n >= 0 and offset_n >= 0:
                    max_n = min(n, offset_n)
                elif offset_n >= 0:
                    max_n = offset_n
                else:
                    max_n = n

                # Read from offset and advance position.
                current = self._file.read(max_n)
                buffer.write(current)
                current_len = len(current)
                if n >= 0:
                    n = max(n - current_len, 0)
                self._file_position += current_len

                # Current offset is exhausted. Advance to next offset.
                if (n != 0 and (
                        offset_end is None or self._file_position >= offset_end
                )):
                    self._offset_range_position += 1
            result = buffer.getvalue()
        return result

    def readable(self) -> bool:
        return self._file.readable()

    def readline(self, limit: int = -1) -> bytes:
        raise UnsupportedOperation()

    def readlines(self, hint: int = -1) -> List[bytes]:
        raise UnsupportedOperation()

    def seek(self, offset: int, whence: int = 0) -> int:
        raise UnsupportedOperation()

    def seekable(self) -> bool:
        return False

    def tell(self) -> int:
        raise UnsupportedOperation()

    def truncate(self, _size: Optional[int] = None) -> int:
        raise UnsupportedOperation()

    def writable(self) -> bool:
        return False

    def write(self, _s: Buffer | bytes) -> int:
        raise UnsupportedOperation()

    def writelines(self, _lines: Iterable[Buffer] | Iterable[bytes]) -> None:
        raise UnsupportedOperation()

    def __next__(self) -> bytes:
        raise UnsupportedOperation()

    def __iter__(self) -> Iterator[bytes]:
        raise UnsupportedOperation()

    def __enter__(self) -> IO[bytes]:
        return self

    def __exit__(
            self,
            type_: Optional[Type[BaseException]],
            value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> None:
        self.close()
        return None
