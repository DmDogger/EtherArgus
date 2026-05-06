import pytest

from application.interfaces.repository import Repository
from application.interfaces.uow import UnitOfWork
from application.use_cases.commands.save_analysis_results_use_case import (
    SaveAnalysisResultsUseCase,
)
from domain.entities.analysis_result import AnalysisResult


class TestSaveAnalysisResultsUseCaseUnit:
    @pytest.mark.asyncio
    async def test_outbox_repository_called_once(
        self,
        analysis_result_obj: AnalysisResult,
        mock_outbox_repository: Repository,
        save_results_use_case: SaveAnalysisResultsUseCase,
    ) -> None:

        await save_results_use_case(analysis_result=analysis_result_obj)

        mock_outbox_repository.save.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_uow_context_manager_was_opened(
        self,
        analysis_result_obj: AnalysisResult,
        mock_uow: UnitOfWork,
        save_results_use_case: SaveAnalysisResultsUseCase,
    ) -> None:

        await save_results_use_case(analysis_result=analysis_result_obj)

        mock_uow.__aenter__.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_uow_context_manager_was_closed(
        self,
        analysis_result_obj: AnalysisResult,
        mock_uow: UnitOfWork,
        save_results_use_case: SaveAnalysisResultsUseCase,
    ) -> None:

        await save_results_use_case(analysis_result=analysis_result_obj)

        mock_uow.__aexit__.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_results_repository_save_results(
        self,
        analysis_result_obj: AnalysisResult,
        mock_results_repository: Repository,
        save_results_use_case: SaveAnalysisResultsUseCase,
    ) -> None:

        await save_results_use_case(analysis_result=analysis_result_obj)

        mock_results_repository.save.assert_awaited_once_with(analysis_result_obj)
