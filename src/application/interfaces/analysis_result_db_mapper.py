from datetime import datetime
from decimal import Decimal
from typing import Mapping, Protocol
from uuid import UUID

from domain.entities.analysis_result import AnalysisResult

type DbScalar = str | UUID | Decimal | float | datetime


class AnalysisResultDBMapper(Protocol):
    def to_aggregate(self, values: Mapping[str, DbScalar]) -> AnalysisResult: ...
    def to_db_rows(self, entity: AnalysisResult) -> Mapping[str, str]: ...
