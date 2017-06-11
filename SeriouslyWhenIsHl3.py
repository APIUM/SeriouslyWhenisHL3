import praw
from credentials import *

# Main Reddit Auth, gives reddit.* 
# Everything Is stored in 'credentials'
# Get values from reddit dev area after
# Authorising your app with reddit
reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT,username=USER,password=PASS)

# Key Configuration
subredditList = ['test', 'python']
keywords = ['trump','and']

# File config
fCommented = open('commented', 'r')
faCommented = open('commented', 'a')

fDisabledUsers = open('disabledUsers', 'r')

fDisabledSubs = open('disabledSubs', 'r')

for i in range (0,len(subredditList)):
    #subreddit = reddit.subreddit(subredditList[i])
    subreddit = reddit.subreddit('all')

    # assume you have a Subreddit instance bound to variable `subreddit`
    for submission in subreddit.stream.submissions():
        #print("___________")
        print(submission.id)     # Output: the submission's ID
        #print(submission.url)    # Output: the URL the submission points to
        #print(submission.subreddit)
                                 # or the submission's URL if it's a self post
    
    # GO to comments
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            for key in keywords:
                if key in comment.body.lower():
                    if comment.id not in fCommented.read():
                        if comment.author.name not in fDisabledUsers.read():
                            if comment.subreddit.name not in fDisabledSubs.read():
                                print("***********FOUND***********")
                                print(key)
                                
                                faCommented.write(comment.id+'\n')
                        
