from application.interfaces.repository import Repository
from application.interfaces.uow import UnitOfWork
from domain.entities.analysis_result import AnalysisResult


class SaveAnalysisResultsUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        outbox_repository: Repository,
        results_repository: Repository,
    ):
        self._uow = uow
        self._outbox_repository = outbox_repository
        self._results_repository = results_repository

    async def __call__(self, analysis_result: AnalysisResult) -> None:
        async with self._uow:
            events = analysis_result.pop_events()

            await self._results_repository.save(analysis_result)
            for event in events:
                # Saving events synchronously as we use one transaction in UoW.
                await self._outbox_repository.save(event)
