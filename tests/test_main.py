import unittest
from pyshortener.main import shorten, expand, LongUrlError

class TestShorten(unittest.TestCase):
    def test_shorten_valid_url(self):
        url = "http://example.com"
        short_url = shorten(url)
        self.assertEqual(short_url, "https://is.gd/iKpnPV")
    
    def test_shorten_complicated_valid_url(self):
        url = "https://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14"
        short_url = shorten(url)
        self.assertEqual(short_url, "https://is.gd/kiARyX")

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