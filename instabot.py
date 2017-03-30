import requests

APP_ACCESS_TOKEN = "2096873226.ed76845.d26be842838e497097d368aff4ed72ac"

BASE_URL = "https://api.instagram.com/v1/"

data = requests.get("http://facebook.com")

def self_info():
    requests_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    my_info = requests.get(requests_url).json()
    print "Requesting url:" + requests_url
    print my_info


self_info()