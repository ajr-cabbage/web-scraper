import sys
import time
import asyncio
import json
from async_crawler import crawl_site_async
from typing import Any
# from crawl import crawl_page

def write_json_report(page_data: dict[str, Any], filename="report.json"):
    values = page_data.values()
    #print(values)
    sorted_by_url = sorted(values, key=lambda x: x['url'])
    with open(filename, "w") as f:
        json.dump(sorted_by_url, f, indent=2)


async def main_async():
    start_time = time.perf_counter()
    args = sys.argv

    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)
    print("starting crawl of: ", args[1])
    page_dat = {}
    try:
        if len(args) == 2:
            page_dat = await crawl_site_async(args[1])
        elif len(args) == 3:
            page_dat = await crawl_site_async(args[1], max_concurrency=int(args[2]))
        elif len(args) == 4:
            page_dat = await crawl_site_async(args[1], max_concurrency=int(args[2]), max_pages=int(args[3]))
    except Exception as e:
        print(e)
        sys.exit(1)
    print("Results from ", args[1])
    print("Sites Visited: ", len(page_dat))
    write_json_report(page_dat)
    #for page in page_dat:
    #    print("URL: ", page_dat[page]["url"])
    #    print("Heading: ", page_dat[page]["heading"])
    #    print("First Paragraph: ", page_dat[page]["first_paragraph"])
    #    print("# of Links: ", len(page_dat[page]["outgoing_links"]))
    #    print("# of Images: ", len(page_dat[page]["image_urls"]))
    end_time = time.perf_counter()
    exec_time = end_time - start_time
    print(f"Time: {exec_time:.6f} seconds")
if __name__ == "__main__":
    asyncio.run(main_async())
