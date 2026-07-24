from typing import Any
from urllib.parse import SplitResult, urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
import requests

def normalize_url(input_url: str) -> str:
    spliturl: SplitResult = urlsplit(input_url)
    path: str = ""
    if spliturl.path[-1] == "/":
        path = spliturl.path[:-1]
    else:
        path = spliturl.path
    return spliturl.netloc + path

def get_heading_from_html(html: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    h1_find = soup.find("h1")
    if h1_find is not None:
        return h1_find.get_text()
    h2_find = soup.find("h2")
    if h2_find is not None:
        return h2_find.get_text()
    return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    main_find = soup.find("main")
    p_find = None
    if main_find is not None:
        p_find = main_find.find("p")
    if p_find is None:
        p_find = soup.find("p")
    if p_find is not None:
        return p_find.get_text()
    else:
        return ""

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    a_finds = soup.find_all("a")
    urls: list[str] = []
    for a in a_finds:
        url: str = a.get("href")
        urls.append(urljoin(base_url, url))
    return urls

def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    img_finds = soup.find_all("img")
    urls: list[str] = []
    for img in img_finds:
        url: str = img.get("src")
        #print("GET RESULT: ", url)
        #print("JOIN RESULT: ", urljoin(base_url, url))
        urls.append(urljoin(base_url, url))
    return urls

def extract_page_data(html: str, page_url: str) -> dict[str, Any]:
    pg_data = {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
    return pg_data

def get_html(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if resp.status_code >= 400:
        raise Exception("Status code: ", resp.status_code)
    if "text/html" not in resp.headers["Content-Type"]:
        raise Exception("Incorrect Content-Type")
    return resp.text

def crawl_page(base_url: str, current_url=None, page_data=None):
    curr_url = current_url
    if curr_url is None:
        curr_url = base_url
    #print("Crawling: ", curr_url)
    if urlsplit(curr_url).netloc != urlsplit(base_url).netloc:
        #print("link out of bounds")
        return
    norm_url = normalize_url(curr_url)
    if norm_url in page_data:
        #print("already been here")
        return
    try:
        html = get_html(curr_url)
    except Exception as e:
        print(e)
    dat = extract_page_data(html, curr_url)
    page_data[norm_url] = dat
    urls = dat["outgoing_links"]
    for url in urls:
        crawl_page(base_url, url, page_data)
