from bs4 import BeautifulSoup
import requests

def fetch_stock_information( stock_id ):

	url = "http://www.webapps.abc.utah.gov/Production/OnlineInventoryQuery/IQ/InventoryQuery.aspx"
	params = fetch_query_params(url)
	params["ctl00$ContentPlaceHolderBody$tbCscCode"] = stock_id

	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"charset": "UTF-8",
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
	}

	r = requests.post(url, headers=headers, data=params)

	# need to strip out that first line of the response
	# It's some ASPX async junk and not valid HTML
	content_full = r.text
	content_list = content_full.split('\n')
	content_list.pop(0)
	content = ''.join(content_list)

	stock_locations = []

	soup = BeautifulSoup(str.encode(content), 'html.parser')
	table = soup.find("table", {"class": "InvGv"}).find_all("tr", {"class": "gridViewRow"})
	# print (table)
	for location in table:
		tds = location.find_all('td')
		td = []
		# print ("Loc: ")
		for col in tds:
			td.append(col.text)
			# print (col.text)
		stock_locations.append(tuple(td))
	return stock_locations

def fetch_query_params( url ):
	fetched_params = {}
	r = requests.get(url)

	soup = BeautifulSoup(r.content, 'html.parser')

	fetched_params["__VIEWSTATE"] = soup.find(id='__VIEWSTATE').get('value')
	fetched_params['__VIEWSTATEGENERATOR'] = soup.find(id= '__VIEWSTATEGENERATOR').get('value')
	fetched_params['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION').get('value')
	fetched_params['__ASYNCPOST'] = 'true'

	return fetched_params

# print (fetch_stock_information("028236"))

# stock_id "028236" is for Bombay Sapphire 750ml (if I recall correctly)
# >>> import dabc_request
# >>> dabc_request.fetch_stock_information("028236")