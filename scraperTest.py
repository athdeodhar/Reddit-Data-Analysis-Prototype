import praw
import re
from praw.models import MoreComments

#Personal Use Script: ScyKOYnB5NWpdQ
#Secret Key: rNq7jDY009QSExpSNlH4xarZH3U

reddit = praw.Reddit(client_id = 'ScyKOYnB5NWpdQ',
                     client_secret = 'rNq7jDY009QSExpSNlH4xarZH3U',
                     user_agent = 'One Piece Score Scraper',
                     username = 'PineappleThePhoenix',
                     password = 'p455w0rd')

submission = reddit.submission(id='d9vxbl')

comments = []
dictionary = {}
words = []
for top_level_com in submission.comments:
    if isinstance(top_level_com, MoreComments):
        continue
    translation_table = dict.fromkeys(map(ord, '!@#$":;`~_[]{}|,<->*.'), None)
    text = top_level_com.body
    text = text.translate(translation_table)
    comments.append(text.lower())

for com in comments:
    com = com.strip()
    temp_list = re.split("\\s+", com)
    words += temp_list

for key in words:
    if key in dictionary:
        dictionary[key] += 1 
    else:
        dictionary[key] = 1


for w in sorted(dictionary, key=dictionary.get, reverse=True):
  print(w, dictionary[w])

 

    
