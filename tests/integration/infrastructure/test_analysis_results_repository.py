import pytest

from domain.entities.analysis_result import AnalysisResult
from domain.value_objects.ethereum_address_vo import EthereumAddressValueObject
from infrastructure.db.repositories.analysis_result_repository import (
    SQLAlchemyCoreAnalysisResultRepository,
)
from tests.integration.fixtures.analysis_result_repository import (
    TRANSACTIONAL_SEED_WALLET_ADDRESS,
)


class TestSQLAlchemyCoreAnalysisResultsRepository:
    @pytest.mark.asyncio
    async def test_get_by_wallet_address_joins_tables_and_returns_result(
        self,
        transactional_seeded_analysis_result_repository: SQLAlchemyCoreAnalysisResultRepository,
    ) -> None:

        some_records = (
            await transactional_seeded_analysis_result_repository.get_by_address(
                address=EthereumAddressValueObject.create(
                    address=TRANSACTIONAL_SEED_WALLET_ADDRESS
                ),
            )
        )

        assert all(isinstance(record, AnalysisResult) for record in some_records)

    @pytest.mark.asyncio
    async def test_method_returns_none_if_nothing_found(
        self,
        ethereum_address: str,
        transactional_seeded_analysis_result_repository: SQLAlchemyCoreAnalysisResultRepository,
    ) -> None:
        # We need to change address as we use seeded values and if we put default address
        # repository will find values, but not none.
        # just using two pointers.
        def _transform_default_address():
            add = list(ethereum_address)
            left, right = 2, len(add) - 1

            while left <= right:
                temp = add[left]
                add[left] = add[right]
                add[right] = temp
                left += 1
                right -= 1
            return "".join(add)

        nothing = await transactional_seeded_analysis_result_repository.get_by_address(
            address=EthereumAddressValueObject.create(
                address=_transform_default_address(),
            )
        )

        assert nothing is None

    @pytest.mark.asyncio
    async def test_upserts_correctly(
        self,
        analysis_result_obj: AnalysisResult,
        analysis_result_repository: SQLAlchemyCoreAnalysisResultRepository,
    ) -> None:

        await analysis_result_repository.save(analysis_result_obj)

        entities = await analysis_result_repository.get_by_address(
            address=analysis_result_obj.address
        )

        assert all(isinstance(entity, AnalysisResult) for entity in entities)
