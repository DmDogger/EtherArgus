from typing import Callable

from domain.entities.analysis_result import AnalysisResult
from domain.events.analysis_requested_event import AnalysisRequestedEvent
from domain.events.base import DomainEvent


class TestAnalysisResult:
    def test_factory_returns_analysis_result_aggregate(
        self, create_analysis_result: Callable[[type[DomainEvent]], AnalysisResult]
    ) -> None:
        analysis_result = create_analysis_result(AnalysisRequestedEvent)

        assert isinstance(analysis_result, AnalysisResult)

    def test_after_create_one_pending_event_in_queue(
        self, create_analysis_result: Callable[[type[DomainEvent]], AnalysisResult]
    ) -> None:
        analysis_result = create_analysis_result(AnalysisRequestedEvent)

        events = analysis_result.pop_events()

        assert len(events) == 1

    def test_second_pop_events_returns_no_events(
        self, create_analysis_result: Callable[[type[DomainEvent]], AnalysisResult]
    ) -> None:
        analysis_result = create_analysis_result(AnalysisRequestedEvent)

        analysis_result.pop_events()
        events = analysis_result.pop_events()

        assert not events

    def test_pending_event_runtime_type_is_passed_event_class(
        self, create_analysis_result: Callable[[type[DomainEvent]], AnalysisResult]
    ) -> None:
        analysis_result = create_analysis_result(AnalysisRequestedEvent)

        events = analysis_result.pop_events()

        assert all(isinstance(event, AnalysisRequestedEvent) for event in events)

    def test_event_requested_to_equals_aggregate_address(
        self, create_analysis_result: Callable[[type[DomainEvent]], AnalysisResult]
    ) -> None:
        analysis_result = create_analysis_result(AnalysisRequestedEvent)

        events = analysis_result.pop_events()

        assert all(event.requested_to == analysis_result.address for event in events)

    def test_event_aggregate_type_matches_aggregate_root_class_name(
        self, create_analysis_result: Callable[[type[DomainEvent]], AnalysisResult]
    ) -> None:
        analysis_result = create_analysis_result(AnalysisRequestedEvent)

        events = analysis_result.pop_events()

        assert all(
            analysis_result.aggregate_type == event.aggregate_type for event in events
        )
