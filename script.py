import os, requests
url = os.environ.get("URL")
print(url)
print(requests.get(url).status_code)