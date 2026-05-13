from infrastructure.etherscan.building.etherscan_query_builder import (
    EtherscanQueryBuilder,
    QueryDict,
)
from infrastructure.etherscan.enums import ModuleEnum, ActionEnum


class EtherscanQueryDirector:
    def build_transactions(self, *, address: str) -> QueryDict:
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.NORMAL)
            .module(module=ModuleEnum.ACCOUNT)
            .page()
            .sort()
            .build()
        )

        return query

    def build_internal_transactions(self, *, address: str) -> QueryDict:
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.INTERNAL)
            .module(module=ModuleEnum.ACCOUNT)
            .page()
            .sort()
            .build()
        )

        return query

    def build_token_transfers(self, *, address: str) -> QueryDict:
        query: QueryDict = (
            EtherscanQueryBuilder()
            .address(address=address)
            .action(action=ActionEnum.TOKEN)
            .module(module=ModuleEnum.ACCOUNT)
            .page()
            .sort()
            .build()
        )

        return query
