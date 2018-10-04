from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['local']
collection = db['phone']
collection2 = db['comments']


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


@app.route("/variable/<string:brand>")
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


@app.route("/contact")
def contact_page():
    result = []
    brands_list = collection.distinct('brand')
    cursor = collection2.find({})

    for document in cursor:
        result.append([document['fname'], document['lname'], document['comment']])

    return render_template("contact.html", brands=brands_list, result=result)


@app.route("/contact", methods=['POST'])
def submit_to_db():
    entry = {}
    entry["fname"] = request.form['firstname']
    entry["lname"] = request.form['lastname']
    entry["comment"] = request.form['comment']

    if(entry["fname"] and entry["lname"] and entry["comment"]):
        collection2.insert_one(entry)

    return redirect(url_for('contact_page'))
