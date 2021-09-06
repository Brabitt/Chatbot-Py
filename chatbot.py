import json
import pickle

import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())


# Tokenize the words from intents

def tokenize_text():
    words = []
    classes = []
    documents = []
    ignore_letters = ['?', '!', '.', ',']
    for intent in intents['intents']:
        for pattern in intent["patterns"]:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    print(documents)
    # lemmatize the words and classes
    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))
    classes = sorted(set(classes))
    print(words)
    print(classes)

    # saving the lists words and classes in files, that will be using in the ML
    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))


tokenize_text()
