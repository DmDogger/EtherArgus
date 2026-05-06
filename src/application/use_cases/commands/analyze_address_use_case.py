import structlog

from application.exceptions.exceptions import BuildFeaturesError, AnalysisRequestFailed
from application.interfaces.build_features import BuildFeaturesUseCase
from application.interfaces.classify_fraud_use_case import ClassifyFraudUseCase
from application.interfaces.feature_extraction import BuiltFeatures
from application.interfaces.save_analysis_results_use_case import SaveAnalysisResultsUseCase
from domain.entities.analysis_result import AnalysisResult
from domain.events.address_analyzed import AddressAnalyzed
from domain.exceptions.exceptions import DomainValidationError
from domain.value_objects.risk_score_vo import RiskScoreValueObject

log = structlog.getLogger(__name__)


class AnalyzeAddressUseCase:
    def __init__(
        self,
        save_analysis_results_use_case: SaveAnalysisResultsUseCase,
        build_features_use_case: BuildFeaturesUseCase,
        classify_fraud_use_case: ClassifyFraudUseCase,
    ):
        self._save_analysis_results_use_case = save_analysis_results_use_case
        self._build_features_use_case = build_features_use_case
        self._fraud_score_classifier = classify_fraud_use_case


    async def __call__(self, address: str) -> None:
        try:

            built_features: BuiltFeatures = await self._build_features_use_case(
                address=address
            )

            risk_score: RiskScoreValueObject = await self._fraud_score_classifier(
                built_features
            )

            analysis_result = AnalysisResult.create(
                event_class=AddressAnalyzed, address=address, score=risk_score
            )

            await self._save_analysis_results_use_case(analysis_result)

        except DomainValidationError as err:
            log.error("Occurred domain validation error", err=str(err))
            raise AnalysisRequestFailed(
                "Analysis request failed."
                "Seems you have violated domain validation"
                f"Error: {err}"
            )
        except BuildFeaturesError as err:
            log.error("Occurred build features error", err=str(err))
            raise
