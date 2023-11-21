from bs4 import BeautifulSoup
from .constants import constantSearchRequestHeaders, constantSearchRequestBody, baseUrl, variantVersionRequestUrl

def _getSearchRequestHeaders(refererRelativeUrl: str) -> dict:
    searchRequestHeaders = {
        "referer": baseUrl + refererRelativeUrl,
	}
    searchRequestHeaders.update(constantSearchRequestHeaders)
    return searchRequestHeaders
    
def _getSearchRequestbody(hdMainProductId: str, variantDataId: str) -> dict:
    searchRequestBody = {
    	"__EVENTARGUMENT": "VariantGroup_" + variantDataId,
        "ctl00$ContentPlaceHolder1$hdChosenVariantId": variantDataId, # this just needs a data-id for any varient of the current product
        "ctl00$ContentPlaceHolder1$hdMainProductId": hdMainProductId,
	}
    searchRequestBody.update(constantSearchRequestBody)
    return searchRequestBody


def getVariantProductPage(scraper, productRelativeUrl: str, hdMainProductId: str, variantDataId: str):
    variantProductPage =  scraper.post(
        variantVersionRequestUrl,
        headers = _getSearchRequestHeaders(productRelativeUrl),
        data = _getSearchRequestbody(hdMainProductId, variantDataId)
        )
    page = BeautifulSoup(variantProductPage.content, "html.parser")
    return page
