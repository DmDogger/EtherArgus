import contextvars
import time
from abc import ABC, abstractmethod
from typing import Self


class BaseMetricClient(ABC):
    def __init__(self):
        self._timer: contextvars.ContextVar[float] = contextvars.ContextVar("_timer")

    def __enter__(self) -> Self:
        when_started = time.perf_counter()
        self._timer.set(when_started)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.set_error()
        else:
            when_end =  time.perf_counter() - self._timer.get()
            self.set_latency(latency=when_end)

    @abstractmethod
    def set_latency(self, latency: float) -> None: ...

    @abstractmethod
    def set_error(self, amount: int = 1) -> None : ...


