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
    user_list = ["singhsudanshu"]
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

        print "User id : " + str(user_info['data'][0]['id'])
        print "Full name : " + str(user_info['data'][0]['full_name'])
        print "Bio : " + str(user_info['data'][0]['bio'])
        response = raw_input("Enter Y to perform operations or N to continue : ").upper()
        if response == "Y":
            operations(user_info['data'][0]['id'])
        else:
            get_user_by_username()

#-------------------------------------------------------------------------------------------------------------------
def operations(user_id):
    requests_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    recent_posts =requests.get(requests_url).json()

    for likes in recent_posts['data']:
            print "Post id: " + str(likes['id']) + " likes :" + str(likes['likes']['count'])


get_user_by_username()