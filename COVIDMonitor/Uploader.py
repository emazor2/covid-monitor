import datetime
from io import TextIOWrapper
from flask import request, url_for
from flask_restful import Resource
import csv
import re

from werkzeug.utils import redirect

from COVIDMonitor.Database import Database


class Uploader(Resource):
    def post(self):
        file = TextIOWrapper(request.files['file'], encoding='utf-8')
        print(request)
        filetype = request.form['file_type']
        datatype = request.form['data_type']
        reader = csv.DictReader(file)
        header = reader.fieldnames
        db = Database.getDb(self)
        if filetype == "time":
            self.timeSeriesFileUploader(db, datatype, header, file)

        elif filetype == "daily":
            self.dailyFileUploader(db, reader)

        return redirect(url_for('homepage'))

    def timeSeriesFileUploader(self, db, datatype, header, file):
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
        reader = csv.DictReader(file, fieldnames=header)
        for data in reader:
            collection.update({"Lat": data.get("Lat", ""), "Long_": data.get("Long_", "")}, data, upsert=True)

    def dailyFileUploader(self, db, reader):
        for data in reader:
            date_str = data["Last_Update"]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            date = date_obj.strftime("%Y-%m-%d")
            confirmed_collection = db['confirmed']
            confirmed_collection.update({"Lat": data.get("Lat", ""), "Long_": data.get("Long_", "")},
                                        {"$set": {date: data.get("Confirmed", ""),
                                                  "Combined_Key": data.get("Combined_Key", "")}},
                                        upsert=True)
            deaths_collection = db['deaths']
            deaths_collection.update({"Lat": data.get("Lat", ""), "Long_": data.get("Long_", "")},
                                     {"$set": {date: data.get("Deaths", ""),
                                               "Combined_Key": data.get("Combined_Key", "")}},
                                     upsert=True)
            active_collection = db['active']
            active_collection.update({"Lat": data.get("Lat", ""), "Long_": data.get("Long_", "")},
                                     {"$set": {date: data.get("Active", ""),
                                               "Combined_Key": data.get("Combined_Key", "")}},
                                     upsert=True)
            recovered_collection = db['recovered']
            recovered_collection.update({"Lat": data.get("Lat", ""), "Long_": data.get("Long_", "")},
                                        {"$set": {date: data.get("Recovered", ""),
                                                  "Combined_Key": data.get("Combined_Key", "")}},
                                        upsert=True)
