from dataclasses import dataclass

from domain.events.base import DomainEvent
from domain.value_objects.correlation_id_vo import CorrelationId
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject


@dataclass(slots=True)
class AddressAnalyzed(DomainEvent):
    correlation_id: CorrelationId
    requested_to: EthereumAddressValueObject
