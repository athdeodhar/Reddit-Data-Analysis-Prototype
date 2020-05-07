'''
This program takes a start and end date and a subreddit name as input,
finds all of the posts fitting the criteria, and processes the data
'''
import praw
import re
from praw.models import MoreComments

f = open("stopwords.txt", "r")
contents = f.read()
arr = contents.split("\n\n")
stopwords = set(arr)

translation_table = dict.fromkeys(map(ord, '?!@+=()&^#$":;`~_[]{}|,<->*.'), None)
posts = 0
def processComment(comment):
    comments = []
    text = comment.body 
    text = text.translate(translation_table)
    comments.append(text.lower())

    for com in comment.replies:
        if isinstance(com, MoreComments):
            continue
        comments.extend(processComment(com))

    return comments

def processSubmission(submission):
    words = []
    comments = []
    comments.append(submission.title.translate(translation_table).lower())
    comments.append(submission.selftext.translate(translation_table).lower())
    for top_level_com in submission.comments:
        if isinstance(top_level_com, MoreComments):
            continue
        comments.extend(processComment(top_level_com))
    return comments

reddit = praw.Reddit(client_id = 'ScyKOYnB5NWpdQ',
                     client_secret = 'rNq7jDY009QSExpSNlH4xarZH3U',
                     user_agent = 'One Piece Score Scraper',
                     username = 'PineappleThePhoenix',
                     password = 'p455w0rd')

subredditName = "india"
subreddit = reddit.subreddit(subredditName)

sortby = "hot"
submissions = eval("subreddit.{}".format(sortby))

timeframe = "all"
maincomments = []

if sortby == "hot":
    for submission in submissions():
        maincomments.extend(processSubmission(submission))
else:
    for submission in submissions(timeframe):
        maincomments.extend(processSubmission(submission))

words = []
dictionary = {}

for com in maincomments:
    com = com.strip()
    temp_list = re.split("\\s+|\'", com)
    temp_list = [x for x in temp_list if x not in stopwords]
    words.extend(temp_list)

    
for key in words:
    if key in dictionary:
        dictionary[key] += 1 
    else:
        dictionary[key] = 1
for w in sorted(dictionary, key=dictionary.get, reverse=True):
    print(w, dictionary[w])
