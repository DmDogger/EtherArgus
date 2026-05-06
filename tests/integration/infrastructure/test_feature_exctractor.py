import pytest


class TestDirectorOfFeatureExtraction:
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Long real http request")
    async def test_director_build_all_features_and_returns_mapping(
        self,
        make_director_of_feature_extraction,
    ) -> None:
        address = "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
        director, normal, internal, tokens = await make_director_of_feature_extraction(
            address,
        )

        done_features = director.build_features(address, normal, internal, tokens)

        assert done_features is not None
