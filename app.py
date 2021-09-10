from flask import Flask, render_template
# from chatbot import *

app = Flask(__name__)


# routes
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000)