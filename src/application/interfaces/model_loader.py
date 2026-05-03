from typing import Protocol, Any


class ModelLoader(Protocol):
    async def load(self) -> Any: ...
