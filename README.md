# Website-Security-Analyser
Little Python script to monitor differents aspects of our differents websites (Blacklists, content integrity, etc.)

Configuration
=============

You MUST create a config.py file similar to this :

~~~python
CONFIG = {
    'email': {
        'smtp': 'SMTP_SERVER.com',
        'port': '25',
        'username': 'SMTP_USERNAME',
        'password': 'SMTP_PASSWORD',
        'from': 'EMAIL@ADRESS.COM',
        'to': 'EMAIL2@ADRESS.COM'
    },
    'blacklist': {
        'ips': [
            ("IP_OF_SERVER", "SERVER_NAME")
        ]
    },
    'integrity': {
        'domains': {
            'DOMAIN_NAME': {
                'url': 'http://DOMAINE.com'
                'tags': ['TAGS_TO_EXCLUDES']
            }
        }
    }
}
~~~

Configuring integrity
=====================

You have 3 choices :

  * Removing a classname from each tags it appears using the syntax: .CLASS_NAME. You can use regex. For example with Wordpress and Visual Composer, you can use **.vc_row-([0-9]+)**.
  * Removing all tags using the syntax: TAG_NAME. For example: **script**
  * Removing all tags containing a class using the syntax: TAG_NAME.CLASS_NAME. For example: **div.rss**

