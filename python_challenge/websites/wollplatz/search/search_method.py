import requests
import cloudscraper
from bs4 import BeautifulSoup
import urllib.parse
from .variant_product_search import getVariantProductPage
from .constants import (
    baseUrl,
    isProductAvailable,
    Product,
    ProductVariantInfo,
    ProductVariant,
    scraperBrowserArgs
    )

def search(productToSearch: Product) -> list[ProductVariantInfo] | None:
    productVariantsResults = []

    # The initialisation of the scraper isn't too effective right now as this example does not use async.
    # A problem with the approach of using cloudscraper is that is sometimes needs to wait to avoid cloudflare's bot detection. With async enabled, this issue would be greatly mitigated.
    scraper = cloudscraper.create_scraper(
        browser=scraperBrowserArgs
    )

    if not productToSearch["relativeUrl"]:
        relativeUrl = _findProductRelativeUrl(productToSearch)
        if relativeUrl:
            productToSearch["relativeUrl"] = relativeUrl
        else:
            return
        
    productPage = _getInitialProductPage(scraper, productToSearch["relativeUrl"])
    productVariants = _getProductVariants(productPage)

    # this is a required value for getting data for variants
    hdMainProductId = productPage.find("input", {"id": "ContentPlaceHolder1_hdMainProductId"}).get("value")

    for productVariant in productVariants:
        variantProductPage = getVariantProductPage(scraper, productToSearch["relativeUrl"], hdMainProductId, productVariant["dataId"],)
        productVariantInfo = _getProductVariantInfo(variantProductPage, productVariant["name"])
        if productVariantInfo:
            productVariantsResults.append(productVariantInfo)
    return productVariantsResults

# This is the function that handles custom searches, like the example ones in runner.py. I ran out of time to finalise it but it's mostly finished, demonstrates its purpose, and I believe's there's a clear path towards making it fully functional.
def _findProductRelativeUrl( productToSearch: Product) -> str | None:
    # This method assumes the first search result is correct, as a simple proof-of-concept that could be expended upon in a real product
    urlSafeProductName = urllib.parse.quote(productToSearch['name'])
    urlSafeProductBrandName = urllib.parse.quote(productToSearch["brandName"])

    # This method may or may not work when this is being reviewed. If I were to continue this, I would confirm whether or not the snowplow IDs need to be updated over time and have the code do so if needed. At the time of writing, this code works.
    # (sooqr seems to be a third party 'Conversion Rate Optimization tool for your eCommerce', https://www.sooqr.com/)
    sooqrResponse = requests.get(f"https://dynamic.sooqr.com/suggest/script/?searchQuery={urlSafeProductName}&filterQuery%5B191640%5D%5B%5D={urlSafeProductBrandName}&limit=1&url=%2Fwolle&sid=144952626.991265444.1700164919.1700524502.1700529218.12&snowplow%5Bdomain_userid%5D=01febbc2-075c-436c-a519-d192e8096997&snowplow%5Bdomain_sessionidx%5D=11&snowplow%5Bdomain_sessionid%5D=1de3d2f1-3f7b-4f03-b096-da11bcab4db1&account=SQ-119572-1")
    sooqrResponseText = sooqrResponse.text

    if sooqrResponseText.find("lieferte keine Ergebnisse"):
        print(f"no results found for: {productToSearch}")
        return
    
    dirtyRelativeUrl = sooqrResponseText.split("www.wollplatz.de")[1].split("\" ")[0]
    cleanRelativeUrl = dirtyRelativeUrl.replace("\\", "")
    
    return cleanRelativeUrl

def _getInitialProductPage(scraper, productRelativeLink: str):
    productPageUrl = baseUrl + productRelativeLink
    productWebpage = scraper.get(productPageUrl)
    return BeautifulSoup(productWebpage.content, "html.parser")

def _getProductVariants(productWebpage) -> list[ProductVariant]:
    variants = []
    variantsContainer = productWebpage.find("div", {"class": "variants-group-container"})
    if variantsContainer is None:
        # in reality I would suggest handling something like this with e.g. google cloud logging with alerts, and include more useful debugging info
        nonBreakingErrorLogFile = open("nonBreakingErrorLog.txt", "a")
        nonBreakingErrorLogFile.write(f"A product does not have variants, currently this is not properly handled. Dumping productWebpage below for debugging:\n{productWebpage}\n\n")
        nonBreakingErrorLogFile.close()
        return variants
        
    for variant in variantsContainer.findChildren("div", {"class": "variants-sb-box-item"}):
        variants.append({
            "name": variant.find("span").get("data-list-text"),
            "dataId": variant.get("data-id")
            })
    return variants


def _getProductVariantInfo(variantProductPage, variantName) -> ProductVariantInfo | None:
    productVariantInfo = {"name": variantName}

    availabilityText = variantProductPage.find("div", {"id": "ContentPlaceHolder1_upStockInfoDescription"}).text.strip()
    productVariantInfo.update({"availability": {"isAvailable": isProductAvailable(availabilityText), availabilityText: availabilityText}})

    priceText = variantProductPage.find("span", {"itemprop": "price"}).text.strip()
    productVariantInfo.update({"price": priceText})

    specificationsTable = variantProductPage.find("div", {"id": "pdetailTableSpecs"})
    
    needleSizeRow = specificationsTable.find("td", string="Nadelstärke").parent
    needleSizeText = needleSizeRow.select("td")[1].text.strip()
    productVariantInfo.update({"needleSize": needleSizeText})

    compositionRow = specificationsTable.find("td", string="Zusammenstellung").parent
    compositionText = compositionRow.select("td")[1].text.strip()
    productVariantInfo.update({"composition": compositionText})

    return productVariantInfo




