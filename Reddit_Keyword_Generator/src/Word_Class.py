"""
-------------------------------------------------------
Class containing functions to work with word objects.
-------------------------------------------------------
Author:  Andrei Secara
Email:   andreisecara01@gmail.com
__updated__ = "2019-04-27"
-------------------------------------------------------
"""

class Reddit_Word:
    
    """
    INITS A NEW WORD
    """
    def __init__(self, name, subreddit):
        self.name = name
        self.count = 0
        self.percentcount = 0
        self.subreddit = subreddit
        
    """
    UPDATES WORD NAME
    """
    def change_name(self, name):
        self.name = name
    
    """
    INCREMENTS COUNT OF WORD
    """
    def increment_count(self):
        self.count += 1
    
    """
    SETS COUNT OF WORD
    """
    def set_count(self, count):
        self.coun = count
        
    """
    SETS SUBREDDIT
    """
    def set_subreddit(self, subreddit):
        self.subreddit = subreddit 
        
    """
    SETS % COUNT
    """
    def set_percent_count(self, value):
        self.percentcount = value