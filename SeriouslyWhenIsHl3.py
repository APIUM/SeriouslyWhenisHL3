import praw
from credentials import *
import threading

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

# Main ugly loop
subreddit = reddit.subreddit('all')

# GO to comments
# This starts iterating through every comment 
# Try is to close the files upon quit
def replyToKeyword():
    try:
        for comment in subreddit.stream.comments():
            for key in keywords:
                # Checks for keywords in the comment body
                if key in comment.body.lower():
                    # Checks for already processed comments
                    if comment.id not in fCommented.read():
                        # Checks for opt-outed users
                        if comment.author.name not in fDisabledUsers.read():
                            # Checks for opt-outed subs
                            if comment.subreddit.name not in fDisabledSubs.read():
                                print("***********FOUND***********")
                                print(key)
                                print(comment.author.name)
                                
                                # Writes comment id to processed comments doc
                                faCommented.write(comment.id+'\n')
    except KeyboardInterrupt:
        faCommented.close()
        fDisabledUsers.close()
        fDisabledSubs.close()

threading.Thread().start()
