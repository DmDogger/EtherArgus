from typing import Protocol

from application.interfaces.http_client import RequestParams


class QueryDirector(Protocol):
    def build_transactions(self, *, address: str) -> RequestParams: ...

    def build_internal_transactions(self, *, address: str) -> RequestParams: ...

    def build_token_transfers(self, *, address: str) -> RequestParams: ...
