import collections
import inspect
import re
import string

from tfx import lovins


alphabetic_re = re.compile('[a-zA-Z]')
mention_re = re.compile('(?P<mention>\w+)')
hashtag_re = re.compile('(?P<hashtag>\w+)')
link_re = re.compile('http:\/\/[^ ]+')

exclude_punctuation = set(string.punctuation)

tweet_extractors = {}
profile_extractors = {}
other_extractors = {}


class EntityExtractorBase:
    entity = None



"""
Tweet extractors defined here - used for every single tweet
Take in either the cleaned message (without hashtags, urls, etc) or the
    original message.
"""

class TweetExtractorBase(EntityExtractorBase):
    register = tweet_extractors
    needs_clean = True # whether or not it needs the cleaned tweet

    def initialise_for_user(self):
        self.entities = []

    def get_user_entities(self):
        counter = collections.defaultdict(int)
        for entity in self.entities:
            counter[entity] += 1
        return counter

    def get_tweet_entities(self, message, cleaned_message, timestamp):
        text = cleaned_message if self.needs_clean else message 
        self.entities.extend(self.process_text(text))


class WordExtractor(TweetExtractorBase):
    entity = 'words'

    def process_text(self, text):
	text = ''.join(ch for ch in text.lower() if ch not in exclude_punctuation)
        return filter(len, text.split(' '))


class DigramExtractor(TweetExtractorBase):
    entity = 'digrams'

    def process_text(self, text):
	text = ''.join(ch for ch in text.lower() if ch not in exclude_punctuation)
        text = ' %s ' % text
        digrams = []

        for i in xrange(len(text) - 1):
            digram = '%c%c' % (text[i], text[i+1])
            if digram != '  ':
                digrams.append(digram)
        
        return digrams


class TrigramExtractor(TweetExtractorBase):
    entity = 'trigrams'

    def process_text(self, text):
	text = ''.join(ch for ch in text.lower() if ch not in exclude_punctuation)
        text = ' %s ' % text
        trigrams = []

        for i in xrange(len(text) - 2):
            trigram = '%c%c%c' % (text[i], text[i+1], text[i+2])
            trigrams.append(trigram)

        return trigrams


class StemExtractor(TweetExtractorBase):
    entity = 'stems'

    def process_text(self, text):
	text = ''.join(ch for ch in text.lower() if ch not in exclude_punctuation)
        return map(lovins.stem, filter(len, text.split(' ')))


class CostemExtractor(TweetExtractorBase):
    entity = 'costems'

    def process_text(self, text):
        words = ''.join(ch for ch in text.lower() if ch not in exclude_punctuation).split(' ')

        # Get the length of the stems for all the words
        stem_lengths = map(len, map(lovins.stem, filter(len, words)))
        return [word[stem_length:] for word, stem_length in zip(words, stem_lengths)]


class HashtagExtractor(TweetExtractorBase):
    entity = 'hashtags'
    needs_clean = False

    def process_text(self, text):
        words = text.lower().split(' ')
        hashtags = []
        for word in words:
            if len(word) > 1 and word[0] == '#':
                # Only match the first group of alphanumeric characters (AND IGNORE IF THERE ARE NO ALPHABETIC CHARACTERS)
                # This stupidly strips out things like 2012 but ... whatever? idk
                if alphabetic_re.search(word):
                    try:
                        hashtags.append(hashtag_re.match(word[1:]).group('hashtag'))
                    except AttributeError:
                        # If there is no hashtag found, do nothing?
                        pass

        return hashtags 


class MentionExtractor(TweetExtractorBase):
    entity = 'mentions'

    def process_text(self, text):
        words = text.lower().split(' ')
        mentions = []
        for word in words:
            if len(word) > 1 and word[0] == '@':
                # Take only alphanumeric characters and underscores (as per twitter's username policy)
                mention = mention_re.match(word[1:])
                if mention:
                    mentions.append(mention.group('mention'))

        return mentions


class NumTweetsExtractor(TweetExtractorBase):
    """
    Store the number of tweets we've processed for this user.
    We have to use this figure and not the real one, otherwise
    various stats are off.

    Has to override some of the methods in the base class.
    """
    entity = 'num_tweets'

    def initialise_for_user(self):
        self.num = 0

    def get_tweet_entities(self, *args):
        self.num += 1

    def get_user_entities(self):
        return self.num


class NumRetweetsExtractor(NumTweetsExtractor):       
    entity = 'num_retweets'

    def get_tweet_entities(self, message, cleaned_message, timestamp):
        if ('RT @' in message) or message.startswith('RT:'):
            self.num += 1


class NumUrlsExtractor(NumTweetsExtractor):
    entity = 'num_urls'

    def get_tweet_entities(self, message, cleaned_message, timestamp):
        self.num += len(link_re.findall(cleaned_message))


class TweetingTimeExtractor(TweetExtractorBase):
    entity = 'tweeting_time'

    def initialise_for_user(self):
        self.start_time = None
        self.end_time = None

    def get_tweet_entities(self, message, cleaned_message, timestamp):
        self.end_time = timestamp

        if self.start_time is None:
            self.start_time = timestamp

    def get_user_entities(self):
        return (self.end_time - self.start_time).total_seconds()



"""
Entity extractors that use profile information only
"""

class ProfileExtractorBase(EntityExtractorBase):
    register = profile_extractors

    def get_user_entities(self, profile):
        return profile[self.profile_key]


class NumFollowersExtractor(ProfileExtractorBase):
    entity = 'num_followers'
    profile_key = 'followers_count'


class NumFriendsExtractor(ProfileExtractorBase):
    entity = 'num_friends'
    profile_key = 'friends_count'


class NameExtractor(ProfileExtractorBase):
    entity = 'name'
    profile_key = 'name'

class DescriptionExtractor(ProfileExtractorBase):
    entity = 'description'
    profile_key = 'description'



"""
Entity extractors that use other entities that have already been extracted lol
"""

class OtherExtractorBase(EntityExtractorBase):
    register = other_extractors


class NumMentionsExtractor(OtherExtractorBase):
    entity = 'num_mentions'
    needed_entity = 'mentions'

    def get_user_entities(self, user_data):
        return len(user_data[self.needed_entity])

    @classmethod
    def get_needed_entities(self):
        return [self.needed_entity]


class NumHashtagsExtractor(NumMentionsExtractor):
    entity = 'num_hashtags'
    needed_entity = 'hashtags'





"""
Initialise all the extractors and put them in the relevant dictionary
"""
things = dict(locals())
for name, thing in things.iteritems():
    if (inspect.isclass(thing) and
        issubclass(thing, EntityExtractorBase) and
        thing.entity is not None):
        thing.register[thing.entity] = thing()
