import httpx


def _patch_httpx():  # type: ignore
    """Monkey-patch httpx so that we can use our own json ser/des.

    https://github.com/encode/httpx/issues/717
    """
    from httpx._content import Any, ByteStream

    def encode_json(json: Any) -> tuple[dict[str, str], ByteStream]:
        # body = json if isinstance(json, bytes) else json_dumps(json).encode("utf-8") # Not used for this project
        return {"Content-Length": str(len(json)), "Content-Type": "application/json"}, ByteStream(json)

    # This makes the above function look and act like the original.
    encode_json.__globals__.update(httpx._content.__dict__)
    encode_json.__module__ = httpx._content.__name__
    httpx._content.encode_json = encode_json
