from enum import Enum


class ActionEnum(Enum):
    INTERNAL = "txlistinternal"
    NORMAL = "txlist"
    TOKEN = "tokentx"


class TaskStatusEnum(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    CANCELLED = "Cancelled"
