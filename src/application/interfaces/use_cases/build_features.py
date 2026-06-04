from typing import Protocol

from application.interfaces.features.feature_extraction import BuiltFeatures


class BuildFeaturesUseCase(Protocol):
    async def __call__(self, address: str) -> BuiltFeatures: ...
