import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from blacklist import *
from integrity import *


if __name__ == "__main__":
	try:
		from config import CONFIG
	except ImportError:
		print "Error: config.py NOT found"
		exit()

	content =  "=======================\n"
	content += "= Checking blacklists =\n"
	content += "=======================\n\n"
	content += check_blacklist() + "\n"

	# content += "=======================================\n"
	# content += "= Checking website status with Sucuri =\n"
	# content += "=======================================\n\n"
	# content += check_sites()

	content += "===============================\n"
	content += "= Checking websites integrity =\n"
	content += "===============================\n\n"
	content += check_websites()

	msg = MIMEMultipart()
	msg['From'] = CONFIG['email']['from']
	msg['To'] = CONFIG['email']['to']
	msg['Subject'] = "Rapport des sites"
	msg.attach(MIMEText(content, 'plain'))

	server = smtplib.SMTP(CONFIG['email']['smtp'], CONFIG['email']['port'])
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(CONFIG['email']['username'], CONFIG['email']['password'])
	text = msg.as_string()
	server.sendmail(CONFIG['email']['from'], CONFIG['email']['to'], text)
