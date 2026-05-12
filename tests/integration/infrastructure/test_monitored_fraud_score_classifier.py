from decimal import Decimal
from typing import Mapping

import pytest
from prometheus_client import CollectorRegistry

from infrastructure.feature_extraction.enums import FeaturesEnum
from infrastructure.ml.fraud_score_classifier import MonitoredFraudScoreClassifier


class TestMonitoredFraudScoreClassifier:
    def test_predict_observes_latency_histogram_on_success(
        self,
        metrics_registry: CollectorRegistry,
        built_features_random: Mapping[FeaturesEnum, Decimal],
        monitored_fraud_score_classifier: MonitoredFraudScoreClassifier,
    ) -> None:
        monitored_fraud_score_classifier.predict(built_features_random)

        samples = {
            sample.name: sample.value
            for metric in metrics_registry.collect()
            for sample in metric.samples
        }

        assert samples["sample_histogram_sum"] > 0.0


    def test_predict_increments_error_counter_when_classifier_raises(
        self,
        metrics_registry: CollectorRegistry,
        monitored_fraud_score_classifier: MonitoredFraudScoreClassifier,
    ) -> None:
        with pytest.raises(Exception):
            monitored_fraud_score_classifier.predict("Invalid args.")

        samples = {
            sample.name: sample.value
            for metric in metrics_registry.collect()
            for sample in metric.samples
        }

        assert samples["sample_counter_total"] >= 1
