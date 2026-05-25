from datetime import UTC
from decimal import Decimal
from typing import Mapping
from uuid import UUID

from domain.entities.analysis_result import AnalysisResult
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject
from domain.value_objects.risk_level import RiskLevelValueObject
from domain.value_objects.risk_score_vo import RiskScoreValueObject

type ScoreValues = Decimal | float


class ConcreteAnalysisResultDBMapper:
    def to_aggregate(
        self, values: Mapping[str, str | UUID | ScoreValues]
    ) -> AnalysisResult:
        return AnalysisResult(
            id=values["id"],
            address=EthereumAddressValueObject(
                wallet_address=values["ethereum_address"]
            ),
            score=RiskScoreValueObject.create(score=values["score"]),
            level=RiskLevelValueObject(level=values["level"]),
        )

    def to_db_rows(self, entity: AnalysisResult) -> Mapping[str, str]:
        return {
            "id": entity.id,
            "wallet_address": entity.address.wallet_address,
            "correlation_id": entity.id,
            "level": entity.level.level,
            "score": entity.score.value,
            "processed_at": entity.processed_at.replace(tzinfo=UTC),
        }
