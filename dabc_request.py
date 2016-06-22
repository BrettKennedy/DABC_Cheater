from bs4 import BeautifulSoup
import requests

def fetch_stock_information( stock_id ):

	# These params are mostly magic smoke and I bet they're brittle.
	# If they break, we'll need to make a get request to URL and parse the page for the new values
	params = {
		"ctl00$ContentPlaceHolderBody$tbCscCode": stock_id,
		"__EVENTVALIDATION": "/wEdAAsceQFxKsYHGdr5+su7V1JQ6NJMDzww3IJozuamiH2ntIYHsMIzYYJ+hEPXbUswhEgM+Qi2wto3oIoOmOtZDQewMu1wDE8XlC69lmZmCD+HfJNQBJwY3SeA8fU/nTO3Cgd0dXDvR/gB01/GD3JYF0vk2B395ZvQbXFGN04uuEIz14KTWmUjUiEBImqToeuQtKrqZqEd5e1TGujvVLTXWKyhCPvlvwBboFdZ+tYjLeo3N1Kp9BzETeWFQPX/PY1aaR18rtB+8/WvIa+nhyI6Xigw",
		"__VIEWSTATEGENERATOR": "791A1D40",
		"__VIEWSTATE": "/wEPDwUKLTUyMDQwNjM5Ng9kFgJmD2QWAgIDD2QWAgIFD2QWAgIDD2QWAgIBD2QWAmYPZBYGAgMPZBYGAgEPZBYCAgMPDxYCHgRUZXh0ZWRkAgMPZBYCAgMPDxYCHwBlZGQCBQ8PFgIfAAUMVmVyc2lvbiAzODYyZGQCBQ8PFgIeB1Zpc2libGVnZBYSAgMPDxYCHwAFATBkZAIHDw8WAh8ABQEwZGQCCw8PFgIfAAUGMDAxNDc1ZGQCDQ8PFgIfAAUoQk9NQkFZIFNBUFBISVJFIEdJTiBXL0dMUycxNSAgICAgICA3NTBtbGRkAhEPDxYCHwAFEFMgIFNwZWNpYWwgT3JkZXJkZAITDw8WAh8ABR9BdmFpbGFibGUgYnkgU3BlY2lhbCBPcmRlciBPbmx5ZGQCFw8PFgIfAAUGJDIyLjk5ZGQCGQ8PFgIfAAUcIGFzIG9mIFR1ZXNkYXkgSnVuZSAyMSwgMjAxNmRkAh0PZBYCAgEPPCsAEQMADxYEHgtfIURhdGFCb3VuZGceC18hSXRlbUNvdW50ZmQBEBYAFgAWAAwUKwAAZAILD2QWAgIBD2QWAgITD2QWAgIBD2QWAgIBD2QWAgIHDzwrABEBDBQrAABkGAIFKmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlckJvZHkkZXJyb3JHcmlkdmlldw9nZAUvY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyQm9keSRndkludmVudG9yeURldGFpbHMPPCsADAEIZmSM03YGYY0XxVD5jdx4/96+wL3SgyiOm59GZ0ke8QKECQ==",
		"__ASYNCPOST": "true",
		}
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"charset": "UTF-8",
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
	}
	url = "http://www.webapps.abc.utah.gov/Production/OnlineInventoryQuery/IQ/InventoryQuery.aspx"

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

# stock_id "028236" is for Bombay Sapphire 750ml (if I recall correctly)
# print (fetch_stock_information("028236"))

# >>> import dabc_request
# >>> dabc_request.fetch_stock_information("028236")