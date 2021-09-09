from flask import Flask, request
from chatbot import *

app = Flask(__name__)


# routes
@app.route('/')
def home():
    return 'hello from flask server'


if __name__ == "__main__":
    app.run(debug=True, port=3000)