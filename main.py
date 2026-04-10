#pip install requests
import smtplib
import ssl
import time
from datetime import date

import request
import requests
#pip install selectorlib
import selectorlib
from pyexpat.errors import messages
import sqlite3


URL = "http://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# DB Connetion
connection = sqlite3.connect("data.db")

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
	#with open("data.txt", "a") as file:
	#	file.write(extracted+"\n")
	row = extracted.split(",")
	row = [item.strip() for item in row]
	cursor = connection.cursor()
	cursor.execute("Insert into events VALUES (?,?,?)",row)
	connection.commit()


def read(extracted):
	#with open("data.txt", "r") as file:
	#	return file.read()
	row = extracted.split(",")
	row = [item.strip() for item in row]
	band, city, date = row
	cursor = connection.cursor()

	cursor.execute("""
	CREATE TABLE IF NOT EXISTS events (
	    band TEXT,
	    city TEXT,
	    date TEXT
	)
	""")

	#connection.commit()
	cursor.execute("SELECT * FROM events where band=? AND city=? AND date=?",(band,city,date))
	row = cursor.fetchall()
	print(row)
	return row



if __name__ == "__main__":
	while True:
		scraped = scrape(URL)
		extracted = extract(scraped)
		print(extracted)

		if extracted != 'No upcoming tours':
			row = read(extracted)
			if not row:
				store(extracted)
				send_email(message="A new event has been found ....")
				#print("Email has been triggered....")
		time.sleep(2)




