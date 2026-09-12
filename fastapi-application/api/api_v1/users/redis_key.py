import hashlib
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession


def users_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Request | None = None,
    response: Response | None = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    exclude_types = (AsyncSession, )
    cache_kw = {}
    for name, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        cache_kw[name] = value
    cache_key = hashlib.md5( 
        f"{func.__module__}:{func.__name__}:{args}:{cache_kw}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"