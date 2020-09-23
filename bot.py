import twitter
import praw
import time
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# To filter out all of the words that don't hold much meaning
# alone(articles, affirmatives, neutral adjectives and verbs)
# so they don't show up in the wordcloud
boringwords = ["the", "a", "she", "he", "is", "was", "should", "said", "people",
			   "have", "her", "his", "an", "i", "in", "they", "for"
			   ,"this", "you", "to", "are", "it", "that", "be", "with","on", "not", "but"
			   ,"as", "so", "we", "all", "at", "their", "if", "all", "their", "it's", "or"
			   , "out", "by", "what", "because", "get", "can", "one", "how", "would",
			   "and", "of", "have", "just", "them", "like", "my", "", "will", "no", "from", "up", "do", "who", "whom", "here", "don't",
			   "your", "now", "has", "go", "more", "about", "see", "me", "than", "should", "i'm", "going", "know", "make",
			   "never", "too", "even", "us", "every", "only", "some", "being", "why", "these", "then",
			   "been", "when", "our", "back", "there", "were", "into", "&x200b;", "over", "that's", "got", "they're", "&", "him", "am",
			   "yes", "yeah", "which", "also", ">", "really", "any", "much", "other", "most", "actually", "had", "sure", "everyone", "thing",
			   "isn't", "things", "aren't", "enough", "doesn't", "without", "i’ll", "where", "whoever", "something",
			   "think", "yet", "either" ]


#Variables
subreddit = "conservative"
numberofcomments = 100


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def transform_format(val):
    if val == 0:
        return 255
    else:
        return val


# APIs
api = twitter.Api(consumer_key='arDfIEpT8wrNZKtOUFBT6yXor',
                  consumer_secret='lBn3x91a3LUetRxp6eAmrcHuislVeA3rzyvIsnKbIgKWXm8Ybu',
                  access_token_key='1308796671363514370-P6O4sw4XY4mFRTbKTNirwsItGm5OTK',
                  access_token_secret='9jEu9mrJhMIFwPQomIpmrqxUladIT2HQjhRYSK3O4Lz5I')

reddit = praw.Reddit(client_id='RjprTHBXrucx7Q',
                     client_secret='uEQ_mU2Cv4lEXWmR2Iuw9s8ilmM',
					 user_agent='searches reddit(by u/derpoftheages)')


comments = []
i = 0
time_probed = time.strftime("%H:%M:%S %Z")
for comment in reddit.subreddit(subreddit).stream.comments():
	if i == numberofcomments:
		break
	comments.append(comment)
	i+=1

freq = {}
remove_char = ['?', ',', '.', ':', '*', '(', ')', '!', '"', '[', ']', '#', '~', '-', '$']

for j in range(len(comments)):
	comm3nt = comments[j].body.split()
	for k in (range(len(comm3nt))):
		current_word = comm3nt[k].lower()
		current_word = ''.join([x for x in current_word if x not in remove_char])
		if current_word not in boringwords and "http" not in current_word and not RepresentsInt(current_word):
			if current_word not in freq:
				freq[current_word] = 1
			else:
				freq[current_word] += 1

words = list(freq.keys())
w = sorted(words,key= lambda x: freq[x], reverse=True)
freqwords = ""
for i in range(len(words)):
	freqwords += (words[i] + ", ") * freq[words[i]]

wordcloud = WordCloud(collocations=False, max_font_size=50, max_words=50, background_color="black").generate(freqwords)
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

plt.savefig('wordcloud.png')
#
# api.PostUpdate("Here is a word cloud from " + "r/" + subreddit +" using the 'interesting' words from a " + str(numberofcomments) + " of the "
# 				   "most recent comments posted to the sub. These comments were found at " + time_probed + ".",
# 			   media= "wordcloud.png")
