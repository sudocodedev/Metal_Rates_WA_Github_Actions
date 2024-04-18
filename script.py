import os

try:
    url = os.environ["URL"]
    to_no = os.environ["TO_PHONE_NUMBER"]
    from_no = os.environ["FROM_PHONE_NUMBER"]
    print(url,type(url))
    print(from_no,type(from_no))
    print(to_no,type(to_no))

except KeyError:
    print("Keys not found")

