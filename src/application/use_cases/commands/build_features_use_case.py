from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO

from application.interfaces.feature_extraction import (
    BuiltFeatures,
    FeatureExtractionDirector,
)
from application.interfaces.request_raw_features import RequestRawFeaturesUseCase
from application.interfaces.response_mapper import (
    RawResponseMapper,
)


class BuildFeaturesUseCase:
    def __init__(
        self,
        director: FeatureExtractionDirector,
        response_mapper: RawResponseMapper,
        request_raw_features_use_case: RequestRawFeaturesUseCase,
    ) -> None:
        self._request_raw_features = request_raw_features_use_case
        self._director = director
        self._mapper = response_mapper

    async def __call__(self, address: str) -> BuiltFeatures:

        response: RawEtherscanResponseDTO = await self._request_raw_features(
            address=address
        )

        normal, internal, tokens = self._mapper.map_all(response)

        built_features: BuiltFeatures = self._director.build_features(
            address=address,
            normal_transactions=normal,
            internal_transactions=internal,
            token_transfers=tokens,
        )

        return built_features
