import requests
from flask import Flask


app = Flask(__name__)


@app.route('/')
def main():
    winTracker = {'x':0, 'o':0}
    for i in range(50):
        winTracker[requests.get("http://alice:5000/evaluatoraccess").text] += 1
        print(winTracker)
    if (winTracker['x'] == winTracker['o']):
        return "Alice does equally well as both x and o!\n" + str(winTracker)
    return "Alice does better as " + max(winTracker, key=winTracker.get) + '.\n' + str(winTracker)


if __name__ == '__main__':
    app.run()
