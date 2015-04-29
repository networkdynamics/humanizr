#Files containing original common words lists (wrong format, too long)
COMMON_WORDS = '/home/jamie/dbpedia/common_words.csv'
COMMON_WORDS_TWITTER = '/home/jamie/dbpedia/common_words_twitter.txt'

#Given an extensive list of common words, takes the top num_words from the list, and returns the list.
def create_common_words_list(num_words, twitter):
	#Opens the appropriate file.
	if twitter:
		fin = open(COMMON_WORDS_TWITTER, 'r')
	else:
		fin = open(COMMON_WORDS, 'r')

	#List to be returned
	out_list = []

	#Depending on the input file, strips each line appropriately and returns a list of the num_words
	#most common words.
	c=0
	if twitter:
		for line in fin:
			if c<num_words:
				out_list.append('%s' % line.split('=')[0])
			else:
				break
			c+=1
	else:
		for line in fin:
			if c>0:
				if c<=num_words:
					out_list.append('%s' % line.split('\t')[0])
				else:
					break
			c+=1
	fin.close()
	return out_list
