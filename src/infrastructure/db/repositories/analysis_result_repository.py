from dataclasses import asdict
from typing import Mapping, Any

import structlog
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from application.interfaces.analysis_result_db_mapper import AnalysisResultDBMapper
from domain.entities.analysis_result import AnalysisResult
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject
from infrastructure.db.tables.tables import analysis_result, ethereum_address


log = structlog.getLogger(__name__)


class SQLAlchemyCoreAnalysisResultRepository:
    def __init__(self, connection: AsyncConnection, mapper: AnalysisResultDBMapper):
        self._connection = connection
        self._mapper = mapper

    async def get_by_address(
        self, address: EthereumAddressValueObject
    ) -> list[AnalysisResult] | None:
        cursor_result_obj = await self._connection.execute(
            select(
                analysis_result,
                ethereum_address.c.wallet_address.label("ethereum_address"),
            )
            .join(
                ethereum_address,
                ethereum_address.c.wallet_address == analysis_result.c.wallet_address,  # type: ignore
            )
            .where(ethereum_address.c.wallet_address == address.wallet_address)
        )

        raw_mappings_data = cursor_result_obj.mappings().all()

        if raw_mappings_data:
            mapped_aggregates = [
                self._mapper.to_aggregate(value) for value in raw_mappings_data
            ]
            return mapped_aggregates
        else:
            log.warning(
                "Got no results for this address", address=address.wallet_address
            )
            return None

    async def upsert(self, entity: AnalysisResult) -> None:
        eth_address_db_entity: Mapping[str, Any] = self._mapper.to_db_rows(
            entity=entity
        )

        await self._connection.execute(
            insert(ethereum_address)
            .values(**asdict(entity.address))
            .on_conflict_do_nothing()
        )

        await self._connection.execute(
            insert(analysis_result)
            .values(eth_address_db_entity)
            .on_conflict_do_nothing()
        )
