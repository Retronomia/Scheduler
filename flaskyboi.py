#testing out flask
#no hate name plz is beautiful

from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'