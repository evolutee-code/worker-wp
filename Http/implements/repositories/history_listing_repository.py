from typing import Iterable

from Http.contracts.repositories.history_listing_repository import \
    HistoryListingRepoInterface as HistoryListingRepositoryContract
from core.models.history_listing_model import VDHHistoryListingBase


class HistoryListingRepository(HistoryListingRepositoryContract):
    def __init__(self, db_pool):
        super().__init__(table_name="vdh_history_listing", db_pool=db_pool, model=VDHHistoryListingBase)

    async def get_histories_not_clicked(self) -> Iterable[VDHHistoryListingBase]:
        return await self.list_alls(
            filter_query={
                "status": 2,
                'is_clicked_submit': 0,
                # 'product_wp_id__isnull': False
            },
            fields_limit=[
                'id',
                'store_id',
                'is_clicked_submit',
                'product_wp_id',
            ]
        )
