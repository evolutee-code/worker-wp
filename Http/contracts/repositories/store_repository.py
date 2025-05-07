from abc import abstractmethod, ABC
from typing import Iterable

from core import BaseRepository
from core.models.history_listing_model import VDHHistoryListingBase


class StoreRepoInterface(BaseRepository, ABC):
    pass
