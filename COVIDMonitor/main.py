import os
import psycopg2

from flask import Flask, redirect, render_template, jsonify, flash, request, url_for
from werkzeug.utils import secure_filename

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
cur = conn.cursor()

UPLOAD_FOLDER = '/files'
ALLOWED_EXTENSIONS = {'csv'}

# app = Flask("Assignment 2")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# check that the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/monitor')
def welcome_monitor():
	# return 'Welcome to the Covid Monitor!!!'
	return render_template("monitor.html")

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['inputFile']
	# TODO: check for validation
	# return file.filename
	# TODO: use user input to determine file type
	# parse file data and send to database
	send_to_db(file)

# send data to database
def send_to_db(file):
    with open(file, 'r') as f:
        # skip header
        next(f)
        # copy csv to database
        cur.copy_from(f, '', sep=',')
    conn.commit()
	

# def upload_file():
# 	if request.method == "POST":
# 		# check if the post request has the file part
# 		if 'file' not in request.files:
# 			flash('No file part')
# 			return redirect(request.url)
# 		file = request.files['file']
# 		# if user does not select file, browser also submit an empty
# 		# part without filename
# 		if file.filename == '':
# 			flash('No selected file')
# 			return redirect(request.url)
# 		if file and allowed_file(file.filename):
# 			filename = secure_filename(file.filename)
# 			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 			return redirect(url_for('upload_file', filename=filename))
# 			# TODO: parse data file


if __name__ == "__main__":
	app.run(debug=True)

	# interact with user
	# file_type = input("Enter 'Time Series' or 'Daily Report': ")
	# country = input("")