import praw                 # Reddit python api wrapper
from credentials import *   # The bot credentials
import pickle               # For saving of info
import os.path              # For pickle file check
import time                 # For wait on exception

# Main Reddit Auth, gives reddit.* 
# Everything Is stored in 'credentials'
# Get values from reddit dev area after
# Authorising your app with reddit
reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,user_agent=USER_AGENT,username=USER,password=PASS)

#***** Other config *****#
# Set True if you want to only check 1 sub
useSubList = False
# Use this if you don't want to comment
dryRun = False
# Prints lines for a lot of things
debug = False
# Comment is in commenting function below
#************************#

# Key Configuration
subredditList = 'test' # Limited to 1 sub currently 
keywords = ['hl3', 'half-life 3', 'half life 3', 'hl3', 'half-life three', 'half life three'] # Keyword use is unlimited

# If pickle files don't exist, create them
# processedComments.p
if os.path.exists("processedComments.p") == False:
    blank = []
    print("Creating pickle file processedComments.p...")
    pickle.dump(blank, open("processedComments.p","wb"))
    print("Done.\n")
# disabledUsers.p
if os.path.exists("disabledUsers.p") == False:
    blank = []
    print("Creating pickle file disabledUsers.p...")
    pickle.dump(blank, open("disabledUsers.p","wb"))
    print("Done.\n")
# disabledSubs.p
if os.path.exists("disabledSubs.p") == False:
    blank = []
    print("Creating pickle file disabledSubs.p...")
    pickle.dump(blank, open("disabledSubs.p","wb"))
    print("Done.\n")
# release.p
if os.path.exists("release.p") == False:
    blank = 1497284412
    print("Creating pickle file release.p...")
    pickle.dump(blank, open("release.p","wb"))
    print("Done.\n")


# The check for useSubList var
if useSubList:
    subreddit = reddit.subreddit(subredditList)
else:
    subreddit = reddit.subreddit('all')

# Sets the release time for hl3
def releasestrf():
    if debug:
        print("Getting release time")
    releaseSeconds = pickle.load(open("release.p", "rb"))
    if debug:
        print("Settting release time")
    releaseSeconds += 2628288
    release = time.strftime("%b %Y", time.gmtime(releaseSeconds))
    if debug:
        print("Saving release time")
    pickle.dump(releaseSeconds, open("release.p","wb"))
    return(release)
    
# The reply comment function, call this is write a comment
def replyComment(comment):
    # Before writing comment check if it's allowed
    # Well it will be too late, but this is a better time interval
    checkDisabledRequests()
    # Set this to what you want your comment to be
    commentPhrase = "By mentioning Half-Life 3 you have delayed it by 1 Month. Half-Life 3 is now estimated for release in %s.\n___\n^I ^am ^a ^bot, ^this ^action ^was ^performed ^automatically. ^To ^disable ^WIHL3 ^on ^your ^sub ^please ^see ^/r/WhenIsHl3. ^To ^never ^have ^WIHL3 ^reply ^to ^your ^comments ^PM ^'!STOP'." % (releasestrf())
    if dryRun:
        print("\tDry run: replying to %s by %s" % (comment.id, comment.author.name))
    else:
        if debug:
            print("Attempting to reply to %s" % (comment.id))
            print(commentPhrase)
        comment.reply(commentPhrase)
        print("Replied to " + comment.id)
        if debug: 
            print("Reply Success")

