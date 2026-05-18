from enum import Enum
from typing import TypeGuard, Sequence

import pandas as pd

from application.interfaces.feature_extraction import BuiltFeatures
from domain.events.base import DomainEvent


def from_raw_dict_to_dataframe(data: BuiltFeatures) -> pd.DataFrame:
    if not data:
        return pd.DataFrame()
    row = {k.value if isinstance(k, Enum) else str(k): v for k, v in data.items()}
    return pd.DataFrame([row])


def ensures_single_domain_event(events: object) -> TypeGuard[Sequence[DomainEvent]]:
    if not isinstance(events, (list, tuple, set)):
        return False

    for event in events:
        if not isinstance(event, DomainEvent):
            return False

    return True
