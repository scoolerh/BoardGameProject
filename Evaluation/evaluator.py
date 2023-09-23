import requests
from flask import Flask


app = Flask(__name__)


@app.route('/')
def main():
    return requests.get("http://alice:5000/evaluatoraccess").text


if __name__ == '__main__':
    app.run()
