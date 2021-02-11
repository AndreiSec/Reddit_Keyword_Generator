"""
-------------------------------------------------------
Main file / entry point to reddit keyword generator
-------------------------------------------------------
Author:  Andrei Secara
Email:   andreisecara01@gmail.com
__updated__ = "2019-04-27"
-------------------------------------------------------
"""
import collections
import pandas as pd
import matplotlib.pyplot as plt 
import praw
import re
from gc import collect
from matplotlib.axis import XAxis

# API secret and other credentials are stored in text file "credentials.txt" to prevent privacy issues while distrubuting the program
# To Use this application, generate your own API key using these instructions: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

fp = open("credentials.txt", "r") # File pointer to credentials.txt Used to import credentials

# Order of credentials in file (seperated by newline): client_id, client_secret, user_agent, username, password
credentialList = [None] * 5 # List to temp store credentials loaded from file


# Set number of top subreddit posts to analyze. As well, number of comments to analyze per post. Keep in mind that the more subreddits to analyze
# the longer it will take, and the more memory instensive it will be.
#THESE VALUE WILL BE SET BY USER ON WEBSITE
postLimit = 5
commentsLimit = 10

#THIS VALUE WILL BE SET BY USER ON WEBSITE
NUMBEROFWORDSTOPRINT = 10

# Used for iteration and counting
i = 0

# DELIMMITERS TO USE WHILE PARSING TEXT
delims = r"[\w']+"

"""
FOR THE WEBSITE, THE USER CAN DEFINE A LIST OF STOP WORDS!
"""
# Load list of common english words into array to use 
en_words_fp = open("common_english_words.txt", "r")
l = en_words_fp.readline() # Read first and only line of text document
english_words_list = l.split(",") # Insert words into an array of strings
en_words_fp.close()

for line in fp:
    line = line.strip('\n')
    line = line.strip('\t')
    credentialList[i] = str(line)
    i += 1
   
print("PRAW Reddit login credentials: \n")
for x in credentialList:
    print(x)

fp.close()

# Create praw reddit instance
reddit = praw.Reddit(
    client_id=credentialList[0],
    client_secret=credentialList[1],
    password=credentialList[4],
    user_agent=credentialList[2],
    username=credentialList[3],
)


# subredditString = input("Please enter the subreddit you wish to analyze: ")
# subredditString= subredditString.strip('\n')
subredditString = "wallstreetbets"
poststype = "rising"

subred = reddit.subreddit(subredditString)

if poststype == "top":
    subredditposts = subred.top(limit = postLimit)
elif poststype == "hot":
    subredditposts = subred.hot(limit = postLimit)
elif poststype == "new":
    subredditposts = subred.new(limit = postLimit)
elif poststype == "rising":
    subredditposts = subred.rising(limit = postLimit)




print("\nConnection Successful ... Analyzing subreddit: '{}' \n".format(subredditString))


# Create dictionairy to store words
wordscount = {}


# storage_file = open(WORDFILENAME, "w")

# TOTAL NUMBER OF WORDS ANALYZED
totalcount = 0
# Time to iterate through each 
for post in subredditposts:
    
    # Reset memory storage every post to save memory
    wordList = []

    titleWordList = []
    titleString = ""
    
    bodyWordList = []
    bodyString = ""
    
    commentWordList = []
    commentString = ""
    
    try:
        print("Analyzing post: " + str(post.title))
    except:
        print("Analyzing post: TITLE UNABLE TO BE READ. Most likely contains emojis.")
    
    # First, read title
    titleString = post.title
    titleWordList = re.findall(delims, titleString)
    
    # Second, read post text
    bodyString = post.selftext
    bodyWordList = re.findall(delims, bodyString)
    
    
    post.comments.replace_more(limit=commentsLimit)
    for comment in post.comments.list():
        commentString = comment.body
        commentWordList = commentWordList + re.findall(delims, commentString)
        
    
    # Concatenate all words from post into a single list to append to file
    wordList = titleWordList + bodyWordList + commentWordList
    
    print("Word List Generated for post generated... Filling dictionary")
    for w in wordList:
        if  w.isalpha() and w.lower() not in english_words_list:
            if w.lower() not in wordscount:
                wordscount[w.lower()] = 1
            else:
                wordscount[w.lower()] += 1
            totalcount += 1


word_counter = collections.Counter(wordscount)

for word, count in word_counter.most_common(NUMBEROFWORDSTOPRINT):
    print("%s : %d : %.2f" % (word, count, (count*100/totalcount)), end="")
    print("%")



# Create a data frame of the most common words 
# Draw a bar chart
lst = word_counter.most_common(NUMBEROFWORDSTOPRINT)
df = pd.DataFrame(lst, columns = ['Word', 'Count'])
df.plot(x="Word", y="Count", kind="bar")
plt.show()


print("Total word count: %s" %(totalcount))


