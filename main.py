import sys
from crawl import crawl_page

def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    print("starting crawl of: ", args[1])
    page_dat = {}
    try:
        crawl_page(args[1], page_data=page_dat)
    except Exception as e:
        print(e)
    print("Results from ", args[1])
    print("Sites Visited: ", len(page_dat))
    for page in page_dat:
        print("URL: ", page_dat[page]["url"])
        print("Heading: ", page_dat[page]["heading"])
        print("First Paragraph: ", page_dat[page]["first_paragraph"])
        print("Links: ", page_dat[page]["outgoing_links"])
        print("Images: ", page_dat[page]["image_urls"])

if __name__ == "__main__":
    main()
