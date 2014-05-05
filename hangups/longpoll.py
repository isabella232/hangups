"""Parser for long-polling responses from the talkgadget API."""

from hangups import javascript


def loads(f):
    """Parse long poll response into a list of objects.

    Supports unseekable streams.

    Raises ValueError if the stream cannot be parsed.

    f must be a binary file-like object.
    """
    msgs = []
    while True:
        c = f.read(1)
        if len(c) == 1:
            msg_len = _read_int(f, already_read=c)
            msg_str = f.read(msg_len)
            if len(msg_str) < msg_len:
                raise ValueError("Unexpected EOF while parsing message")
            msgs.append(javascript.loads(msg_str.decode()))
        else:
            return msgs


def _read_int(f, already_read=''):
    """Read characters until newline is reached and return integer."""
    len_str = already_read
    while True:
        c = f.read(1)
        if c == b'\n':
            break
        elif len(c) == 0:
            raise ValueError("Unexpected EOF while parsing message length")
        else:
            len_str = len_str + c
    try:
        return int(len_str)
    except ValueError:
        raise ValueError("Malformed message length")