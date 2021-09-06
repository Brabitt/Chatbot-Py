import json
import pickle
import random

import nltk
import numpy as np
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
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
    words = sorted(set(words))
    classes = sorted(set(classes))
    print(words)
    print(classes)

    # saving the lists words and classes in files, that will be using in the ML training
    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

    # Preparing the training data for the chatbot
    # here we replace the letters by number and store them in an array
    training = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        words_patterns = document[0]
        words_patterns = [lemmatizer.lemmatize(word.lower()) for word in words_patterns]
        for word in words:
            if word in words_patterns:
                bag.append(1)
            else:
                bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training)  # create train and test lists. X - patterns, Y - intents
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    print("Training data created")
