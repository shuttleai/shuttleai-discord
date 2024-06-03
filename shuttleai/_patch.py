import httpx


def _patch_httpx():  # type: ignore
    """
    Monkey-patch httpx to accept direct bytes (orjson.dumps) directly.
    Originally from
    - https://github.com/encode/httpx/issues/717
    But modified to be faster for ShuttleAI's specific use case.
    Do not use this patch outside of ShuttleAI if you don't know what you're doing.
    """
    from httpx._content import Any, ByteStream

    def encode_json(json: Any) -> tuple[dict[str, str], ByteStream]:
        return {
            "Content-Length": str(len(json)),
            "Content-Type": "application/json",
        }, ByteStream(json)

    # This makes the above function look and act like the original.
    encode_json.__globals__.update(httpx._content.__dict__)
    encode_json.__module__ = httpx._content.__name__
    httpx._content.encode_json = encode_json
