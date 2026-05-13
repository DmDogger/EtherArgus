import pytest
from prometheus_client import CollectorRegistry

from infrastructure.metrics.prometheus_metrics_client import PrometheusMetricClient


class TestPrometheusMetricsClient:
    def test_error_counter_correctly_increment_value(
        self,
        inference_metrics_client: PrometheusMetricClient,
        metrics_registry: CollectorRegistry,
    ) -> None:

        error_amount = 5

        inference_metrics_client.set_error(error_amount)

        samples = {
            sample.name: sample.value
            for metric in metrics_registry.collect()
            for sample in metric.samples
        }

        assert any(metric == error_amount for metric in samples.values())

    def test_error_counter_increment_value_with_dunder_exit(
        self,
        inference_metrics_client: PrometheusMetricClient,
        metrics_registry: CollectorRegistry,
    ) -> None:
        with pytest.raises(ValueError):
            with inference_metrics_client:
                raise ValueError("Error errorsky")

        samples = {
            sample.name: sample.value
            for metric in metrics_registry.collect()
            for sample in metric.samples
        }

        assert samples["sample_counter_total"] >= 1
