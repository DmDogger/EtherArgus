import pytest_asyncio

from application.interfaces.build_features import BuildFeaturesUseCase
from application.interfaces.feature_extraction import FeatureExtractionDirector
from application.interfaces.etherscan_transactions_mapper import (
    EtherscanTransactionsMapper,
)
from application.interfaces.fraud_score_classifier import FraudScoreClassifier
from application.interfaces.response_mapper import RawResponseMapper
from application.use_cases.commands.build_features_use_case import (
    BuildFeaturesUseCase as ConcreteBuildFeaturesUseCase,
)
from application.use_cases.commands.classify_fraud_use_case import ClassifyFraudUseCase
from application.use_cases.queries.request_raw_features_use_case import (
    RequestRawFeaturesUseCase,
)
from infrastructure.ml.concrete_async_executor import ConcreteAsyncExecutor
from infrastructure.raw_response_mapper.mapper import ConcreteRawResponseMapper


@pytest_asyncio.fixture
async def request_features_use_case(etherscan_fetcher) -> RequestRawFeaturesUseCase:
    return RequestRawFeaturesUseCase(fetcher=etherscan_fetcher)


@pytest_asyncio.fixture
async def build_features_use_case(
    director_of_feature_builder: FeatureExtractionDirector,
    request_features_use_case: RequestRawFeaturesUseCase,
    etherscan_mapper: EtherscanTransactionsMapper,
) -> BuildFeaturesUseCase:
    response_mapper: RawResponseMapper = ConcreteRawResponseMapper(
        mapper=etherscan_mapper,
    )
    return ConcreteBuildFeaturesUseCase(
        director=director_of_feature_builder,
        response_mapper=response_mapper,
        request_raw_features_use_case=request_features_use_case,
    )


@pytest_asyncio.fixture
async def classify_fraud_use_case(
    fraud_score_classifier: FraudScoreClassifier,
) -> ClassifyFraudUseCase:
    return ClassifyFraudUseCase(
        async_executor=ConcreteAsyncExecutor(),
        fraud_score_classifier=fraud_score_classifier,
    )
