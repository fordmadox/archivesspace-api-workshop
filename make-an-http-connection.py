#!/usr/bin/env python3
import urllib.request

api_url = input('ArchivesSpace API URL: ')
req = urllib.request.Request(api_url)

response =  urllib.request.urlopen(req)
print(response.read().decode('utf-8'))

