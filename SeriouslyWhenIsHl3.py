import praw
from credentials import *
import threading
import sys

# Main Reddit Auth, gives reddit.* 
# Everything Is stored in 'credentials'
# Get values from reddit dev area after
# Authorising your app with reddit
reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT,username=USER,password=PASS)

# Other config
useSubList = True
dryRun = True
commentPhrase = "You have said somthing of note"

# Key Configuration
subredditList = 'test' # Limited to 1 sub currently 
keywords = ['trump','and'] # Keyword use is unlimited

# File config
fCommented = open('commented', 'r')
faCommented = open('commented', 'a')
fDisabledUsers = open('disabledUsers', 'r')
fDisabledSubs = open('disabledSubs', 'r')

processedComments = []

# Main ugly loop
if useSubList:
    subreddit = reddit.subreddit(subredditList)
else:
    subreddit = reddit.subreddit('all')
    

def replyComment(comment):
    if dryRun:
        print("\tDry run: replying to %s by %s" % (comment.id, comment.author.name))
    else:
        comment.reply(commentPhrase)
    
    
def parseCommented():
    with open('commented', 'r') as comList:
        for line in comList:
            processedComments.append(line)

# GO to comments
# This starts iterating through every comment 
# Try is to close the files upon quit

def findKeyword():
    for comment in subreddit.stream.comments():
        for key in keywords:
            # Checks for keywords in the comment body
            if key in comment.body.lower():
                # Checks for already processed comments
                parseCommented()
                if comment.id not in processedComments:
                    # Checks for opt-outed users
                    if comment.author.name not in fDisabledUsers.read():
                        # Checks for opt-outed subs
                        if comment.subreddit.name not in fDisabledSubs.read():
                            print("Processing %s from match '%s'..." % (comment.id, key))
                            replyComment(comment) 
                            
                            # Writes comment id to processed comments doc
                            faCommented.write(comment.id+'\n')





try:
    findKeyword()
except KeyboardInterrupt:
    print("Interupted")
    print("Closing Files")
    faCommented.close()
    fCommented.close()
    fDisabledUsers.close()
    fDisabledSubs.close()
    pass
finally:
    faCommented.close()
    fDisabledUsers.close()
    fDisabledSubs.close()
