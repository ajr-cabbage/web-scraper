import asyncio
import aiohttp
from typing import Any

from crawl import urlsplit, normalize_url, extract_page_data

class AsyncCrawler:
    base_url: str
    base_domain: str
    page_data: dict[str, Any]
    lock: asyncio.Lock
    max_concurrency: int
    semaphore: asyncio.Semaphore
    session: aiohttp.ClientSession
    max_pages: int
    should_stop: bool
    all_tasks: set

    def __init__(self, base_url: str, max_concurrency=5, max_pages=50) -> None:
        self.base_url = base_url
        self.base_domain = base_url
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()


    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return False
            return normalized_url not in self.page_data

    async def get_html(self, url: str):
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as resp:
            if resp.status >= 400:
                raise Exception("Status code: ", resp.status)
            if "text/html" not in resp.headers["Content-Type"]:
                raise Exception("Incorrect Content-Type")
            return await resp.text()

    async def crawl_page(self, base_url: str, current_url=None):
        if self.should_stop:
            return
        curr_url = current_url
        if curr_url is None:
            curr_url = base_url
        print("Crawling: ", curr_url)
        if urlsplit(curr_url).netloc != urlsplit(base_url).netloc:
            #print("link out of bounds")
            return
        norm_url = normalize_url(curr_url)
        try:
            async with self.semaphore:
                html = await self.get_html(curr_url)
        except Exception as e:
            print(e)
            return
        dat = extract_page_data(html, curr_url)
        if not await self.add_page_visit(norm_url):
            return
        async with self.lock:
            self.page_data[norm_url] = dat
        urls = dat["outgoing_links"]
        current_tasks = []
        try:
            for url in urls:
                new_task = asyncio.create_task(self.crawl_page(base_url, url))
                self.all_tasks.add(new_task)
                current_tasks.append(new_task)
        finally:
            await asyncio.gather(*current_tasks, return_exceptions=True)
            for task in current_tasks:
                self.all_tasks.discard(task)


    async def crawl(self) -> dict[str, Any]:
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url: str, max_concurrency=5, max_pages=50) -> dict[str, Any]:
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        await crawler.crawl()
    return crawler.page_data
