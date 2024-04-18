import os, requests

try:
    url = os.environ['URL']
    print(requests.get(url).status_code)
except KeyError:
    print("URL not found")
