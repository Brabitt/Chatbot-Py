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


def clean_sentence(sentence):
    """
    define a function to lemmatize the words that we will give it to the chatbot
    :param sentence:
    :return: a lemmatizer sentence
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    print('lemmatize the word/sentence:------', sentence_words)
    return sentence_words


# preparing the bag of words

def bag_words(sentence):
    """
    prepare the bag of words, this function is in charge of
    creating a bag with the length
    of the word/phrase and save it in a list.
    If the word/phrase is in the 'words' list,
    then it replaces the 0 in the bag with a 1.
    :param sentence:
    :return: a bag of words
    """
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


def predict_class(sentence):
    """
    in this function we compare the phrase/word with the class it belongs to,
    i.e. we write words that match the list words and this function will
    compare them with our model and predict which class they belong to.

    :param sentence:
    :return: return_list ---> example with the word 'hello':
            output -----> [{'intent': 'greeting', 'probability': '0.9996928'}]

    """
    bag_of_words = bag_words(sentence)
    print('bag of words without coma : ------', bag_of_words)
    result = model.predict(np.array([bag_of_words]))[0]
    print('result: ----- ', result)

    ERROR_THRESHOLD = 0.25

    results = [[i, r] for i, r in enumerate(result) if r > ERROR_THRESHOLD]
    print('results after: ---- ', results)

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        print(return_list)
    return return_list


predict_class(sentence=input())
