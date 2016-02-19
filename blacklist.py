import dns.resolver
import sys

def check_blacklist():
	try:
		from config import CONFIG
	except ImportError:
		print "Error: config.py NOT found"
		exit()

	backlist_operators = ["zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org", "virbl.dnsbl.bit.nl", "dnsbl.inps.de", "ix.dnsbl.manitu.net", "dnsbl.sorbs.net", "bl.spamcannibal.org", "bl.spamcop.net", "xbl.spamhaus.org", "pbl.spamhaus.org", "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net", "dnsbl-3.uceprotect.net", "db.wpbl.info"]

	content = ""
	for site_info in CONFIG['blacklist']['ips']:
		single_content = ""
		for backlist_operator in backlist_operators:
		    try:
	        	my_resolver = dns.resolver.Resolver()
		        query = '.'.join(reversed(str(site_info[0]).split("."))) + "." + backlist_operator
	        	answers = my_resolver.query(query, "A")
		        answer_txt = my_resolver.query(query, "TXT")
        		single_content += '%s (%s) IS listed in %s (%s: %s)' %(site_info[1], site_info[0], bl, answers[0], answer_txt[0]) + "\n"
		    except dns.resolver.NXDOMAIN:
				pass

		if single_content == "":
	       		single_content += '%s (%s): OK' %(site_info[1], site_info[0]) + "\n"

		content += single_content

	return content

# Send report (Only if in standalone)
if __name__ == "__main__":
	print check_blacklist()
