import requests

APP_ACCESS_TOKEN = "2096873226.ed76845.d26be842838e497097d368aff4ed72ac"

BASE_URL = "https://api.instagram.com/v1/"


#_____________________________________________________________________________________________
def self_info():
    requests_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    my_info = requests.get(requests_url).json()
    print "Requesting url:" + requests_url
    print my_info
    print my_info['data']['bio']
    print my_info['data']['counts']['followed_by']


#_____________________________________________________________________________________________
def get_user_by_username():
    user_list = ["singhsudanshu","shubham.is.here"]
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

#_____________________________________________________________________________________________
def operations(user_id):
    requests_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    recent_posts =requests.get(requests_url).json()
    post_list = ["x"]
    for likes in recent_posts['data']:
            post_list.append(likes['id'])
            print "User_id : " + str(user_id) + " Post id: " + str(post_list.index(likes['id'])) + " likes :" + str(likes['likes']['count'])

    post_id = raw_input("Enter Post Id you wan't to access OR B to go back: ")
    if post_id == "b" or post_id == "B":
        get_user_by_username()
    else:
        x = int(post_id)

    if post_list[x] not in post_list:
        print "Invalid Post id !"
        operations(user_id)
    else:
        post_id = post_list[x]
        select_operation(user_id ,post_id)

#_____________________________________________________________________________________________
def select_operation(user_id , post_id):
    opr = raw_input("Enter L to like a Post OR C to comment on a Post OR B to go back : ").upper()
    if opr == "L":
        like_post(user_id , post_id)
    elif opr == "C":
        comment_post(user_id , post_id)
    elif opr == "B":
        operations(user_id)
#_____________________________________________________________________________________________
def like_post(uid , post_id):
    payload = {'access_token':APP_ACCESS_TOKEN}
    requests_url = (BASE_URL + 'media/%s/likes' % (post_id))
    response_to_like = requests.post(requests_url, payload).json()

    if len(response_to_like):
        print "You ve' successfully liked that post !"
        operations(uid)

    else:
        print "Failed to like this Post !"
        operations(uid)

#_____________________________________________________________________________________________
def comment_post(uid , post_id):
    comment = raw_input("Comment here : ")
    payload = {'access_token': APP_ACCESS_TOKEN , 'text':comment}
    requests_url = (BASE_URL + 'media/%s/comments' % (post_id))
    response_to_comments = requests.post(requests_url, payload).json()

    if len(response_to_comments):
        print "You ve' successfully commented on that post !"
        operations(uid)

    else:
        print "Failed to comment on this Post !"
        operations(uid)




get_user_by_username()