from flask import Flask, render_template,url_for,redirect,request
import random 
import requests

app = Flask(__name__, template_folder = "templates", static_folder = "static")
fortunes = ["you will have an amazing meal", "you will have a sweet dream", "you will have a good day", "something good will happen today", "you will have an easy lab", "Abdallah will catch you out at night", "you will have a boring DU", "you will eat IASA's food", "you will have diarrhea", "you will slip"]

@app.route("/home", methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		return render_template("home.html")
	else:
		birth_month = request.form['birth_month']
		return redirect(url_for('fortune', month_name=birth_month))


@app.route("/fortune/<month_name>", methods=['GET','POST'])
def fortune(month_name):
	users_fortune = fortunes[(len(month_name) - 1) % len(fortunes)]
	return render_template("fortune.html", fortune = users_fortune)

if __name__ == "__main__":
	app.run(debug = True)