from urllib.parse import SplitResult, urlsplit
from bs4 import BeautifulSoup, Tag

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
    p_find = soup.find("main").find("p")
    if p_find is not None:
        return p_find.get_text()
    p_find = soup.find("p")
    if p_find is not None:
        return p_find.get_text()
    return ""
