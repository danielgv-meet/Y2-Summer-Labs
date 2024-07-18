from flask import Flask, render_template,url_for,redirect,request
from flask import session as login_session
import random 
import requests


app = Flask(__name__, template_folder = "templates", static_folder = "static")
fortunes = ["you will have an amazing meal", "you will have a sweet dream", "you will have a good day", "something good will happen today", "you will have an easy lab", "Abdallah will catch you out at night", "you will have a boring DU", "you will eat IASA's food", "you will have diarrhea", "you will slip"]
app.config['SECRET_KEY'] = "your_secret_string"

@app.route("/home", methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		return render_template("home.html")
	else:
		login_session["month_name"] = request.form['birth_month']
		login_session["his_name"] = request.form['name']
		login_session["zodiac"] = request.form['zodiac']

		return redirect('/fortune')


@app.route("/fortune", methods=['GET','POST'])
def fortune():
	if request.method == 'POST':
		ascii_value = 0
		for letter in login_session["month_name"]:
			ascii_value += ord(letter)
		for letter in login_session["his_name"]:
			ascii_value += ord(letter)
		for letter in login_session["zodiac"]:
			ascii_value += ord(letter)

		login_session["fortune"] = fortunes[(ascii_value - 1) % 10]
		print(login_session)
	return render_template("fortune.html")	

if __name__ == "__main__":
	app.run(debug = True)