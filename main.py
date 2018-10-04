from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['local']
collection = db['phone']


@app.route("/")
def home_page():
    brands_list = collection.distinct('brand')
    return render_template("home.html", brands=brands_list)


@app.route("/", methods=['POST'])
def search_page():
    result = []
    search_text = request.form['search'].lower()
    brands_list = collection.distinct('brand')
    cursor = collection.find({})

    for document in cursor:
        doc_atr = [document['date'], document['brand'], document['model'], document['rating'], document['proc'], document['price']]
        doc_lower = [x.lower() for x in doc_atr]
        if any(search_text in x for x in doc_lower):
            result.append(doc_atr)

    return render_template("category.html", brands=brands_list, result=result)


@app.route("/<brand>")
def variable_page(brand):
    result = []
    brands_list = collection.distinct('brand')

    if brand == 'all':
        cursor = collection.find({})
    else:
        cursor = collection.find({"brand": brand})

    for document in cursor:
        result.append([document['date'], document['brand'], document['model'], document['rating'], document['proc'], document['price']])
    return render_template("category.html", brands=brands_list, result=result)
