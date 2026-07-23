import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

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


if __name__ == "__main__":
    unittest.main()
