import re
from nltk.corpus import wordnet

#building a list keywords

list_words = ['yes', 'yeah', 'sure', 'no', 'nah']

list_syn = {}

for word in list_words:
    synonyms = []
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():

            # remove any special characters from any of the synonym strings
            lem_name = re.sub('[^a-zA-z0-9 n.]', ' ', lem.name())
            synonyms.append(lem_name)

    list_syn[word] = set(synonyms)

print(list_syn)

# building dictionary of intents and keywords

keywords = {}
keywords_dict = {}

# defining new key in the keywords dictionary
keywords['yes'] = []

for synonym in list(list_syn['yes']):
    keywords['yes'].append('.*\b' + synonym + '\b.*')
for synonym in list(list_syn['yeah']):
    keywords['yes'].append('.*\b' + synonym + '\b.*')
for synonym in list(list_syn['sure']):
    keywords['yes'].append('.*\b' + synonym + '\b.*')

keywords['no'] = []

for synonym in list(list_syn['no']):
    keywords['no'].append('.*\b' + synonym + '\b.*')
for synonym in list(list_syn['nah']):
    keywords['no'].append('.*\b' + synonym + '\b.*')

for intent, keys in keywords.items():
    keywords_dict[intent] = re.compile('|'.join(keys))

#building a dictionary of responses
responses = {
    'yes': 'cool. what did you think of?',
    'no': 'thanks, maybe next time',
    'fallback': 'i dont get it pls help'
}

print(
    'Hey thanks for watching [streamers] stream. would you mind asking a few questions about your experience?'
)

while (True):
    user_input = input().lower()

    if user_input == 'no':
        print('coolsies')

        break

    matched_intent = None

    for intent, pattern in keywords_dict.items():
        if re.search(pattern, user_input):
            matched_intent = intent

    key = 'fallback'
    if matched_intent in responses:
        key = matched_intent

    print(responses[key])
