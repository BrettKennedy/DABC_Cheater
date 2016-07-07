from bs4 import BeautifulSoup
import requests

url = "http://www.webapps.abc.utah.gov/Production/OnlineInventoryQuery/IQ/InventoryQuery.aspx"
def fetch_stock_data( stock_ids ):
	stock_data = {}

	# only fetch params once, reuse them for all stock queries
	base_params = fetch_query_params(url)

	# If our base_params query failed, return an empty object
	if len(list(base_params)) == 0:
		return {}


	for stock_id in stock_ids:
		current_params = dict.copy(base_params)
		current_params["ctl00$ContentPlaceHolderBody$tbCscCode"] = stock_id
		stock_data[stock_id] = fetch_stock_information(current_params)
	return stock_data

def fetch_stock_information( params ):

	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"charset": "UTF-8",
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
	}

	r = requests.post(url, headers=headers, data=params)

	# If the request fails, return an empty object
	if (r.status_code != 200):
		return []

	# need to strip out that first line of the response
	# It's some ASPX async junk and not valid HTML
	content_full = str(r.text)

	content_list = content_full.split('\n')
	content_list.pop(0)
	content = ''.join(content_list)

	stock_locations = []

	soup = BeautifulSoup(str.encode(content), 'html.parser')
	location_table = soup.find("table", {"class": "InvGv"})
	
	if location_table == None:
		return [];

	location_rows = location_table.find_all("tr", {"class": "gridViewRow"})

	if location_table == None:
		return [];

	# print (location_rows)
	for location in location_rows:
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

	# If the request fails, return an empty object
	if (r.status_code != 200):
		return {}

	soup = BeautifulSoup(r.content, 'html.parser')

	fetched_params["__VIEWSTATE"] = soup.find(id='__VIEWSTATE').get('value')
	fetched_params['__VIEWSTATEGENERATOR'] = soup.find(id= '__VIEWSTATEGENERATOR').get('value')
	fetched_params['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION').get('value')
	fetched_params['__ASYNCPOST'] = 'true'

	return fetched_params

def write_to_file(txt) :
	file = open('output.txt', 'w')
	file.write(txt)
	file.close()

# print (fetch_stock_information("028236"))
# print (fetch_stock_information("016906"))

# stock_id "028236" is for Bombay Sapphire 750ml (if I recall correctly)
# >>> import dabc_request
# >>> dabc_request.fetch_stock_data(["028236","016906"])
