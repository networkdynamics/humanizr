import re

open_result_files = {}


def format_timedelta(timedelta):
    total_seconds = timedelta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return '%d hours, %d minutes, %d seconds' % (hours, minutes, seconds)


def is_str(val):
    """
    Utility function to check if something is a string or unicode.
    """
    return isinstance(val, basestring)


def is_a_feature(s):
    return not (s.startswith('__') or s.endswith('Base'))


def clean(text):
    # If it's a retweet, get rid of the RT text (might as well)
    if 'RT @' in text:
        text = re.sub('RT @\w+?:? ', '', text)
    if 'RT: ' in text:
        text = text.replace('RT: ', '')

    #text = text.lower()
    
    # Now get rid of the URLs starting with http:// (links appear shortened so, no https)
    text = re.sub(r'[ ]*http:\/\/[^ ]+', '', text)

    # Now replace some HTL entities
    replacements = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        ':': ''
    }

    # Get rid of other ampersand-containing things
    text = re.sub(r'&#\d+;', '', text)

    for key, value in replacements.iteritems():
        text = text.replace(key, value)

    # Now remove all the other non-ascii chars
    text = ''.join(c for c in text if 0 < ord(c) < 128)

    # Get rid of hashtags and mentions too
    text = re.sub(r'[@#]\w+[ ]*', '', text)

    # Tabs?
    text = text.replace('\t', '')
    return text.strip(' ')
