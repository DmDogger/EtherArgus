from dataclasses import dataclass
from typing import final

from domain.events.base import DomainEvent
from domain.value_objects.correlation_id_vo import CorrelationId
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject


@final
@dataclass(slots=True)
class AnalysisRequestedEvent(DomainEvent):
    correlation_id: CorrelationId
    requested_to: EthereumAddressValueObject
