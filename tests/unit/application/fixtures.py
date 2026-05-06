from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from application.interfaces.feature_extraction import BuiltFeatures
from application.use_cases.commands.analyze_address_use_case import (
    AnalyzeAddressUseCase,
)
from application.use_cases.commands.save_analysis_results_use_case import (
    SaveAnalysisResultsUseCase,
)
from domain.entities.analysis_result import AnalysisResult
from domain.events.address_analyzed import AddressAnalyzed
from domain.value_objects.risk_score_vo import RiskScoreValueObject


def _repository_mock() -> AsyncMock:
    repo = AsyncMock()
    repo.save = AsyncMock(side_effect=lambda entity: entity)
    repo.update = AsyncMock(side_effect=lambda entity: entity)
    repo.get_by_id = AsyncMock(return_value=None)
    return repo


@pytest.fixture
def sample_eth_address() -> str:
    return "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"


@pytest.fixture
def built_features_stub() -> BuiltFeatures:
    return {}


@pytest.fixture
def risk_score_stub() -> RiskScoreValueObject:
    return RiskScoreValueObject.create(score=0.37)


@pytest.fixture
def mock_results_repository() -> AsyncMock:
    return _repository_mock()


@pytest.fixture
def mock_outbox_repository() -> AsyncMock:
    return _repository_mock()


@pytest.fixture
def mock_uow() -> AsyncMock:
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = None
    return uow


@pytest.fixture
def mock_build_features_use_case(built_features_stub: BuiltFeatures) -> AsyncMock:
    use_case = AsyncMock()
    use_case.return_value = built_features_stub
    return use_case


@pytest.fixture
def mock_classify_fraud_use_case(risk_score_stub: RiskScoreValueObject) -> AsyncMock:
    use_case = AsyncMock()
    use_case.return_value = risk_score_stub
    return use_case


@pytest.fixture
def mock_save_analysis_results_use_case() -> AsyncMock:
    use_case = AsyncMock()
    use_case.return_value = None
    return use_case


@pytest.fixture
def analyze_address_use_case(
    mock_save_analysis_results_use_case: AsyncMock,
    mock_build_features_use_case: AsyncMock,
    mock_classify_fraud_use_case: AsyncMock,
) -> AnalyzeAddressUseCase:
    return AnalyzeAddressUseCase(
        save_analysis_results_use_case=mock_save_analysis_results_use_case,
        build_features_use_case=mock_build_features_use_case,
        classify_fraud_use_case=mock_classify_fraud_use_case,
    )


@pytest.fixture
def save_results_use_case(
    mock_results_repository: AsyncMock,
    mock_outbox_repository: AsyncMock,
    mock_uow: AsyncMock,
) -> SaveAnalysisResultsUseCase:
    return SaveAnalysisResultsUseCase(
        uow=mock_uow,
        results_repository=mock_results_repository,
        outbox_repository=mock_outbox_repository,
    )


@pytest.fixture
def analysis_result_obj(sample_eth_address: str) -> AnalysisResult:
    a_result = AnalysisResult.create(
        event_class=AddressAnalyzed,
        address=sample_eth_address,
        score=RiskScoreValueObject.create(score=0.9),
    )
    return a_result
