import abc
import asyncio
import datetime
import functools
from typing import Any
from croniter import croniter
from ..utils.datetime.helper import datetime_now


def is_async_callable(obj: Any) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func

    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )


class CacheInit(abc.ABC):  # pragma: no cover
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def croniter_str_to_seconds(
        self, croniter_string: str, from_datetime: datetime.datetime | None = None
    ) -> int:
        runtime_now = datetime_now()
        croniter_iter = croniter(croniter_string, (from_datetime or runtime_now))
        next_time: datetime.datetime = croniter_iter.get_next(datetime.datetime)
        return (next_time - (from_datetime or runtime_now)).seconds

    @abc.abstractmethod
    async def initialize(self, *args, **kwargs):
        """服務開始時 初始化 快取服務"""
        raise NotImplementedError

    @abc.abstractmethod
    async def finalize(self, *args, **kwargs):
        """服務結束時 關閉/結束 快取服務"""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self):
        """服務結束時 刪除 快取服務內容"""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self):
        """取得 快取服務內 所有內容 盡力取得 key-value 最差只有 key"""
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, key: str) -> Any | None:
        """取得 該key 對應的 value"""
        raise NotImplementedError

    @abc.abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        expire: int | str | None = None,
    ) -> None:
        """設定 該key 對應的 value"""
        raise NotImplementedError

    @abc.abstractmethod
    async def clear(
        self,
        key: str | None = None,
        startswith_like: str | None = None,
    ):
        """主動 清除該key 對應的 value，支援多key(startswith) 刪除"""
        raise NotImplementedError

    @abc.abstractmethod
    async def test(self):
        """測試服務是否正常"""
        raise NotImplementedError

    @classmethod
    def cache(cls, key: str | None = None, expire: str | int | None = None):
        """

        Args:
            key: cache 過期時間
            expire: 過期時間 支援 n秒後過期、cron

        Returns:

        """

        def decorator(func):
            async def wrapper(*args, **kwargs):
                cache = cls()
                cache_key = key
                if cache_key is None:
                    func_name = func.__name__
                    cache_key = f"func_{func_name}"

                if (result := await cache.get(cache_key)) is None:
                    if is_async_callable(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    await cache.set(cache_key, result, expire=expire)
                    return result
                return result

            return wrapper

        return decorator
