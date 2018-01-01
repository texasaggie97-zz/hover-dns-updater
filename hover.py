#!/usr/bin/env python

"""hover.py: Provides dynamic DNS functionality for Hover.com using their unofficial API. 
   This script is based off one by Andrew Barilla: https://gist.github.com/andybarilla/b0dd93e71ff18303c059"""

__author__      = "Mark Silva"
__credits__ = ["Mark Silva", "Andrew Barilla", "Dan Krause"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Mark Silva"
__email__ = ""
__status__ = "Alpha"

import requests
import json

# Your hover.com username and password
username = "username"
password = "password"
 
# Sign into hover.com and then go to: https://www.hover.com/api/domains/YOURDOMAIN.COM/dns
# Look for the subdomain record(s) that you want to update and put its/their id(s) here.
dns_ids = ["dns0000000"]
 
class HoverException(Exception):
    pass
 
 
class HoverAPI(object):
    def __init__(self, username, password):
        params = {"username": username, "password": password}
        r = requests.post("https://www.hover.com/api/login", params=params)
        if not r.ok or "hoverauth" not in r.cookies:
            raise HoverException(r)
        self.cookies = {"hoverauth": r.cookies["hoverauth"]}
    def call(self, method, resource, data=None):
        url = "https://www.hover.com/api/{0}".format(resource)
        r = requests.request(method, url, data=data, cookies=self.cookies)
        if not r.ok:
            raise HoverException(r)
        if r.content:
            body = r.json()
            if "succeeded" not in body or body["succeeded"] is not True:
                raise HoverException(body)
            return body
 
ip = requests.post("http://bot.whatismyipaddress.com")
if ip.ok:
    # connect to the API using your account
    client = HoverAPI(username, password)
 
    current_ip = ip.content
    same_ip = False

    current = client.call("get", "dns")
        
    try:
        for domain in current.get("domains"):
            for entry in domain["entries"]:
                if entry["id"] in dns_ids and entry["content"] == current_ip:
                    same_ip = True
    except:
        pass

    if not same_ip:
        for dns_id in dns_ids:
            client.call("put", "dns/" + dns_id, {"content": current_ip})