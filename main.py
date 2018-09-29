from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['local']
collection = db['phone']


@app.route("/")
def home_page():
    result = []
    cursor = collection.find({})
    for document in cursor:
        result.append(document['name'])
    return render_template("index.html", entries=result)
