from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/', methods = ['POST'])
def getvalue():
	firstName = request_form['fname']
	lastName = request_form['lname']
	email = request_form['email']
	storerec = request.form['store']
	age = request.form['age']
	now = datetime.now()

	
	# do things with the data 

	return render_template('submittedform.html')