from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from io import TextIOWrapper
import csv
import re
import datetime

app = Flask("Assignment 2")
app.config['UPLOAD_FOLDER'] = '/uploaded_files'
client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = TextIOWrapper(request.files['file'], encoding='utf-8')
        filetype = request.form['file_type']
        datatype = request.form['data_type']
        reader = csv.DictReader(f)
        header = reader.fieldnames
        db = client.a2test
        if filetype == "time":
            collection = db[datatype]
            # replace the state and province headers so they are consistent
            for n, h in enumerate(header):
                if "State" in h:
                    header[n] = 'Province_State'
                elif "Country" in h:
                    header[n] = 'Country_Region'
                elif re.match("^[0-9//]*$", h):
                    m, d, y = [int(x) for x in h.split('/')]
                    y = 2000 + y
                    date = datetime.date(y, m, d)
                    header[n] = date.strftime("%Y-%m-%d")
                elif "Long" in h:
                    header[n] = "Long_"
                else:
                    continue
            reader = csv.DictReader(f, fieldnames=header)
            for data in reader:
                collection.update({"Lat": data["Lat"], "Long_": data["Long_"]}, data, upsert=True)

        if filetype == "daily":
            for data in reader:
                date_str = data["Last_Update"]
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                date = date_obj.strftime("%Y-%m-%d")
                confirmed_collection = db['confirmed']
                confirmed_collection.update({"Lat": data["Lat"], "Long_": data["Long_"]},
                                            {"$set": {date: data["Confirmed"], "Combined_Key": data["Combined_Key"]}},
                                            upsert=True)
                deaths_collection = db['deaths']
                deaths_collection.update({"Lat": data["Lat"], "Long_": data["Long_"]},
                                         {"$set": {date: data["Deaths"], "Combined_Key": data["Combined_Key"]}},
                                         upsert=True)
                active_collection = db['active']
                active_collection.update({"Lat": data["Lat"], "Long_": data["Long_"]},
                                         {"$set": {date: data["Active"], "Combined_Key": data["Combined_Key"]}},
                                         upsert=True)
                recovered_collection = db['recovered']
                recovered_collection.update({"Lat": data["Lat"], "Long_": data["Long_"]},
                                            {"$set": {date: data["Recovered"], "Combined_Key": data["Combined_Key"]}},
                                            upsert=True)

        return redirect(url_for('home'))


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        print("s")
        query_type = request.form["query_type"]
        countries = request.form["countries"]
        states = request.form["states"]
        combined = request.form["combined"]
        date_start = request.form["date_start"]
        date_end = request.form["date_end"]

        all_countries = [x for x in countries.split('/')]
        all_states = [x for x in states.split('/')]
        all_combined = [x for x in combined.split('/')]

        print(all_countries)


if __name__ == "__main__":
    app.run()
