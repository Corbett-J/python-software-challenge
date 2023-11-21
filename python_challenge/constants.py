from typing import TypedDict

# documentation through typing
class Product(TypedDict):
    name: str
    relativeUrl: int

class ProductVariantInfo(TypedDict):
    name: str
    price: str
    availability: str
    needleSize: str
    composition: str

class ProductVariant(TypedDict):
    name: str
    dataId: str

_brandName = str
_platformName = str

class SearchQuery(TypedDict):
    _brandName: list[
        Product
       ]

class SearchResults(TypedDict):
    _platformName: list[
        Product
       ]
    
class ProductSearchResult(TypedDict):
    name: str
    results: list[ProductVariantInfo]

class ProductVariantInfo(TypedDict):
    name: str
    price: str
    availability: str
    needleSize: str
    composition: str

ProductSearchResults = list[ProductSearchResult]

# I've set up the data in this format for better readibility and to help keep the code DRY, should this list expand in the future.
productsAlwaysSearched: SearchQuery = {
    "DMC": [
        {"name": "Natura XL", "relativeUrl": "/wolle/dmc/dmc-natura-xl"}
        ],
    "Drops": [
        {"name": "Safran", "relativeUrl": "/wolle/drops/drops-safran"},
        {"name": "Baby Merino Mix", "relativeUrl": "/wolle/drops/drops-baby-merino-mix"}
        ],
    # This brand and product both do not currently exist on the website.
    # I'll leave the code like this for this challange, but in reality I would discuss this issue with whoever set the task.
    "Hahn": [
        {"name": "Alpacca Speciale", "relativeUrl": ""},
        ],
    "Stylecraft": [
        {"name": "Special double knit", "relativeUrl": "/wolle/stylecraft/stylecraft-special-dk"}
        ]
    }