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
        """Interacts with the database to add/update data when
        a file is uploaded."""
        file = TextIOWrapper(request.files['file'], encoding='utf-8')
        print(request)
        filetype = request.form['file_type']
        datatype = request.form['data_type']
        reader = csv.DictReader(file)
        header = reader.fieldnames
        db = Database.getDb(self)
        if filetype == "time":
            uploader = TimeSeriesFileUploader(
                db, datatype, header, file, reader)
            uploader.upload()

        elif filetype == "daily":
            uploader = DailyFileUploader(db, datatype, header, file, reader)
            uploader.upload()

        return redirect(url_for('homepage'))


class FileUploader:
    def __init__(self, database, datatype, header, file, reader):
        self.database = database
        self.datatype = datatype
        self.header = header
        self.file = file
        self.reader = reader

    def upload(self):
        pass


class TimeSeriesFileUploader(FileUploader):
    def upload(self):
        """Updates the database when a Time Series file is uploaded."""
        collection = self.database[self.datatype]
        # replace the state and province headers so they are consistent
        for n, h in enumerate(self.header):
            if "State" in h:
                self.header[n] = 'Province_State'
            elif "Country" in h:
                self.header[n] = 'Country_Region'
            elif re.match("^[0-9//]*$", h):
                m, d, y = [int(x) for x in h.split('/')]
                y = 2000 + y
                date = datetime.date(y, m, d)
                self.header[n] = date.strftime("%Y-%m-%d")
            elif "Long" in h:
                self.header[n] = "Long_"
            else:
                continue
        reader = csv.DictReader(self.file, fieldnames=self.header)
        for data in reader:
            collection.update(
                {"Lat": data.get("Lat", ""), "Long_": data.get("Long_", "")},
                data,
                upsert=True)


class DailyFileUploader(FileUploader):
    def upload(self):
        """Updates the database when a Daily Report file is uploaded."""
        for data in self.reader:
            date_str = data["Last_Update"]
            date_obj = datetime.datetime.strptime(
                date_str, "%Y-%m-%d %H:%M:%S")
            date = date_obj.strftime("%Y-%m-%d")
            confirmed_collection = self.database['confirmed']
            confirmed_collection.update(
                {"Lat": data.get("Lat", ""), "Long_": data.get("Long_", ""), "Province_State": data.get("Province_State", ""), "Country_Region": data.get("Country_Region", "")},
                {"$set": {
                            date: data.get("Confirmed", ""),
                            "Combined_Key": data.get("Combined_Key", "")
                        }},
                upsert=True)
            deaths_collection = self.database['deaths']
            deaths_collection.update(
                {"Lat": data.get("Lat", ""), "Long_": data.get("Long_", ""), "Province_State": data.get("Province_State", ""), "Country_Region": data.get("Country_Region", "")},
                {"$set": {
                            date: data.get("Deaths", ""),
                            "Combined_Key": data.get("Combined_Key", "")
                        }},
                upsert=True)
            active_collection = self.database['active']
            active_collection.update(
                {"Lat": data.get("Lat", ""), "Long_": data.get("Long_", ""), "Province_State": data.get("Province_State", ""), "Country_Region": data.get("Country_Region", "")},
                {"$set": {
                            date: data.get("Active", ""),
                            "Combined_Key": data.get("Combined_Key", "")
                        }},
                upsert=True)
            recovered_collection = self.database['recovered']
            recovered_collection.update(
                {"Lat": data.get("Lat", ""), "Long_": data.get("Long_", ""), "Province_State": data.get("Province_State", ""), "Country_Region": data.get("Country_Region", "")},
                {"$set": {
                            date: data.get("Recovered", ""),
                            "Combined_Key": data.get("Combined_Key", "")
                        }},
                upsert=True)
