from dataclasses import field
from typing import final
from uuid import UUID, uuid4

from domain.exceptions.exceptions import UnsupportedCorrelationIdFormat

type CorrelationId = UUID | str | float | int


@final
class CorrelationId:
    id: CorrelationId = field(default_factory=lambda: uuid4())

    def __post_init__(self):
        if not isinstance(self.id, CorrelationId):
            raise UnsupportedCorrelationIdFormat(
                f"Correlation ID should be an instance of these types: '{CorrelationId}'\n"
                f"But got: {self.id}"
            )
