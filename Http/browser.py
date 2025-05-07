import os
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class BrowserManager:
    """Manages browser interactions."""

    def __init__(self, playwright, domain_url, store_dict=dict, user_data_dir=''):
        self.p = playwright
        self.store_dict = store_dict
        self.user_data_dir = f'profile/{user_data_dir}'
        self.browser = None
        self.page = None
        self.domain = domain_url

    async def launch_browser(self):
        headless = int(os.getenv("HEADLESS")) == 1
        self.browser = await self.p.firefox.launch(headless=headless)
        context = await self.browser.new_context()
        self.page = await context.new_page()
        """Logs into WordPress if login fields are detected."""
        await self.page.goto(self.domain)
        if await self.page.query_selector('#user_login'):
            logger.info("Logging in to WordPress...")
            await self.page.fill('input[name="log"]', self.store_dict['username_login'])
            await self.page.fill('input[name="pwd"]', self.store_dict['password_login'])
            await self.page.click('input[name="wp-submit"]')

        await self.page.wait_for_load_state('networkidle')

    async def initialize(self):
        """Initializes the browser and logs in."""
        await self.launch_browser()

        return self.browser, self.page
