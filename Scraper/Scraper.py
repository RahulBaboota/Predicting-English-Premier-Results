import csv
import requests as r
from lxml import html
from pprint import pprint

## Defining the heading columns.
headerData = ['Season', 'Name', 'Attack', 'Midfield', 'Defense', 'Overall']

with open('Log.csv', 'a') as f:
	writer = csv.writer(f)
	writer.writerow(headerData)

## Defining the 'dynamic' url from where to extract the data .
for i in range(0, 13):

	if (i == 0):
		url = 'https://www.fifaindex.com/teams/fifa06_2/?league=13'
		print url
	else:
		url = 'https://www.fifaindex.com' + urlList[-i] + '?league=13'
		print url

	## Sending a 'GET' request to the above url .
	Response = r.get(url)

	## Parsing the response and creating a Tree from it .
	Tree = html.fromstring(Response.text)

	## Getting all the information for the team objects.
	teamObjects = Tree.xpath('/html/body/main/div/div[2]/div[2]/div/table/tbody')[0]

	## Iterating through each team object to extract their information.
	for Object in teamObjects:

		## Creating a short-lived list which contains all the data for a particular team for the particular season.
		rowData = []

		## Adding the relevant information to the dictionary.
		seasonNum = int('20' + url[36:38])
		rowData.append(str(seasonNum - 1) + '-' + str(seasonNum))
		rowData.append(Object.xpath('./td[@data-title = "Name"]/a/text()')[0])
		rowData.append(Object.xpath('./td[@data-title = "ATT"]/span/text()')[0])
		rowData.append(Object.xpath('./td[@data-title = "MID"]/span/text()')[0])
		rowData.append(Object.xpath('./td[@data-title = "DEF"]/span/text()')[0])
		rowData.append(Object.xpath('./td[@data-title = "OVR"]/span/text()')[0])

		with open('Log.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(rowData)
		
	if (i == 0):
		## Obtaining the url's for the other season pages.
		urlList = Tree.xpath('/html/body/main/div/div[2]/div[2]/nav[1]/ol/li[2]/div//a/@href')[2:14]