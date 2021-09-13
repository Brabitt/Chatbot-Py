from flask import Flask, render_template, request
from chatbot import predict_class, getResponse, model, intents

app = Flask(__name__)


# routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]

    ints = predict_class(msg)
    res = getResponse(ints, intents)
    return res


if __name__ == "__main__":
    app.run(debug=True, port=3000)
