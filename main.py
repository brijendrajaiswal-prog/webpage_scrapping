#pip install requests
import smtplib
import ssl

import request
import requests
#pip install selectorlib
import selectorlib
from pyexpat.errors import messages


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

def send_email(message):
	host = "smtp.gmail.com"
	port = 465

	username = "brijendra.jaiswal@gmail.com"
	password = "put_your_password"
	# password = "your_app_password"

	receiver = "brijendra.jaiswal@gmail.com"
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL(host, port, context=context) as server:
		server.login(username, password)
		server.sendmail(username, receiver, message)
	print("Email has been sent...")

def store(extracted):
	with open("data.txt", "a") as file:
		file.write(extracted+"\n")

def read(extracted):
	with open("data.txt", "r") as file:
		return file.read()

if __name__ == "__main__":
	scraped = scrape(URL)
	extracted = extract(scraped)
	print(extracted)

	content = read(extracted)
	if extracted != 'No upcoming tours':
		if extracted not in content:
			store(extracted)
			send_email(message="A new event has been found ....")
			print("Email has been triggered....")




