from enum import Enum


class Status(str, Enum):
    ACTIVE = 'active'
    LIMIT = 'limit'
    PENDING = 'pending'
