import unittest
from pyshortener.main import shorten, expand, LongUrlError

class TestShorten(unittest.TestCase):
    def test_shorten_valid_url(self):
        url = "http://example.com"
        short_url = shorten(url)
        self.assertEqual(short_url, "https://is.gd/iKpnPV")

    def test_shorten_invalid_url(self):
        url = "invalid_url"
        with self.assertRaises(LongUrlError):
            shorten(url)

    def test_shorten_invalid_service(self):
        url = "https://www.example.com"
        with self.assertRaises(ValueError):
            shorten(url, service="invalid_service")

    def test_expand_valid_url(self):
        short_url = "https://is.gd/iKpnPV"
        expanded_url = expand(short_url)
        self.assertEqual(expanded_url, "http://example.com")

if __name__ == "__main__":
    unittest.main()