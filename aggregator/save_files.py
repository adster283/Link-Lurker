import requests

response = requests.get('https://adaway.org/hosts.txt')

f = open("unprocessed.txt", "w")
f.write(response.text)
f.close()

