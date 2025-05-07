from abc import abstractmethod, ABC
from typing import Iterable

from core import BaseRepository
from core.models.history_listing_model import VDHHistoryListingBase


class HistoryListingRepoInterface(BaseRepository, ABC):
    async def get_histories_not_clicked(self) -> Iterable[VDHHistoryListingBase]:
        ...
