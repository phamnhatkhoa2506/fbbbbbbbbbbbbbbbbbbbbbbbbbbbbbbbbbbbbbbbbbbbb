# import asyncio
# import json
# from typing import List, Dict
# from httpx import AsyncClient, Response
# from parsel import Selector
# from loguru import logger as log

# # initialize an async httpx client
# client = AsyncClient(
#     # enable http2
#     http2=True,
#     # add basic browser like headers to prevent being blocked
#     headers={
#         "Accept-Language": "en-US,en;q=0.9",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Accept-Encoding": "gzip, deflate, br",
#     },
# )

# def parse_profile(response: Response):
#     """parse profile data from hidden scripts on the HTML"""
#     assert response.status_code == 200, "request is blocked, use the ScrapFly codetabs"
#     selector = Selector(response.text)
#     data = selector.xpath("//script[@id='__UNIVERSAL_DATA_FOR_REHYDRATION__']/text()").get()
#     profile_data = json.loads(data)["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]  
#     return profile_data


# async def scrape_profiles(urls: List[str]) -> List[Dict]:
#     """scrape tiktok profiles data from their URLs"""
#     to_scrape = [client.get(url) for url in urls]
#     data = []
#     # scrape the URLs concurrently
#     for response in asyncio.as_completed(to_scrape):
#         response = await response
#         profile_data = parse_profile(response)
#         data.append(profile_data)
#     log.success(f"scraped {len(data)} profiles from profile pages")
#     return data


# async def run():
#     profile_data = await scrape_profiles(
#         urls=[
#             "https://www.tiktok.com/@oddanimalspecimens"
#         ]
#     )
#     # save the result to a JSON file
#     with open("profile_data.json", "w", encoding="utf-8") as file:
#         json.dump(profile_data, file, indent=2, ensure_ascii=False)


# if __name__ == "__main__":
#     asyncio.run(run())

import asyncio
import json
from loguru import logger as log
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse

SCRAPFLY = ScrapflyClient(key="scp-test-de0081e0084f44f58e69fb3c806a561d")

def parse_facebook_page(response: ScrapeApiResponse):
    """Parse public Facebook posts from a page."""
    page_html = response.scrape_result["content"]  # Lấy HTML của trang
    print(response)
    if not page_html:
        raise Exception("Không lấy được dữ liệu từ Facebook")
    
    # Giả lập việc trích xuất dữ liệu bài viết từ HTML
    posts = []
    # ⚠ Ở đây bạn cần BeautifulSoup hoặc regex để trích xuất nội dung bài viết
    # Ví dụ giả định:
    posts.append({"content": "Bài viết mẫu từ Facebook", "time": "2025-03-29"})

    return posts

async def scrape_facebook_page(url: str):
    """Scrape public posts from a Facebook page."""
    log.info(f"Scraping Facebook page: {url}")

    response = await SCRAPFLY.async_scrape(
        ScrapeConfig(
            url,
            asp=True,
            country="AU",
            render_js=True,
            rendering_wait=5000,  # Đợi JavaScript tải xong
        )
    )

    data = parse_facebook_page(response)
    log.success(f"Scraped {len(data)} posts from Facebook")
    return data

async def crawl_data(request):
    page_data = await scrape_facebook_page(
        url="https://www.facebook.com/Vuonglan1989"
    )
    with open("facebook_page_data.json", "w", encoding="utf-8") as file:
        json.dump(page_data, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # asyncio.run(run()) 
    '''
    '''