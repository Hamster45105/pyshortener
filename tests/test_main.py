import unittest
from pyshortener.main import shorten, expand, get_stats, LongUrlError, GenericError

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

    def test_get_stats_valid_url(self):
        short_url = "UsQlQM"
        stats = get_stats(short_url, 'hitsweek', format_response=True)
        self.assertIsInstance(stats, str)
        self.assertIn("Date,Visits", stats)

    def test_get_stats_valid_url_with_title(self):
        short_url = "UsQlQM"
        stats = get_stats(short_url, 'hitsweek', include_title=True, format_response=True)
        self.assertIsInstance(stats, str)
        self.assertIn("Visits this week", stats)
        self.assertIn("Date,Visits", stats)

    def test_get_stats_invalid_url(self):
        short_url = "invalid_url"
        with self.assertRaises(GenericError):
            get_stats(short_url, 'hitsweek', format_response=True)

    def test_get_stats_invalid_stats_type(self):
        short_url = "UsQlQM"
        with self.assertRaises(ValueError):
            get_stats(short_url, 'invalid_stats_type', format_response=True)

    def test_get_stats_invalid_service(self):
        short_url = "UsQlQM"
        with self.assertRaises(ValueError):
            get_stats(short_url, 'hitsweek', service="invalid_service", format_response=True)

if __name__ == "__main__":
    unittest.main()
