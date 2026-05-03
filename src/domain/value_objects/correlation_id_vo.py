from dataclasses import dataclass, field
from typing import final
from uuid import UUID, uuid4

from domain.exceptions.exceptions import UnsupportedCorrelationIdFormat

type CorrelationIdPrimitive = UUID | str | float | int


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CorrelationId:
    id: CorrelationIdPrimitive = field(default_factory=lambda: uuid4())

    def __post_init__(self) -> None:
        if isinstance(self.id, bool):
            raise UnsupportedCorrelationIdFormat(
                f"Correlation ID must not be bool, got: {self.id!r}"
            )
        if not isinstance(self.id, (UUID, str, int, float)):
            raise UnsupportedCorrelationIdFormat(
                f"Correlation ID must be UUID, str, int, or float, "
                f"got {type(self.id).__name__}"
            )
        if isinstance(self.id, str) and not self.id.strip():
            raise UnsupportedCorrelationIdFormat(
                "Correlation ID string must be non-empty"
            )

    @classmethod
    def create(
        cls,
        *,
        id: CorrelationIdPrimitive | None = None,
    ) -> "CorrelationId":
        if id is None:
            return cls()
        return cls(id=id)
