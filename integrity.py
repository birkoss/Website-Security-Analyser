from bs4 import BeautifulSoup

import urllib2
import os
import re
import hashlib
import time

def check_websites():
    try:
        from config import CONFIG
    except ImportError:
        print "Error: config.py NOT found"
        exit()

    content = ""

    for site_name in CONFIG['integrity']['domains']:
        site_content = urllib2.urlopen( CONFIG['integrity']['domains'][site_name]['url'] ).read()
        soup = BeautifulSoup(site_content)

        try:
            for site_tag in CONFIG['integrity']['domains'][site_name]['tags']:
                matchObj = re.match( r'([^.#]*)([.#]?)([^.#]*)', site_tag, re.M|re.I)
                if matchObj:
                    if matchObj.group(1) == "":         # Matching .CLASSNAME format
                        soup = BeautifulSoup( re.sub( matchObj.group(3), "", str(soup)) )
                    elif matchObj.group(2) == "":       # Matching TAG format
                        [x.extract() for x in soup.findAll( matchObj.group(1))]
                    else:                               # Matching TAG.CLASSNAME format
                        [x.extract() for x in soup.findAll( matchObj.group(1), { ("id" if matchObj.group(2) == "#" else "class"): re.compile( matchObj.group(3)) } )]
        except KeyError:
            pass

        new_md5 = hashlib.md5( str(soup) ).hexdigest()

        # Create site path if not presents
        site_path = '.integrity/' + site_name + "/"
        if not os.path.exists(site_path):
            os.makedirs(site_path)

        # Save the file content (useful to analyse later)
        file = open(site_path + (time.strftime("%Y-%m-%d")) + ".html", "w")
        file.write( str(soup) )
        file.close()

        # Open existing MD5
        current_md5 = ""
        try:
            with open(site_path + "/md5.txt", 'r') as content_file:
                current_md5 = content_file.read()
        except IOError:
            pass

        # Save new MD5
        file = open(site_path + "/md5.txt", "w")
        file.write( new_md5 )
        file.close()

        if current_md5 == "":
            content += site_name + ": CREATED\n"
        else:
            content += site_name + ": " + ("OK" if new_md5 == current_md5 else "CHANGED") + "\n"

    return content

# Send report (Only if in standalone)
if __name__ == "__main__":
    print check_websites()
