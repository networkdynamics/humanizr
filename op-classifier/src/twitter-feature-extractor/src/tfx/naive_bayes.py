#http://norvig.com/ngrams/ - most common words

import json
import math
import sys
import string
from modify_common_words import create_common_words_list

WORD_COUNTS = 'word_counts.txt'
CAT_COUNTS = 'cat_counts.txt'

"""
Naive Bayes Classifier

This Naive Bayes Classifier is to be used for determining the category of an
organizational twitter account. It uses word frequencies to determine a score
for each category for each account and the category which receives the highest
score is the decided label for the organization.

This was constructed following the instructions on this page:
https://www.bionicspirit.com/blog/2012/02/09/howto-build-naive-bayes-classifier.html

Note***
The frequency of each category was assumed to be equal so was ommitted from the
score equation. This should probably be changed at some point. Also, common words
from a list of most common words can be ommitted.
"""

class NaiveBayesClassifier:

	#Initializes the object variables. n is the number of most common words to be ignored
	#when training and classifying.
	def initialize(self, n, cat_list, twitter=False):

		#Dictionary storing specific word counts for each category.
		self.words = {}
		#Dictionary storing total word counts for each category.
		self.categories = {}
		for cat in cat_list:
			self.words[cat] = {}
			self.categories[cat] = 0
		
		#List of most common words (number of words specified by user)
		self.common = create_common_words_list(n, twitter)
		#List of English punctuation, to be stripped from words before counting.
		self.punc_table = (string.punctuation, "")
		#self.punc_table = (string.punctuation+'0123456789', "")

	#Given a category (cat) and a string of text (text), counts words and stores them in
	#the dictionary under cat.
	def train(self, cat, text):		
		for word in text.split():
			#Changes capital letters to lower case and removes punctuation from words
			word = word.lower()
			word = word.translate(self.punc_table)
			try:
				if len(word)>0:
					try:
						self.words[cat][word] += 1
					except KeyError:
						self.words[cat][word] = 1
					self.categories[cat] += 1
			except:
				pass

	#Writes the dictionaries storing words counts to file.
	def save_dictionaries(self):
		#writes back to the specific word count json file
		outfile = open(WORD_COUNTS, 'w')
		json.dump(self.words, outfile)
		outfile.close()
		#writes back to the total word count json file
		outfile = open(CAT_COUNTS, 'w')
		json.dump(self.categories, outfile)
		outfile.close()

	#Loads the dictionaries storing words counts and the list of most common words.
	def load_dictionaries(self, n, twitter):
		#loads the dictionary of specific word counts
		json_words=open(WORD_COUNTS)
		self.words = json.load(json_words)
		json_words.close()
		#loads the dictionary of total word counts
		json_cats=open(CAT_COUNTS)
		self.categories = json.load(json_cats)
		json_cats.close()
		#Loads the list of most common words to ignore.
		self.common = create_common_words_list(n, twitter)
		print '%d most common words ignored.' % (len(self.common))

	#Uses the Naive bayes formula and word counts to determine a score for each category
	#the inputted text string. Returns a dictionary whose keys are made up of the list
	#of categories and whose values correspond to the score for the given category.
	def classify(self, text):
		#Dictionary containing results to be returned
		result = {}	
	
		#make sure string is in ascii
		if isinstance(text, unicode):
			text = text.encode('ascii', 'xmlcharrefreplace')	
		else:
			text = text.decode('utf8').encode('ascii', 'xmlcharrefreplace')	

		#Tallies the total number of words
		total = 0
		for cat in self.categories.keys():
			total += self.categories[cat]
	
		#Calculates the score for each category for the inputted text
		for cat in self.categories.keys():
			score = 0
			for word in text.split():
				#Capital letters changed to lower case, punctuation removed.
				word = word.lower()
				word = word.translate(None, string.punctuation)
				#word = word.translate(None, string.punctuation+'0123456789')
				if len(word)>0:
					if word not in self.common:
						try:
							if self.words[cat][word] > 1:
								#Follows the Bayesian formula provided in the article referenced at the top of this class
								score += math.log(float(self.words[cat][word])/float(self.categories[cat]))
							else:
								#score if the word is not in the dictionary
								score += math.log(float(0.5)/float(total))
						except KeyError:
							#score if the word is not in the dictionary
							score += math.log(float(0.5)/float(total))
			result[cat] = score
		return result



