import unittest
from python_challenge.websites.wollplatz.search.search_method import _getProductVariantInfo, _getProductVariants
from python_challenge.websites.wollplatz.search.variant_product_search import _getSearchRequestbody, _getSearchRequestHeaders
from python_challenge.websites.wollplatz.search.constants import isProductAvailable as _isProductAvailable
from testing.constants import knownGoodProductPage
from testing.getProductVariantInfo.constants import expectedProductVariantInfo
from testing.getProductVariants.constants import expectedProductVariants
from testing.getSearchRequestHeaders.constants import expectedSearchRequestHeaders
from testing.getSearchRequestbody.constants import expectedSearchRequestBody

class getProductVariantInfo(unittest.TestCase):
    def test_response_with_valid_data(self):
        productVariantInfo = _getProductVariantInfo(knownGoodProductPage, "example_name")
        self.assertEqual(productVariantInfo, expectedProductVariantInfo, "response does not match expected response")

class getProductVariants(unittest.TestCase):
    def test_response_with_valid_data(self):
        productVariants = _getProductVariants(knownGoodProductPage)
        self.assertEqual(productVariants, expectedProductVariants, "response does not match expected response")

class getSearchRequestHeaders(unittest.TestCase):
    def test_response_with_valid_data(self):
        searchRequestHeaders = _getSearchRequestHeaders("/example/url?testing=")
        self.assertEqual(searchRequestHeaders, expectedSearchRequestHeaders, "response does not match expected response")

class getSearchRequestbody(unittest.TestCase):
    def test_response_with_valid_data(self):
        searchRequestBody = _getSearchRequestbody("00018726_23", "1234431")
        self.assertEqual(searchRequestBody, expectedSearchRequestBody, "response does not match expected response")

class isProductAvailable(unittest.TestCase):
    def test_available_with_valid_data(self):
        availability = _isProductAvailable("Lieferbar")
        self.assertEqual(availability, True, "unexpected availability mapping")

    def test_unavailable_with_valid_data(self):
        availability = _isProductAvailable("Nicht mehr verfügbar, sehen Sie sich die Alternativen an")
        self.assertEqual(availability, False, "unexpected availability mapping")

    def test_unavailable_with_invalid_data(self):
        availability1 = _isProductAvailable("")
        self.assertEqual(availability1, False, "unexpected availability mapping")
        availability2 = _isProductAvailable(None)
        self.assertEqual(availability2, False, "unexpected availability mapping")
        availability3 = _isProductAvailable({})
        self.assertEqual(availability3, False, "unexpected availability mapping")
        availability4 = _isProductAvailable(1213)
        self.assertEqual(availability4, False, "unexpected availability mapping")






if __name__ == '__main__':
    unittest.main()