from enum import Enum

import pandas as pd

from application.interfaces.feature_extraction import BuiltFeatures


def from_raw_dict_to_dataframe(data: BuiltFeatures) -> pd.DataFrame:
    if not data:
        return pd.DataFrame()
    row = {k.value if isinstance(k, Enum) else str(k): v for k, v in data.items()}
    return pd.DataFrame([row])
