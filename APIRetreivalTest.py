import requests

url = 'http://127.0.0.1:8000/'
response = requests.get(url)
for i in response.json():
    print(i)
    print("\n\n")