#pip install requests
import request
import requests
#pip install selectorlib
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# You can write the fun in a separte code
def scrape(url):
	"""Scrap the page source from the URL """

	response = requests.get(url, headers=HEADERS)
	source = response.text
	return source

def extract(source):
	"""Extract all the links from the source """
	extractor = selectorlib.Extractor(source).from_yaml_file("extract.yaml")
	value = extractor.extract(source)['tours']
	return value

if __name__ == "__main__":
	scraped = scrape(URL)
	extracted = extract(scraped)
	print(extracted)



