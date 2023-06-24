import requests

query = input("What is your query?\n")
query = query.replace(' ', '+')

#key is my custom API key, cx is my custom search engine
url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyBsCVTYP45YTcpUiBqtl_5MMEMaDQJWrM8&cx=f5996d80d9b394fb3&q="
response = requests.get(url + query)

print("Here are the first 10 titles")
for i in range(10):
    print(i+1, response.json()["items"][i]["title"])

#perfect
