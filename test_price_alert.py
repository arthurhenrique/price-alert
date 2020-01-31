import unittest
import httpretty
import requests
import logging
from sure import expect
from price_alert import config_logger, get_price


class TestPriceAlert(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPriceAlert, self).__init__(*args, **kwargs)
        self.url = "http://localhost:8090/TESTITEM"
        self.html_body = '<span id="priceblock_ourprice">79,99&nbsp;€</span>'
        self.xpath_selector = "//*[@id='priceblock_ourprice']"

    def setUp(self):
        config_logger(False)
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, self.url,
                               body=self.html_body,
                               content_type="application/json")
        # ugly workaround for https://github.com/gabrielfalcao/HTTPretty/issues/368
        import warnings
        warnings.filterwarnings(
            "ignore", category=ResourceWarning, message="unclosed.*")

    def test_get_price(self):
        price = get_price(self.url, self.xpath_selector)
        expect(price).to.equal(79.99)

    def test_get_price_not_found(self):
        price = get_price(self.url, "//*[@id='wrong']")
        expect(price).to.equal(None)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
