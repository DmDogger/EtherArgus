from typing import final

from application.dto.raw_etherscan_response_dto import RawEtherscanResponseDTO
from application.interfaces.etherscan.etherscan_transactions_mapper import (
    EtherscanTransactionsMapper,
)
from application.interfaces.etherscan.response_mapper import TransactionsSequence


@final
class ConcreteRawResponseMapper:
    def __init__(self, mapper: EtherscanTransactionsMapper):
        self._mapper = mapper

    def map_all(self, raw_response: RawEtherscanResponseDTO) -> TransactionsSequence:
        normal = self._mapper.from_raw_normal_transactions(raw_response)
        internal = self._mapper.from_raw_internal_transactions(raw_response)
        token_transfers = self._mapper.from_raw_token_transfers(raw_response)
        return normal, internal, token_transfers
