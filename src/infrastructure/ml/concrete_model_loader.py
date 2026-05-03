from asyncio import TaskGroup
from typing import final

import structlog

from application.interfaces.async_executor import AsyncExecutor
from infrastructure.exceptions import ModelLoadingError
from infrastructure.ml.dto.ml_artifacts import MLArtifacts
from infrastructure.ml.model_registry import ModelRegistry

log = structlog.getLogger(__name__)


@final
class ConcreteModelLoader:
    """Loads ML artifacts from disk in parallel and assembles ``MLArtifacts``."""

    def __init__(self, async_executor: AsyncExecutor) -> None:
        """``async_executor`` runs blocking ``ModelRegistry`` loaders off the event loop."""
        self._async_executor = async_executor

    async def load(self) -> MLArtifacts:
        """Load model, scaler, imputer, and feature order concurrently.

        Returns:
            Bundled artifacts for inference.

        Raises:
            ModelLoadingError: If any loader fails (errors are aggregated from the task group).
        """
        loaders = (
            ModelRegistry.load_model_from_disk,
            ModelRegistry.load_scaler_from_disk,
            ModelRegistry.load_imputer_from_disk,
            ModelRegistry.load_feature_order_from_disk,
        )
        try:
            async with TaskGroup() as group:
                tasks = [
                    group.create_task(self._async_executor(loader))
                    for loader in loaders
                ]
            return MLArtifacts(
                model=tasks[0].result(),
                scaler=tasks[1].result(),
                imputer=tasks[2].result(),
                feature_order=tasks[3].result(),
            )
        except BaseExceptionGroup as err_gr:
            log.error(
                "Occurred unexpected error during loading ML artifacts",
                err_gr=str(err_gr.exceptions),
            )
            raise ModelLoadingError(
                f"Occurred unexpected error during loading ML artifacts: '{err_gr.exceptions}'"
            )
