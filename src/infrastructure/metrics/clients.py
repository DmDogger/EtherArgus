import contextvars
import time
from abc import ABC, abstractmethod
from typing import final, Self

from prometheus_client import Counter, Histogram


class BaseMetricClient(ABC):
    @abstractmethod
    def __enter__(self): ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb): ...


@final
class InferencePrometheusMetricClient(BaseMetricClient):
    def __init__(self, counter: Counter, histogram: Histogram):
        self._counter = counter
        self._histogram = histogram
        self._timer: contextvars.ContextVar[float] = contextvars.ContextVar("_timer")

    def __enter__(self) -> Self:
        self._timer.set(time.time())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.set_error()
        else:
            self.set_inference_latency(amount=time.time() - self._timer.get())

    def set_error(self, amount: float = 1) -> None:
        self._counter.inc(amount)

    def set_inference_latency(self, amount: float | int) -> None:
        self._histogram.observe(amount)
