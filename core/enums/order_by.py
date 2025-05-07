from enum import Enum


class OrderBy(str, Enum):
    INCREASE = "asc"
    DECREASE = "desc"