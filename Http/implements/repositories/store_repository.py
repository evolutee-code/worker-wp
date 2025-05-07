from typing import Iterable

from Http.contracts.repositories.store_repository import \
    StoreRepoInterface as StoreRepositoryContract
from core.models.store_model import VDHStoreBase


class StoreRepository(StoreRepositoryContract):
    def __init__(self, db_pool):
        super().__init__(table_name="vdh_stores", db_pool=db_pool, model=VDHStoreBase)
