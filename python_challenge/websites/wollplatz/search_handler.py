import json
from typing import TypedDict
from .search.search_method import search
from .search.constants import (ProductVariantInfo, Product)

class ProductSearchResult(TypedDict):
    name: str
    results: list[ProductVariantInfo]

ProductSearchResults = list[ProductSearchResult]

class SearchResults(TypedDict):
    _platformName: list[
        Product
       ]

def handleSearch(productsToSearch: list[Product]) -> ProductSearchResults:
    productSearchResults = []
    for productToSearch in productsToSearch:
        productSearchResults.append({
        "name": productToSearch["name"],
        "results": search(productToSearch)
        })
    return productSearchResults
