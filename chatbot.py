import json


intents = json.loads(open('intents.json').read())


for intent in intents['intents']:
    for pattern in intent["patterns"]:
        print(pattern)