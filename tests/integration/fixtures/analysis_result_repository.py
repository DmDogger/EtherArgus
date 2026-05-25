from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from application.interfaces.analysis_result_db_mapper import AnalysisResultDBMapper
from domain.enums import RiskLevelEnum
from infrastructure.db.mappers.analysis_result_db_mapper import (
    ConcreteAnalysisResultDBMapper,
)
from infrastructure.db.repositories.analysis_result_repository import (
    SQLAlchemyCoreAnalysisResultRepository,
)
from infrastructure.db.tables.tables import analysis_result, ethereum_address, metadata

TRANSACTIONAL_SEED_WALLET_ADDRESS = "0xdadB0d80178819F2319190D340ce9A924f783711"
TRANSACTIONAL_SEED_ANALYSIS_ROW_COUNT = 2


@pytest_asyncio.fixture
async def postgres_async_engine(postgres_async_database_url: str):
    engine = create_async_engine(postgres_async_database_url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture
async def postgres_async_connection(postgres_async_engine):
    async with postgres_async_engine.connect() as connection:
        yield connection


@pytest.fixture
def analysis_result_db_mapper() -> AnalysisResultDBMapper:
    return ConcreteAnalysisResultDBMapper()


@pytest_asyncio.fixture
async def analysis_result_repository(
    postgres_async_connection: AsyncConnection,
    analysis_result_db_mapper: AnalysisResultDBMapper,
) -> SQLAlchemyCoreAnalysisResultRepository:
    return SQLAlchemyCoreAnalysisResultRepository(
        postgres_async_connection, analysis_result_db_mapper
    )


@pytest_asyncio.fixture
async def transactional_seeded_analysis_result_repository(
    postgres_async_engine,
    analysis_result_db_mapper: AnalysisResultDBMapper,
) -> SQLAlchemyCoreAnalysisResultRepository:
    wallet_id = uuid4()
    row_a_id = uuid4()
    row_b_id = uuid4()
    corr_a = uuid4()
    corr_b = uuid4()
    score_a = 0.42
    score_b = 0.75

    async with postgres_async_engine.connect() as conn:
        transaction = await conn.begin()
        try:
            await conn.execute(
                insert(ethereum_address).values(
                    id=wallet_id, wallet_address=TRANSACTIONAL_SEED_WALLET_ADDRESS
                )
            )
            await conn.execute(
                insert(analysis_result).values(
                    id=row_a_id,
                    wallet_address=TRANSACTIONAL_SEED_WALLET_ADDRESS,
                    correlation_id=corr_a,
                    level=RiskLevelEnum.LOW,
                    score=score_a,
                )
            )
            await conn.execute(
                insert(analysis_result).values(
                    id=row_b_id,
                    wallet_address=TRANSACTIONAL_SEED_WALLET_ADDRESS,
                    correlation_id=corr_b,
                    level=RiskLevelEnum.HIGH,
                    score=score_b,
                )
            )
            yield SQLAlchemyCoreAnalysisResultRepository(
                conn, analysis_result_db_mapper
            )
        finally:
            await transaction.rollback()
