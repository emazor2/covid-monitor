from flask import Flask, render_template, request, redirect, url_for, send_file
from pymongo import MongoClient
from io import TextIOWrapper
import csv
import re
import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
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
        query_type = request.form["query_type"]
        key_type = request.form["key_type"]
        input_keys = request.form["key_list"]
        date_start = request.form["date_start"]
        date_end = request.form["date_end"]
        data_format = request.form["return_format"]

        all_keys = [x for x in input_keys.split('/')]

        db = client.a2test
        collection = db[query_type]

        all_data = []

        # check if query is by country/region, state/province, or combined_key
        if key_type == "states":
            for key in all_keys:
                data_dict = {"Province_State": key}
                all_data.append(data_dict)

        if key_type == "countries":
            for key in all_keys:
                data_dict = {"Country_Region": key}
                all_data.append(data_dict)

        if key_type == "combined":
            for key in all_keys:
                data_dict = {"Combined_Key": key}
                all_data.append(data_dict)

        # query db for each document containing data for specified location
        all_documents = []
        for data_dict in all_data:
            documents = collection.find(data_dict)

            for document in documents:
                new_doc = {"Province_State": document.get("Province_State", ""),
                           "Country_Region": document.get("Country_Region", ""),
                           "Combined_Key": document.get("Combined_Key", ""), "Lat": document.get("Lat", ""),
                           "Long_": document.get("Long_", "")}
                # cases = document[date_start]
                # data_dict[date_start] = cases

                for key in document:
                    if date_start <= key <= date_end:
                        new_doc[key] = document[key]
                all_documents.append(new_doc)
        # data_dict["query_type"] = query_type

        # TODO: call correct display function depending on user input
        if data_format == "json":
            return_data = display_json(all_documents)
        elif data_format == "csv":
            return_data = display_csv(all_documents)
        elif data_format == "text":
            return_data = display_text(all_documents)
        elif data_format == "line_plot":
            return_data = display_plot(all_documents, query_type, key_type, date_start, date_end)

        return return_data

        # return "test"


def display_json(all_data):
    pd.DataFrame(all_data).to_json('out.json', orient="records")
    return send_file('out.json', as_attachment=True)


def display_csv(all_data):
    pd.DataFrame(all_data).to_csv('out.csv')
    return send_file('out.csv', as_attachment=True)


def display_text(all_data):
    pd.DataFrame(all_data).to_html('out.html')
    return send_file('out.html', as_attachment=True)


def display_plot(all_documents, query_type, key_type, date_start, date_end):
    # line graph
    if key_type == "states":
        key = "Province_State"
    elif key_type == "countries":
        key = "Country_Region"
    elif key_type == "combined":
        key = "Combined_Key"

    locations = []
    for document in all_documents:
        location = document[key]
        if location not in locations:
            locations.append(document[key])
        document.pop("Lat")
        document.pop("Long_")

    if key_type == "states" or key_type=="countries":
        for location in locations:
            combined_document = {}
            combined_document[key] = location

            all_dates = list(all_documents[0].keys())
            all_dates.remove("Province_State")
            all_dates.remove("Country_Region")
            all_dates.remove("Combined_Key")

            for date in all_dates:
                combined_document[date] = 0

            for date in all_dates:
                for document in all_documents:
                    if key in combined_document and key in document:
                        key_1 = combined_document[key]
                        key_2 = document[key]
                        if date in combined_document and date in document and key_1 == key_2:

                            cases = int(document[date])
                            if date != "Country_Region" and date != "Province_State" and date != "Combined_Key":
                                combined_document[date] += cases

            cases = list(combined_document.values())
            cases.pop(0)

            plt.plot(all_dates, cases)

    else:
        for data in all_documents:

            data.pop("Country_Region")
            data.pop("Province_State")
            data.pop("Combined_Key")

            dates = list(data.keys())
            cases = list(data.values())

            int_cases = []
            for case in cases:
                int_cases.append(int(case))

            plt.plot(dates, int_cases)

    plt.xlabel("Date")
    plt.ylabel("Number of Cases")
    plt.title("Changes in the number of " + query_type + " cases" + " from " + date_start + " to " + date_end)
    plt.legend(locations)
    plt.show()
    
    return 'Line plot should pop up in a new window'


if __name__ == "__main__":
    app.run(debug=True)
