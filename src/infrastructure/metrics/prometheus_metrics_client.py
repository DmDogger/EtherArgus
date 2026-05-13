from typing import final

from prometheus_client import Histogram, Counter

from infrastructure.metrics.base import BaseMetricClient


@final
class PrometheusMetricClient(BaseMetricClient):
    def __init__(self, counter: Counter, histogram: Histogram):
        super().__init__()
        self._counter = counter
        self._histogram = histogram

    def set_error(self, amount: int = 1, /) -> None:
        self._counter.inc(amount)

    def set_latency(self, latency: float | int) -> None:
        self._histogram.observe(latency)
