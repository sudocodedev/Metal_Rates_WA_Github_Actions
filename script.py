import os

print("Hello World!! I was ran by Github actions")

try:
    number = os.environ["URL"]
except KeyError:
    number = "Key Not Found"

print(number)
