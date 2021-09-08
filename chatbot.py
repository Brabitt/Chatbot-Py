import random
import numpy as np
import pickle
import json

import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# we load our model and pkl documents for use in our chatbot

model = load_model('chatbotmodel.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
print(words, classes)


# define a function to lemmatize the words that we will give it to the chatbot

def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    print(sentence_words)
    return sentence_words


# preparing the bag of words

def bag_words(sentence):
    sentence_words = clean_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for w in sentence_words:
        print(w)
        for i, word in enumerate(words):
            print(i, word)
            if word == w:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
    print(bag)
    return np.array(bag)


bag_words(sentence=input())
