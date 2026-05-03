import pytest

from application.interfaces.model_loader import ModelLoader
from infrastructure.ml.dto.ml_artifacts import MLArtifacts


class TestModelLoader:
    @pytest.mark.asyncio
    async def test_model_loader_load_all_models_with_no_exceptions(
        self, model_loader_obj: ModelLoader
    ) -> None:
        artifacts = await model_loader_obj.load()

        assert isinstance(artifacts, MLArtifacts)
