from flask import Flask, render_template, make_response, request, redirect, url_for, send_file
from flask_restful import Resource, Api
from pymongo import MongoClient
from io import TextIOWrapper
import csv
import re
import datetime
import matplotlib.pyplot as plt
import pandas as pd


from COVIDMonitor import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