def checkDisabledRequests():
    if debug:
        print("Checking messages for stop requests")
    for item in reddit.inbox.all(limit=None):
        if debug:
            print("Does body == !STOP")
            print(repr(item.body) == "'!STOP'")
        if repr(item.body) == "'!STOP'":
            print("Matched message with !STOP")
            # Loads pickle file for disabled users
            disabledUsers = pickle.load(open("disabledUsers.p", "rb"))
            if repr(item.author.name).replace("'","") not in disabledUsers:
                disabledUsers.append(repr(item.author.name).replace("'",""))
                pickle.dump(disabledUsers, open("disabledUsers.p","wb"))
                print("Added %s to disabledUsers" % (repr(item.author.name)))
                item.reply("Added %s to disabled user list" % (repr(item.author.name)))
            else:
                if debug:
                    print("Found stop match, but already processed")
        subArray = repr(item.body).replace("'","").split("@")
        if debug:
            print("^^^")
            print(subArray)
        if len(subArray) == 2:
            if debug:
                print("len is 2")
            else:
                print("Wrong length")
            if subArray[0] == '!STOP':
                subToDisable = subArray[1].replace("/r/","")
                # Get rid of possible /r/
                if debug:
                    print("SubArray: ")
                    print(subArray)
                    print("subToDisable: " + subToDisable)
                for moderator in reddit.subreddit(subToDisable).moderator():
                    print(moderator)
                    if moderator == repr(item.author.name).replace("'",""):
                        # Loads pickle file for disabled subs
                        disabledSubs = pickle.load(open("disabledSubs.p", "rb"))
                        if subToDisable not in disabledSubs:
                            disabledSubs.append(subToDisable)
                            pickle.dump(disabledSubs, open("disabledSubs.p","wb"))
                            print("Added %s to disabledSubs" % (subToDisable))
                            item.reply("%s moved to disabled list" % (subToDisable))
                        else:
                            if debug:
                                print("Found subToDisable match, but already processed")
                    else:
                        if debug:
                            print("Moderator %s did not match %s" % (moderator, repr(item.author.name)))

                


# The not-so-grand finale
# The main loop
def findKeyword():
    for comment in subreddit.stream.comments():
        for key in keywords:
            # Checks for keywords in the comment body
            if key in comment.body.lower():
                if debug:
                    print("Matched keyword:%s in comment: %s" % (key, comment.id)) 
                # Checks for already processed comments
                processedComments = pickle.load(open("processedComments.p", "rb"))
                if comment.id not in processedComments:
                    # Loads pickle file for disabled users
                    disabledUsers = pickle.load(open("disabledUsers.p", "rb"))
                    if debug:
                        print("Comparing comment author: %s with disabled user list" % (comment.author.name.replace("'","")))
                        print(disabledUsers)
                    # Checks for opt-outed users
                    if comment.author.name.replace("'","") not in disabledUsers:
                        # Loads pickle file for disabled subs
                        disabledSubs = pickle.load(open("disabledSubs.p", "rb"))
                        # Checks for opt-outed subs
                        if comment.subreddit.name not in disabledSubs:
                            print("Processing %s from match '%s'..." % (comment.id, key))
                            replyComment(comment) 
                            
                            # Writes comment id to pickle file
                            processedComments.append(comment.id)
                            if debug:
                                print("Writing comment id: %s to pickle" % (comment.id))
                            # Uses pickle to save the array
                            pickle.dump(processedComments, open("processedComments.p","wb"))
                            if debug:
                                print("Saved pickle")
                        else:
                            if debug:
                                print("Comment id:%s matched but sub %s disabled" % (comment.id, comment.subreddit.name))
                    else:
                        if debug:
                            print("Comment id:%s matched but user %s disabled" % (comment.id, comment.author.name))
                else:
                    if debug:
                        print("Comment %s was matched with a record for an already processed comment" % (comment.id))





for i in range(100):
    try:
        print("Program starting.\nDebug: %s\nDry Run: %s\nUsing Sub List: %s" % (debug, dryRun, useSubList))
        print("-----\n")
        findKeyword()
    except KeyboardInterrupt:
        print("Keyboard Interrupt sent. Closing...")
        exit(0)
    except praw.exceptions.APIException:
        print("PRAW commenting too much, waiting 2 minutes to retry")
        time.sleep(120)
        pass
    except:
        print("Exception raised, waiting 2 minutes...")
        time.sleep(120)
        pass
