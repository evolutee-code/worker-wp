import asyncio
import traceback

from playwright.async_api import async_playwright

from Http.browser import BrowserManager
from Http.dependencies.container import Container

PROCESSING = 2
ERROR = 3


class ClickSubmitEvent:
    def __init__(self, store_dict):
        self.store_dict = store_dict
        self.items = store_dict['history_listings']
        self.domain_url = f"{store_dict['domain']}/wp-admin"
        self.product_url = f"{store_dict['domain']}/wp-admin/post.php?post=product_id&action=edit"
        self.browser_manager = None
        self.browser = None
        self.page = None
        self.container = Container()
        self.history_listing_service = None
        self.db_pool = None

    @classmethod
    async def process(cls, store_dict):
        processor = cls(store_dict)
        await processor.init_pool()

        return await processor._process_images()

    async def init_pool(self):
        self.container.mysql_connector()
        self.db_pool = await self.container.db_pool()

        history_listing_repository = self.container.history_listing_repository(db_pool=self.db_pool)

        self.history_listing_service = self.container.history_listing_service(
            history_listing_repository=history_listing_repository
        )

    async def _process_images(self):
        async with async_playwright() as p:
            self.browser_manager = BrowserManager(p, self.domain_url, self.store_dict)
            self.browser, self.page = await self.browser_manager.initialize()

            for history in self.items:
                is_clicked = history.get('is_clicked_submit')

                if is_clicked == 1:
                    continue

                product_id = history.get('product_wp_id')
                history_id = history.get('id')

                try:
                    await self.history_listing_service.update_clicked(history_id, PROCESSING)
                    await asyncio.sleep(1)
                    url = self.product_url.replace('product_id', str(product_id))

                    await self.page.goto(url)
                    if await self.page.query_selector('#error-page'):
                        continue

                    await self.page.wait_for_load_state('networkidle')
                    await self.page.evaluate("window.scrollTo(0, 0)")

                    publish_button = await self.page.query_selector('#publishing-action')

                    await asyncio.sleep(1)

                    if not publish_button:
                        continue

                    await publish_button.click()
                    await self.page.wait_for_load_state('networkidle')
                    await self.page.wait_for_url("**")
                    message = self.page.locator("#message.notice-success")
                    await message.wait_for(state="visible")

                    await self.history_listing_service.update_clicked(history_id)

                    print(f"Successfully processed product ID: {product_id}")
                    print('--------------------------------------')

                except Exception as e:
                    await self.history_listing_service.update_clicked(history_id, ERROR)
                    print("❌ Exception:", str(e))
                    traceback.print_exc()
                    return None

            await self.browser.close()
            return None

    async def close(self):
        await self.browser_manager.close_browser()
