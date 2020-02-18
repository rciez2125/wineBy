from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/contactform', methods = ['POST'])
def getvalue():
	firstName = request_form['fname']
	lastName = request_form['lname']
	email = request_form['email']
	storerec = request.form['store']
	age = request.form['age']
	now = datetime.now()

	d2 = pd.read_csv('customerlist.csv', index_col = 'Unnamed: 0')
	s2 = pd.read_csv('storerecnotes.csv', index_col = 'Unnamed: 0')

	d = pd.DataFrame({'firstName': firstName, 'lastName': lastName, 'email': email}, index = [d2.index[-1]+1])
	s = pd.DataFrame({'date': now, 'storerec': storerec}, index = [s2.index[-1]+1])
	d2 = d2.append(d)
	s2 = s2.append(s)
	d2.to_csv('customerlist.csv')
	s2.to_csv('storerecnotes.csv')
	print("The email address is '" + email + "'")
	return render_template('submittedform.html')