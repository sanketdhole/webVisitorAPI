from flask import Flask
from flask import request, jsonify
import time
import json

from util import ImageDownloader

imageDownloader = ImageDownloader()

app = Flask(__name__)

@app.route("/")
def index():
    imageDownloader.removeOldFiles()
    return json.dumps({
        'name':'Web Visitor',
        'status': 'Active',
        'time':time.ctime()
        })

@app.route("/image", methods=["POST"])
def getImage():
    imageDownloader.removeOldFiles()
    if request.method == "POST":
        return imageDownloader.addUrl(request.form['url'])

@app.route("/count")
def getCount():
    imageDownloader.removeOldFiles()
    return jsonify({'count':imageDownloader.getCount()})
            


if __name__=="__main__":
    app.run()
