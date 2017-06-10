import praw
from credentials import *

# Main Reddit Auth, gives reddit.* 
# Everything Is stored in 'credentials'
# Get values from reddit dev area after
# Authorising your app with reddit
reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT,username=USER,password=PASS)

subreddit = reddit.subreddit('test')

# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
    print(submission.title)  # Output: the submission's title
    print(submission.score)  # Output: the submission's score
    print(submission.id)     # Output: the submission's ID
    print(submission.url)    # Output: the URL the submission points to
                             # or the submission's URL if it's a self post
