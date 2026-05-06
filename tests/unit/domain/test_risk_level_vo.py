import pytest

from domain.enums import RiskLevelEnum
from domain.exceptions.exceptions import InvalidRiskLevel
from domain.value_objects.risk_level import RiskLevelValueObject


class TestRiskLevelValueObject:
    def test_accepts_discrete_band_high(self) -> None:
        vo = RiskLevelValueObject.set(risk=96)

        assert vo.level == RiskLevelEnum.HIGH

    def test_rejects_band_outside_low_medium_high(self) -> None:
        with pytest.raises(InvalidRiskLevel):
            RiskLevelValueObject(level="critical")
