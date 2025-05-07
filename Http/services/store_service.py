import os
from typing import Optional, Any, Dict, Iterable
import requests
from Http.contracts.repositories.store_repository import \
    StoreRepoInterface as StoreRepository, StoreRepoInterface


class StoreService:
    store_repo: StoreRepoInterface

    def __init__(
            self,
            store_repository: StoreRepository,
    ):
        self.store_repo = store_repository

    async def get_list_stores(self) -> dict[str, Any]:
        url = f"{os.environ.get('DOMAIN_API')}/api/stores"
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        data = []
        if response.status_code == 200:
            data = response.json()
            data = data.get('response', []).get('data', [])
        return data
