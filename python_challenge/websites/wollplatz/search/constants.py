from typing import TypedDict

scraperBrowserArgs = {
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }

class Product(TypedDict):
    brandName: str
    name: str
    relativeUrl: str

class Availability(TypedDict):
    isAvailable: bool
    availabilityText: str
class ProductVariantInfo(TypedDict):
    name: str
    price: str
    availability: Availability
    needleSize: str
    composition: str

class ProductVariant(TypedDict):
    name: str
    dataId: str

# I've opted base availability on the availability text to begin with to give more flexibility:
# When building scrapers for platforms before there have been instances where my teams have wanted to consider technically available items to be unavailable. (E.g. if it the item would arrive after two months.)
def isProductAvailable(availabilityText: str) -> bool:
    match availabilityText:
        case "Lieferbar":
            return True
        case "Nicht mehr verfügbar, sehen Sie sich die Alternativen an":
            return False
        case "Reservieren Sie im Voraus, Lieferzeit nach Rücksprache nach Rücksprache":
            return False
        case _:
            # in reality I would suggest handling something like this with e.g. google cloud logging with alerts, and include more useful debugging info
            nonBreakingErrorLogFile = open("nonBreakingErrorLog.txt", "a")
            nonBreakingErrorLogFile.write(f"Unknown availability text: {availabilityText}\n")
            nonBreakingErrorLogFile.close()
            return False

baseUrl = "https://www.wollplatz.de"
variantVersionRequestUrl = baseUrl + "/Product-detail.aspx"


constantSearchRequestHeaders = {
    "authority": baseUrl,
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
    "origin": baseUrl,
    "request-context":"appId=cid-v1:e3a9afea-b955-4ac1-991c-20c079fe637f",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "x-requested-with":"XMLHttpRequest"
    }

constantSearchRequestBody = {
    "ctl00$ContentPlaceHolder1$scriptmanager": "ctl00$ContentPlaceHolder1$upChildProduct|ContentPlaceHolder1_upChildProduct",
    "__EVENTTARGET": "ContentPlaceHolder1_upChildProduct",
    "__VIEWSTATEGENERATOR": "F2EE7CEF",
    "ctl00$ContentPlaceHolder1$hdIsPackageProduct": False,
    "ctl00$ContentPlaceHolder1$hdIsSidebarProduct": False,
    "ctl00$ContentPlaceHolder1$hdMainProductIsComposedProduct": False,
    "ctl00$ContentPlaceHolder1$hdMainProductComposedProductSetChildSellPriceToZero": False,
    "ctl00$ContentPlaceHolder1$hdMainProductStockInfo": "",
    "ctl00$ContentPlaceHolder1$hdProductLabelClass": "label-duurzaam",
    "ctl00$ContentPlaceHolder1$hdProductLabelText": "Umweltfreundlich",
    "ctl00$ContentPlaceHolder1$hdVariantsDisplayType": "3",
    "ctl00$ContentPlaceHolder1$hdTransNoValidEmail": "E-mail nicht korrekt",
    "ctl00$ContentPlaceHolder1$hdColorPickerData": "",
    "ctl00$ContentPlaceHolder1$hdExternalPickerUrl": "",
    "ctl00$ContentPlaceHolder1$hdTransAdjustmentTextTooShort": "Invoer is te kort",
    "ctl00$ContentPlaceHolder1$hdTransAdjustmentTextTooLong": "Invoer is te lang",
    "ctl00$ContentPlaceHolder1$hdTransAdjustmentTextMinimalChars": "minimale aantal karakters",
    "ctl00$ContentPlaceHolder1$hdTransAdjustmentTextMaximalChars": "maximale aantal karakters",
    "ctl00$ContentPlaceHolder1$hdQtyUnitCorrected": "",
    "ctl00$ContentPlaceHolder1$hdShowVariantsInGridViewAsBoxed": "true",
    "ctl00$ContentPlaceHolder1$hdVariantChildHasOwnUrl": "S0vMKU4FAA==",
    "ctl00$ContentPlaceHolder1$hdProductAdjustmentCheckedValues": "",
    "ctl00$ContentPlaceHolder1$hdProductAdjustmentHasPreChosen": "",
    "ctl00$ContentPlaceHolder1$hdProductAdjustmentsIsValid": "",
    "ctl00$ContentPlaceHolder1$hdStandardAmountQtyCorrected": "",
    "ctl00$ContentPlaceHolder1$hdStandardAmountQty": "",
    "ctl00$ContentPlaceHolder1$ratings": "rating5",
    "ctl00$ContentPlaceHolder1$txtReviewName": "",
    "ctl00$ContentPlaceHolder1$txtReviewEmailAddress": "",
    "ctl00$ContentPlaceHolder1$txtFullNameCity": "",
    "ctl00$ContentPlaceHolder1$txtReviewArgument": "",
    "ctl00$ContentPlaceHolder1$txtCompeleteFullName": "",
    "ctl00$ContentPlaceHolder1$reviewverzonden": "",
    "ctl00$ContentPlaceHolder1$txtQuestion": "",
    "ctl00$ContentPlaceHolder1$txtQuestionName": "",
    "ctl00$ContentPlaceHolder1$txtQuestionEmailTel": "",
    "ctl00$ContentPlaceHolder1$txtCompleteZipCode": "",
    "ctl00$ContentPlaceHolder1$hdChosenOptions": "",
    "__ASYNCPOST": "true",
}