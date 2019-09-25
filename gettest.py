#!/usr/bin/env python3
import requests
url = "http://www.google.se"
output = requests.get(url).text
print(output)