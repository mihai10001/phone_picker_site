from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['local']
collection = db['phone']


@app.route("/")
def home_page():
    brands_list = collection.distinct('brand')
    return render_template("home.html", brands=brands_list)


@app.route("/<brand>")
def variable(brand):
    result = []
    brands_list = collection.distinct('brand')

    if brand == 'all':
        cursor = collection.find({})
    else:
        cursor = collection.find({"brand": brand})

    for document in cursor:
        result.append([document['date'], document['brand'], document['model'], document['rating'], document['proc'], document['price']])
    return render_template("category.html", brands=brands_list, result=result)
