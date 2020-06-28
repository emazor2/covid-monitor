from flask import request, send_file
from flask_restful import Resource
from COVIDMonitor.Database import Database
import sys
import matplotlib.pyplot as plt
import pandas as pd


class Query(Resource):
    def post(self):
        query_type = request.form['query_type']
        key_type = request.form['key_type']
        input_keys = request.form['key_list']
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        data_format = request.form['return_format']

        all_keys = [x for x in input_keys.split('/')]

        db = Database.getDb(self)
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

                for key in document:
                    if date_start <= key <= date_end:
                        new_doc[key] = document[key]
                all_documents.append(new_doc)

        exporter = ExportFactory(data_format).getExporter(all_documents, query_type, key_type, date_start, date_end)
        return_data = exporter.export_file()

        return return_data


class ExportFactory:
    def __init__(self, data_format):
        self.data_format = data_format

    def getExporter(self, all_documents, query_type, key_type, date_start, date_end):
        if self.data_format == "json":
            return JsonExporter(all_documents)
        elif self.data_format == "csv":
            return CsvExporter(all_documents)
        elif self.data_format == "text":
            return HtmlExporter(all_documents)
        elif self.data_format == "line_plot":
            return PlotExporter(all_documents, query_type, key_type, date_start, date_end)


class Exporter:
    def __init__(self, all_documents):
        self.all_documents = all_documents

    def export_file(self):
        pass


class JsonExporter(Exporter):
    def export_file(self):
        if "pytest" in sys.modules:
            pd.DataFrame(self.all_documents).to_json('COVIDMonitor/out.json', orient="records")
        else:
            pd.DataFrame(self.all_documents).to_json('out.json', orient="records")
        return send_file('out.json', as_attachment=True)


class CsvExporter(Exporter):
    def export_file(self):
        if "pytest" in sys.modules:
            pd.DataFrame(self.all_documents).to_csv('COVIDMonitor/out.csv')
        else:
            pd.DataFrame(self.all_documents).to_csv('out.csv')
        return send_file('out.csv', as_attachment=True)


class HtmlExporter(Exporter):
    def export_file(self):
        print(self.all_documents)
        if "pytest" in sys.modules:
            pd.DataFrame(self.all_documents).to_html('COVIDMonitor/out.html')
        else:
            pd.DataFrame(self.all_documents).to_html('out.html')
        return send_file('out.html', as_attachment=True)


class PlotExporter(Exporter):
    def __init__(self, all_documents, query_type, key_type, date_start, date_end):
        super().__init__(all_documents)
        self.query_type = query_type
        self.key_type = key_type
        self.date_start = date_start
        self.date_end = date_end

    def export_file(self):
        plt.switch_backend('Agg')
        # line graph
        if self.key_type == "states":
            key = "Province_State"
        elif self.key_type == "countries":
            key = "Country_Region"
        elif self.key_type == "combined":
            key = "Combined_Key"

        locations = []
        for document in self.all_documents:
            location = document[key]
            if location not in locations:
                locations.append(document[key])
            document.pop("Lat")
            document.pop("Long_")

        if self.key_type == "states" or self.key_type == "countries":
            for location in locations:
                combined_document = {key: location}

                all_dates = list(self.all_documents[0].keys())
                all_dates.remove("Province_State")
                all_dates.remove("Country_Region")
                all_dates.remove("Combined_Key")

                for date in all_dates:
                    combined_document[date] = 0

                for date in all_dates:
                    for document in self.all_documents:
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
            for data in self.all_documents:

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
        plt.title(
            "Changes in the number of " + self.query_type + " cases" + " from " + self.date_start + " to " + self.date_end)
        plt.legend(locations)

        if "pytest" in sys.modules:
            plt.savefig('COVIDMonitor/out.png')
        else:
            plt.savefig('out.png')
        return send_file('out.png', as_attachment=True)
