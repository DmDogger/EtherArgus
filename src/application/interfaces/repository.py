from typing import Protocol, TypeVar
from uuid import UUID

T = TypeVar("T")


class Repository(Protocol[T]):
    async def save(self, entity: T) -> T: ...
    async def update(self, entity: T) -> T: ...
    async def get_by_id(self, id_: UUID) -> T | None: ...
