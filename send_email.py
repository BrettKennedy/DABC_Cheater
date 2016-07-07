import smtplib
import json

def get_gmail_creds ( ): 
	with open('data.json') as data_file:
		data = json.load(data_file)
		return data["gmail_smtp_credentials"]
	return {}

def send_email( recipients, message ):
	# Get credentials
	creds = get_gmail_creds()
	# Connect to the server
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	# Log in
	server.login(creds['username'],creds['password'])
	# Send the payload
	server.sendmail(creds['username'], recipients, message)
	# abandon ship
	server.quit()
	
