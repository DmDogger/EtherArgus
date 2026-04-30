from copy import copy
from typing import Self, TypedDict, Literal

from config.etherscan import etherscan_settings
from infrastructure.etherscan_fetcher.enums import ActionEnum


class QueryDict(TypedDict, total=False):
    apikey: str
    chainid: str
    module: str
    action: Literal[ActionEnum.NORMAL, ActionEnum.INTERNAL, ActionEnum.TOKEN]
    address: str
    startblock: int
    endblock: int
    page: int
    offset: int
    sort: str


class EtherscanQueryBuilder:
    """A builder pattern for construction a http request"""

    _query: QueryDict

    def __init__(self):
        self._query = {"apikey": etherscan_settings.api_key_etherscan, "chainid": "1"}

    def address(self, address: str) -> Self:
        self._query["address"] = address
        return self

    def module(self, module: str) -> Self:
        self._query["module"] = module
        return self

    def action(self, action: ActionEnum) -> Self:
        self._query["action"] = action.value
        return self

    def start_block(self, start: int = 1) -> Self:
        self._query["startblock"] = start
        return self

    def end_block(self, end: int) -> Self:
        self._query["endblock"] = end
        return self

    def page(self, page: int = 1) -> Self:
        self._query["page"] = page
        return self

    def offset(self, offset: int) -> Self:
        self._query["offset"] = offset
        return self

    def sort(self, sort: Literal["asc", "desc"] = "desc") -> Self:
        self._query["sort"] = sort
        return self

    def build(self) -> QueryDict:
        return copy(self._query)
