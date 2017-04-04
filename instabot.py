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
    requests_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (user_name , APP_ACCESS_TOKEN)
    search_results = requests.get(requests_url).json()


    if len(search_results['data']) :
        print "User id : " + str(search_results['data'][0]['id'])
        print "Full name : " + str(search_results['data'][0]['full_name'])
        print "Bio : " + str(search_results['data'][0]['bio'])
        response = raw_input("Enter Y to perform operations or N to continue search : ").upper()
        if response == "Y":
            operations(search_results['data'][0]['id'])
        else:
            get_user_by_username()

    elif user_name == "q" or user_name == "Q":
        exit()
    else:
        print "User doesn't exists !"
        get_user_by_username()
    ''' if user_name not in user_list:
        if user_name == "q" or user_name == "Q":
            exit()
        else:
            print "User doesn't exists !"
            get_user_by_username()
    else:
        requests_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (user_name, APP_ACCESS_TOKEN)
        user_info = requests.get(requests_url).json()

        print "User id : " + str(search_results['data'][0]['id'])
        print "Full name : " + str(search_results['data'][0]['full_name'])
        print "Bio : " + str(search_results['data'][0]['bio'])'''


#_____________________________________________________________________________________________
def operations(user_id):
    requests_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    recent_posts =requests.get(requests_url).json()

    post_list = ["x"]
    for likes in recent_posts['data']:
            post_list.append(likes['id'])
            print "User_id : " + str(user_id) + " Post id: " + str(post_list.index(likes['id'])) + " likes :" + str(likes['likes']['count']) + " Comments : " +  str(likes['comments']['count'])

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
        select_operation(user_id, post_id)

#_____________________________________________________________________________________________
def select_operation(user_id , post_id):
    opr = raw_input("Enter L to like a Post \n  OR C to comment on a Post \n  OR D to Delete last comment \n  OR B to go back : ").upper()
    if opr == "L":
        like_post(user_id , post_id)
    elif opr == "C":
        comment_post(user_id , post_id)
    elif opr == "B":
        operations(user_id)
    elif opr == "D":
        select_the_way_to_delete_comment(user_id,post_id)
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
def select_the_way_to_delete_comment(user_id,post_id):
    response = raw_input("Enter W to delete comment by word OR M to delete comments manually OR B to go back :").upper()
    if response == "W":
        delete_comment_by_word(user_id,post_id)
    elif response == "M":
        delete_comment_manually(user_id,post_id)
    elif response == "B":
        operations(user_id)
    else:
        print "Invalid Input !"
        select_the_way_to_delete_comment(user_id,post_id)

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

# _____________________________________________________________________________________________
def delete_comment_by_word(user_id , post_id):
    word = raw_input("Enter word you want to search in comments :")
    requests_url = (BASE_URL + 'media/%s/comments?access_token=%s' % (post_id, APP_ACCESS_TOKEN))
    result = requests.get(requests_url).json()
    result2 = result['data']
    comment_list = []

    # Storing all the commenrt_id of comments containing word entered by user in a list "comment_list")
    for i in range(len(result2)):

        split = result2[i]['text'].split()

        if word in split:
            comment_list.append(result2[i]['id'])


    if len(comment_list):
        for i in comment_list:
            requests_url2 = (BASE_URL + 'media/%s/comments/%s?access_token=%s' % (post_id, i, APP_ACCESS_TOKEN))
            response = requests.delete(requests_url2).json()
        print str(len(comment_list)) + " Comment successfully deleted !"
        operations(user_id)
    else:
        print "No comments found for " + str(word)
        print "Comment not deleted !"
        operations(user_id)


#_____________________________________________________________________________________________
def delete_comment_manually(user_id,post_id):
    requests_url = (BASE_URL + 'media/%s/comments?access_token=%s' % (post_id,APP_ACCESS_TOKEN))
    fetch = requests.get(requests_url).json()
    c = 1
    for comments in fetch['data']:
        if len(comments['text']):
            print "comment id : " + str(c) + " " + "text : " + str(comments['text'])
        else:
            print "No comments to delete !"
            operations(user_id)
        c = c + 1
    comment_y = raw_input("Enter the comment id you wan't to Delete OR B to go Back  :")
    if comment_y == "b" or comment_y == "B":
        operations(user_id)
    else:

        comment_y = int(comment_y)

    comment_id =["x"]
    for x in fetch['data']:
        comment_id.append(x['id'])
    x = comment_id[comment_y]

    requests_url2 = (BASE_URL + 'media/%s/comments/%s?access_token=%s' % (post_id, x , APP_ACCESS_TOKEN))
    response = requests.delete(requests_url2).json()
    if len(response['meta']['code']) == "200":
        print "comment successfully deleted !"
        delete_comment_manually(user_id, post_id)
    else:
        print "Comment not deleted !"
        delete_comment_manually(user_id,post_id)

get_user_by_username()

