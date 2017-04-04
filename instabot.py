''' This is instabot made by Sumit Pandey , Here you can do various things such as :
    1 --> Check your Profile
    2 --> like a post
    3 --> comment on a post
    4 --> delete a comment as well as multiple comments by searching comments by words
    5 --> Find Average number of words per comment on a post
'''
import requests # Requests library imported to perform different queries such as get , post , delete ,put


APP_ACCESS_TOKEN = "2096873226.ed76845.d26be842838e497097d368aff4ed72ac" # This is access token provided by www.instagram.com/developer/

BASE_URL = "https://api.instagram.com/v1/" # This is a common portion of a url which we gonna use again and again


#_____________________________________________________________________________________________
#This Function Prints the Users Profile Info
def self_info():
    requests_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN) # this is a URL requesting to fetch users information
    my_info = requests.get(requests_url).json() #This is json response recieved from the instagram API

    print "Name :" + str(my_info['data']['full_name'])
    print "Bio :" + str(my_info['data']['bio'])
    print "Followers :" + str(my_info['data']['counts']['followed_by'])

    get_user_by_username()

#_____________________________________________________________________________________________
#this Function search the username to perform operations
def get_user_by_username():
    user_name = raw_input("Enter Username  you wants to Search  OR 9 to Check your profile  OR Q to quit : ") # Asking user to type username
    requests_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (user_name , APP_ACCESS_TOKEN)
    search_results = requests.get(requests_url).json()


    if len(search_results['data']) :
        print "User id : " + str(search_results['data'][0]['id'])
        print "Full name : " + str(search_results['data'][0]['full_name'])
        print "Bio : " + str(search_results['data'][0]['bio'])
        response = raw_input("Enter Y to perform operations or N to continue search : ").upper()
        if response == "Y":
            operations(search_results['data'][0]['id']) # Assuming that there 'll be only one result because of unique usernames on Instagram
        else:
            get_user_by_username()
    elif user_name == "9" :
        self_info()

    elif user_name == "q" or user_name == "Q":
        exit()
    else:
        print "User doesn't exists !"
        get_user_by_username()


#_____________________________________________________________________________________________
#This Function fetches the information of the selected username to perform further operations
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
        x = int(post_id) #converting post_id into integer so that It can be searched in the Post_list

    if post_list[x] not in post_list:
        print "Invalid Post id !"
        operations(user_id)
    else:
        post_id = post_list[x]
        select_operation(user_id, post_id)

#_____________________________________________________________________________________________
#This function helps user to select the desired operation
def select_operation(user_id , post_id):
    opr = raw_input("Enter L to like a Post \n  OR C to comment on a Post \n  OR D to Delete comment \n  OR A to find average number of words per comment \n  OR B to go back : ").upper()
    if opr == "L":
        like_post(user_id , post_id)
    elif opr == "C":
        comment_post(user_id , post_id)
    elif opr == "B":
        operations(user_id)
    elif opr == "D":
        select_the_way_to_delete_comment(user_id,post_id)
    elif opr == "A":
        Average_number_of_words(user_id,post_id)
#_____________________________________________________________________________________________
#This Fuction likes the post selected by user
def like_post(uid , post_id):
    payload = {'access_token':APP_ACCESS_TOKEN}
    requests_url = (BASE_URL + 'media/%s/likes' % (post_id))
    response_to_like = requests.post(requests_url, payload).json() # post request is used to send data

    if len(response_to_like):
        print "You ve' successfully liked that post !"
        operations(uid)

    else:
        print "Failed to like this Post !"
        operations(uid)


#_____________________________________________________________________________________________
# This function is to select the way to delete comment i.e either by searching a specific word or by selecting the comment manually
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
#This Function is to comment on a specific post
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
#This function deletes multiple comments containing a single word entered by user
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
# This Function deletes the comment manually by selecting a comment from the all comments
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



#_____________________________________________________________________________________________
# This Function finds the average number of words per comment on a post
def Average_number_of_words(user_id , post_id):
    requests_url = (BASE_URL + 'media/%s/comments?access_token=%s' % (post_id, APP_ACCESS_TOKEN))
    fetch = requests.get(requests_url).json()
    c = 1
    av = 0
    if len(fetch['data']) > 0:

        for comments in fetch['data']:
            if len(comments['text']):
                print "comment id : " + str(c) + " " + "text : " + str(comments['text'])
                x1 = comments['text'].split()
                k = 0
                for i in x1:
                    k = k +1
                av = av + k

            c = c + 1
        total_words = av
        total_comments = c - 1
        Average = total_words / total_comments
        print "Average number of words per comment is : " + str( Average)
        operations(user_id)
    else:
        print "No comments found !"
        operations(user_id)




get_user_by_username()# Calling a function .

