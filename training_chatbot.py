import json
import pickle
import random

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

# Tokenize the words from intents

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

# lemmatize the words and classes
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# saving the lists words and classes in files, that will be using in the ML training
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Preparing the training data for the chatbot
# here we replace the letters by number and store them in an array
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    # list of tokenized words for the pattern
    words_patterns = document[0]
    words_patterns = [lemmatizer.lemmatize(word.lower()) for word in words_patterns]
    # create our bag of words array with 1, if word match found in current pattern
    for word in words:
        if word in words_patterns:
            bag.append(1)
        else:
            bag.append(0)
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training, dtype=object)  # create train and test lists. X - patterns, Y - intents
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print("Training data created")

# building the neuronal network

model = Sequential()
# Adding the layers in to our model
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# check the model

check_model = model.summary()
print(check_model)

# compile the model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# training the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=True)
model.save('chatbotmodel.h5', hist)
