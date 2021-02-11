"""
-------------------------------------------------------
Main file / entry point to reddit keyword generator
-------------------------------------------------------
Author:  Andrei Secara
Email:   andreisecara01@gmail.com
__updated__ = "2019-04-27"
-------------------------------------------------------
"""
from Word_Class import *
from Popularity_Tree import *
import praw
import re

# API secret and other credentials are stored in text file "credentials.txt" to prevent privacy issues while distrubuting the program
# To Use this application, generate your own API key using these instructions: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

fp = open("credentials.txt", "r") # File pointer to credentials.txt Used to import credentials

# Order of credentials in file (seperated by newline): client_id, client_secret, user_agent, username, password

credentialList = [None] * 5 # List to temp store credentials loaded from file


# Set number of top subreddit posts to analyze. As well, number of comments to analyze per post. Keep in mind that the more subreddits to analyze
# the longer it will take, and the more memory instensive it will be.
postLimit = 1
commentsLimit = 10

WORDFILENAME = "words.txt"
TOPWORDSNUMBER = 10

# Used for iteration and counting
i = 0

# DELIMMITERS TO USE WHILE PARSING TEXT
delims = r"[\w']+"


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
subredditString = "learnpython"
subred = reddit.subreddit(subredditString)

top = subred.top(limit = postLimit)
print("\nConnection Successful ... Analyzing subreddit: '{}' \n".format(subredditString))


# Create dictionairy to store words
wordscount = {}


# storage_file = open(WORDFILENAME, "w")

# TOTAL NUMBER OF WORDS ANALYZED
totalcount = 0
# Time to iterate through each 
for post in top:
    
    # Reset memory storage every post to save memory
    wordList = []

    titleWordList = []
    titleString = ""
    
    bodyWordList = []
    bodyString = ""
    
    commentWordList = []
    commentString = ""
    
    
    print("Analyzing post: " + str(post.title))
    
    # First, read title
    titleString = post.title
    titleWordList = re.findall(delims, titleString)
    
    # Second, read post text
    bodyString = post.selftext
    bodyWordList = re.findall(delims, bodyString)
    
    
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        commentString = comment.body
        commentWordList = commentWordList + re.findall(delims, commentString)
        
    
    # Concatenate all words from post into a single list to append to file
    wordList = titleWordList + bodyWordList + commentWordList
    
    # Write all words to a storage file to save memory (analyzing thousands of posts could
    # exceed memory capacity of some systems. Also more secure in case of system shutdown.
#     wordNumber = 1
#     maxWordsPerLine = 10
    # Wordnumber is here to keep track of how many words are written per line
    for w in wordList:
#         if wordNumber == maxWordsPerLine:
#             storage_file.write("\n") # Create a new line to write another line of words
#             wordNumber = 1 # Reset word number counter back to one
        if  w.isalpha() and w not in english_words_list:
            if w not in wordscount:
                wordscount[w] = 1
            else:
                wordscount[w] += 1
#             storage_file.write(w.lower() + " ")
            totalcount += 1
        
#         wordNumber += 1

    
# storage_file.close()







print("Total word count: %s" %(totalcount))


