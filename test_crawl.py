import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data

class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_2(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_3(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_4(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_1(self):
        input_html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
            <main>
              <p>Learn to code by building real projects.</p>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)
    def test_get_heading_2(self):
        input_html = """
        <html>
            <body>
            <h2>Welcome to Boot.dev</h2>
            <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
            </main>
            </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)
    def test_get_heading_3(self):
        input_html = """
        <html>
            <body>
            <main>
            </main>
            </body>
        </html>
        """
        actual = get_heading_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_paragraph_1(self):
        input_html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
            <main>
              <p>Learn to code by building real projects.</p>
              <p>This is the second paragraph.</p>
            </main>
          </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)
    def test_get_paragraph_2(self):
        input_html = """
        <html>
            <body>
                <p>Outside paragraph.</p>
                <main>
                    <p>Main paragraph.</p>
                </main>
            </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    def test_get_paragraph_3(self):
        input_html = """
        <html>
            <body>
            <main>
            </main>
            </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_paragraph_4(self):
        input_html = """
        <html>
            <body>
                <p>Outside paragraph.</p>
                <main>
                    <b>Main paragraph.</b>
                </main>
            </body>
        </html>
        """
        actual = get_first_paragraph_from_html(input_html)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_1(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_absolute_2(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com/things/and/stuff/"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/things/and/stuff/"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_absolute_3(self):
        input_url = "http://www.example.com"
        input_body = """
        <html><head><title>The Dormouse's story</title></head>
        <body>
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://www.example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://www.example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>
        <p class="story">...</p>
        """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["http://www.example.com/elsie", "http://www.example.com/lacie", "http://www.example.com/tillie"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_1(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_relative_2(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="images/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/images/logo.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_relative_3(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic_1(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_basic_2(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <html><body>
            <h2>Test Title</h2>
            <p>This is the first paragraph.</p>
            <main><p>This is the real paragraph</p></main>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
            <img src="https://crawler-test.com/hats/bluehat.png"
        </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the real paragraph",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg", "https://crawler-test.com/hats/bluehat.png"],
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
