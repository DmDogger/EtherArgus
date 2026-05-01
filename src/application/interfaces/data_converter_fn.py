from __future__ import annotations

from typing import Protocol

import pandas as pd

from application.interfaces.feature_extraction import BuiltFeatures


class FromRawDictToDataFrame(Protocol):
    def __call__(self, data: BuiltFeatures) -> pd.DataFrame: ...
