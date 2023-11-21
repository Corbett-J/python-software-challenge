from bs4 import BeautifulSoup

with open("testing\de_wolle_dmc_dmc-natura-xl.html", encoding="utf8") as example_html:
    knownGoodProductPage = BeautifulSoup(example_html, "html.parser")