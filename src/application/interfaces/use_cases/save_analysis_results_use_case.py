from domain.entities.analysis_result import AnalysisResult


class SaveAnalysisResultsUseCase:
    async def __call__(self, analysis_result: AnalysisResult) -> None: ...
