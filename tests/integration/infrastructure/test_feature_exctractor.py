import pytest

from infrastructure.feature_extractor.director_of_feature_extraction import (
    DirectorOfFeatureExtraction,
)


class TestDirectorOfFeatureExtraction:
    @pytest.mark.asyncio
    async def test_director_build_all_features_and_returns_mapping(
        self,
        make_director_of_feature_extraction,
    ) -> None:
        address = "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
        director: DirectorOfFeatureExtraction = await make_director_of_feature_extraction(
            address=address,
        )

        done_features = director()

        assert done_features is not None
