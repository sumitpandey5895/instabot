import requests

APP_ACCESS_TOKEN = "2096873226.ed76845.d26be842838e497097d368aff4ed72ac"

BASE_URL = "https://api.instagram.com/v1/"

data = requests.get("http://facebook.com")

def self_info():
    requests_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    my_info = requests.get(requests_url).json()
    print "Requesting url:" + requests_url
    print my_info
    print my_info['data']['bio']
    print my_info['data']['counts']['followed_by']

#------------------------------------------------------------------------------------

def get_user_by_username():
    user_list = ["singhsudanshu",]
    user_name = raw_input("Enter Username you wants to search or Q to quit : ")
    if user_name not in user_list:
        if user_name == "q" or user_name == "Q":
            exit()
        else:
            print "User doesn't exists !"
            get_user_by_username()
    else:
        requests_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (user_name, APP_ACCESS_TOKEN)
        user_info = requests.get(requests_url).json()
        print user_info
        get_user_by_username()


#self_info()

get_user_by_username()