from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['local']
collection = db['phone']
collection2 = db['comment']


# ~~~~~~~ HOME PAGE ~~~~~~~

@app.route('/')
def home_page():
    brands_list = collection.distinct('brand')
    return render_template('home.html', brands=brands_list)


# ~~~~~~~ GUIDE PAGE ~~~~~~~

@app.route('/guide')
def guide_page():
    brands_list = collection.distinct('brand')
    return render_template('guide.html', brands=brands_list)


# ~~~~~~~ DEALS PAGE ~~~~~~~

@app.route('/filter')
def deals_page():
    trusted_result = []
    trusted_cheap_result = []
    brands_list = collection.distinct('brand')
    trusted_vendors = ["Samsung", "Apple", "OnePlus", "Nokia", "Huawei", "Xiaomi", "Google", "LG", "HTC", "Blackberry", "Sony", "OPPO"]
    cursor = collection.find({'brand': {'$in': trusted_vendors}})

    for document in cursor:
        doc_atr = [document['date'], document['brand'], document['model'], document['rating'], document['proc'], document['price']]
        trusted_result.append(doc_atr)
        if document['price'] != '-' and int(document['price'].split(' ')[0]) <= 500:
            trusted_cheap_result.append(doc_atr)

    return render_template('filter.html', brands=brands_list, trusted=trusted_result, trusted_cheap=trusted_cheap_result)


# ~~~~~~~ VARIABLE PAGES [SEARCHBOX + BRANDS] ~~~~~~~

@app.route('/', methods=['POST'])
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

    return render_template('category.html', brands=brands_list, text='You have searched for: ' + search_text, result=result)


@app.route('/variable/<string:brand>')
def variable_page(brand):
    result = []
    brands_list = collection.distinct('brand')

    if brand == 'all':
        cursor = collection.find({})
    else:
        cursor = collection.find({'brand': brand})

    for document in cursor:
        result.append([document['date'], document['brand'], document['model'], document['rating'], document['proc'], document['price']])
    return render_template('category.html', brands=brands_list, text='You have selected: ' + brand, result=result)


# ~~~~~~~ PROPOSE PAGE ~~~~~~~

@app.route('/propose')
def propose_page():
    brands_list = collection.distinct('brand')
    return render_template('propose.html', brands=brands_list)


@app.route('/propose', methods=['POST'])
def submit_propose_to_db():
    entry = {}
    entry['date'] = request.form['date']
    entry['brand'] = request.form['brand']
    entry['model'] = request.form['model']
    entry['rating'] = request.form['rating']
    entry['proc'] = request.form['proc']
    entry['price'] = request.form['price']

    if all([entry['date'], entry['brand'], entry['model'], entry['rating'], entry['proc'], entry['price']]):
        collection.insert_one(entry)

    return redirect(url_for('propose_page'))


# ~~~~~~~ CONTACT PAGE ~~~~~~~

@app.route('/contact')
def contact_page():
    result = []
    brands_list = collection.distinct('brand')
    cursor = collection2.find({})

    for document in cursor:
        result.append([document['fname'], document['lname'], document['comment']])

    return render_template('contact.html', brands=brands_list, result=result)


@app.route('/contact', methods=['POST'])
def submit_comment_to_db():
    entry = {}
    entry['fname'] = request.form['firstname']
    entry['lname'] = request.form['lastname']
    entry['comment'] = request.form['comment']

    if all([entry['fname'], entry['lname'], entry['comment']]):
        collection2.insert_one(entry)

    return redirect(url_for('contact_page'))
