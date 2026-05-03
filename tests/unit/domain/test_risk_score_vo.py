import pytest

from domain.exceptions.exceptions import InvalidRiskScore
from domain.value_objects.risk_score_vo import RiskScoreValueObject


class TestRiskScoreValueObject:
    def test_accepts_score_on_closed_unit_interval(self) -> None:
        vo = RiskScoreValueObject.create(score=0.5)

        assert vo.score == 0.5

    def test_rejects_score_strictly_below_zero(self) -> None:
        with pytest.raises(InvalidRiskScore):
            RiskScoreValueObject.create(score=-0.01)

    def test_rejects_score_strictly_above_one(self) -> None:
        with pytest.raises(InvalidRiskScore):
            RiskScoreValueObject.create(score=1.01)
