import os
from typing import Optional, Any, Dict, Iterable
import requests

from Http.contracts.repositories.history_listing_repository import \
    HistoryListingRepoInterface as HistoryListingRepository, HistoryListingRepoInterface
from core.models.history_listing_model import VDHHistoryListingBase

SUCCESS = 1


class HistoryListingService:
    history_listing_repo: HistoryListingRepoInterface

    def __init__(
            self,
            history_listing_repository: HistoryListingRepository,
    ):
        self.history_listing_repo = history_listing_repository

    async def get_history_listings(self) -> Iterable[VDHHistoryListingBase]:
        return await self.history_listing_repo.get_histories_not_clicked()

    async def update_clicked(self, history_id: int, status: int = SUCCESS) -> dict[str, Any]:
        url = f"{os.environ.get('DOMAIN_API')}/api/update_history/{history_id}"
        headers = {
            "Accept": "application/json"
        }

        payload = {"is_clicked_submit": status}

        response = requests.post(url, headers=headers, json=payload)
        data = []

        if response.status_code == 200:
            data = response.json()
            data = data.get('response', []).get('data', [])

        return data
