import json
from constants import SearchQuery, productsAlwaysSearched
from websites.wollplatz import search_handler as wollplatz_search_handler
# from websites.another_website_here import search_handler as another_website_here_search_handler


searchHandlers: list = [
    wollplatz_search_handler,
    # another_website_here_search_handler
]

# This is set up to be handed queries from e.g. a search form on the website hosting this code.
# The user would input the paramaters and submit them for a search, and we would then retun the results to them that are currently saved in json format.
def searchAllWebsites(_searchQuery: SearchQuery, debug_mode=False):
    if debug_mode:
        combinedSearchQuery = _searchQuery
    else:
        combinedSearchQuery = _searchQuery | productsAlwaysSearched

    queryResults = []

    # iterating like this allows us to easily conduct the same search over multiple websites, with each directory having its own independent search method(s) for the website it handles
    # each search_handler should return results in the standardised ProductSearchResults format (found outlined in this example in 'runner\websites\wollplatz\search_handler.py')
    for searchHandler in searchHandlers:
        for brandName, productQueries in combinedSearchQuery.items():
            for productQuery in productQueries:
                productQuery.update({"brandName": brandName})
            # For the sake of time and simplicity I opted not to make this project asyc, but if I were to continue this project it would be my #1 priority to greatly improve execution speed
            queryResult = searchHandler.handleSearch(productQueries)
            queryResults.append(queryResult)
    
    result = {
        "combinedSearchQuery": combinedSearchQuery,
        "queryResults": queryResults,
    }

    resultJsonObject = json.dumps(result, sort_keys=True, indent=4)
    with open("results.json", "w") as outfile:
       outfile.write(resultJsonObject)

# to run all of the code, simply run this file with python
searchAllWebsites({
    "Gütermann": [
        {"name": "Creative Cotton Box", "relativeUrl": ""}
        ],
    "Rico": [
        {"name": "Baby Dream DK", "relativeUrl": ""},
        ],
    "Budgetyarn": [
        {"name": "Soft Aran", "relativeUrl": ""}
        ]
    })
