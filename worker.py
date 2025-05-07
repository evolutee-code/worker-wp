import traceback

from Http.dependencies.container import Container
from Http.strategies.click_submit_event import ClickSubmitEvent
from core.services.redis_cache import RedisCache
import os
import logging
import asyncio


class Worker:
    """Worker class to handle history listing processing."""

    def __init__(self, index: int, total: int):
        self.index = index
        self.total = total
        self.container = Container()
        self.cache = RedisCache()

        self.db_pool = None
        self.history_listing_service = None
        self.store_service = None

    async def startup(self):
        """Initialize dependencies and database connections."""
        self.container.mysql_connector()
        self.db_pool = await self.container.db_pool()

        history_listing_repository = self.container.history_listing_repository(db_pool=self.db_pool)
        store_repository = self.container.store_repository(db_pool=self.db_pool)

        self.history_listing_service = self.container.history_listing_service(
            history_listing_repository=history_listing_repository
        )

        self.store_service = self.container.store_service(
            store_repository=store_repository
        )

        print("✅ Worker initialized successfully")

    async def shutdown(self):
        """Cleanup resources when the worker is done."""
        mysql_connector = self.container.mysql_connector()
        if mysql_connector.pool:
            await mysql_connector.close()
            print("🔌 Database connection closed")

        await self.cache.close()
        print("🧹 Cache closed")

    async def process_task(self, store):
        logging.info(f"[Worker {self.index}] Processing task ID: {store.get('id')}")
        await asyncio.sleep(2)

        store_dict = {
            'domain': store.get('domain'),
            'username_login': store.get('username_login'),
            'password_login': store.get('password_login'),
            'history_listings': store.get('history_listing'),
        }

        await ClickSubmitEvent.process(store_dict)

    async def main(self):
        await self.startup()
        try:
            while True:
                stores = await self.store_service.get_list_stores()
                for row in stores:
                    if row['id'] % self.total != self.index:
                        continue
                    logging.info(f"[Worker is processing {row['name']}] ")
                    await self.process_task(row)
                await asyncio.sleep(3)


        except Exception as e:
            logging.exception(f"[Worker {self.index}] Exception occurred: {e}")
            print("❌ Exception:", str(e))
            traceback.print_exc()
        finally:
            await self.shutdown()


async def run_worker():
    index = int(os.environ.get("WORKER_INDEX", 0))
    total = int(os.environ.get("WORKER_TOTAL", 2))
    worker = Worker(index, total)
    await worker.main()


if __name__ == "__main__":
    import os
    import logging
    import asyncio

    log_dir = f"{os.environ.get('WORKING_DIR', 0)}/logs"
    os.makedirs(log_dir, exist_ok=True)
    # Setup logging
    log_file = os.path.join(log_dir, f"worker-{os.environ.get('WORKER_INDEX', '0')}.log")
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO
    )
    asyncio.run(run_worker())
