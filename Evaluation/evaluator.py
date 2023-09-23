import requests
from flask import Flask


app = Flask(__name__)


@app.route('/')
def main(): 
    return alice() + "<br><br>" + alicevbaab()
def alice():
    winTracker = {'x':0, 'o':0}
    for i in range(50):
        winTracker[requests.get("http://alice:5000/alice").text] += 1
    if (winTracker['x'] == winTracker['o']):
        return "Alice does equally well as both x and o!\n" + str(winTracker)
    return "Alice does better as " + max(winTracker, key=winTracker.get) + '.\n' + str(winTracker)
def alicevbaab():
    winTracker = {'Alice':0, 'Baab':0}
    for i in range(20):
        winTracker[requests.get("http://alice:5000/alicevbaab").text] += 1
    if (winTracker['Alice'] == winTracker['Baab']):
        return "Alice and Baab are both great!\n" + str(winTracker)
    return max(winTracker, key=winTracker.get) + " does better.\n" + str(winTracker)

    


if __name__ == '__main__':
    app.run()
