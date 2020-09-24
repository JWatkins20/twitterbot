import twitter
import praw
import time
import threading
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# To filter out all of the words that don't hold much meaning
# alone(articles, affirmatives, neutral adjectives and verbs)
# so they don't show up in the wordcloud
subreddits = ["politics",
"futurology",
"neoliberal",
"wayofthebern",
"worldpolitics",
"socialism",
"conspiracy",
"conservative",
"politicaldiscussion",
"sandersforpresident",
"anarcho_capitalism",
"libertarian",
"democrats",
"republican",
"politicalhumor",
"atheism",
"blackpeopletwitter",
"latestagecapitalism",
"political_revolution",
"progressive",
"nottheonion"]



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
numberofcomments = 100

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# APIs
api = twitter.Api(consumer_key='arDfIEpT8wrNZKtOUFBT6yXor',
                  consumer_secret='lBn3x91a3LUetRxp6eAmrcHuislVeA3rzyvIsnKbIgKWXm8Ybu',
                  access_token_key='1308796671363514370-P6O4sw4XY4mFRTbKTNirwsItGm5OTK',
                  access_token_secret='9jEu9mrJhMIFwPQomIpmrqxUladIT2HQjhRYSK3O4Lz5I')

reddit = praw.Reddit(client_id='RjprTHBXrucx7Q',
                     client_secret='uEQ_mU2Cv4lEXWmR2Iuw9s8ilmM',
					 user_agent='searches reddit(by u/derpoftheages)')


class Thread(threading.Thread):
	def __init__(self, subreddit):
		threading.Thread.__init__(self)
		self.subreddit = subreddit

	def run(self):
		getCommentsAndPostWordCloud(self.subreddit)

def getCommentsAndPostWordCloud(subreddit):
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
	freqwords = ""
	for i in range(len(words)):
		freqwords += (words[i] + ", ") * freq[words[i]]

	wordcloud = WordCloud(width=800, height=400, collocations=False, max_font_size=100, max_words=50, background_color="black").generate(freqwords)
	plt.figure(figsize=(20,10), facecolor='k')
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad=0)
	plt.savefig('wordcloud.png')

	api.PostUpdate("Here is a word cloud from www.reddit.com/r/" + subreddit +" using the 'interesting' words from a " + str(numberofcomments) + " of the "
					"most recent comments posted to the sub. These comments were found at " + time_probed + ".",
				   media= "wordcloud.png")

#Main

#select five random indices
random_indices = random.sample(range(0, 21), 5)
p = 0
t = time.time()
for i in random_indices:
	selected_sub = subreddits[i]
	getCommentsAndPostWordCloud(selected_sub)



