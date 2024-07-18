from flask import Flask, render_template,url_for,redirect,request
import random 

app = Flask(__name__, template_folder = "templates", static_folder = "static")

@app.route("/home")
def home():
	return render_template("home.html")


@app.route("/fortune")
def fortune():
	fortunes = ["you will have an amazing meal", "you will have a sweet dream", "you will have a good day", "something good will happen today", "you will have an easy lab", "Abdallah will catch you out at night", "you will have a boring DU", "you will eat IASA's food", "you will have diarrhea", "you will slip"]
	rndNum = random.randint(0, 9)
	return render_template("fortune.html", fortune = fortunes[rndNum])

@app.route("/indecisive")
def indecisive():
	fortunes = ["you will have an amazing meal", "you will have a sweet dream", "you will have a good day", "something good will happen today", "you will have an easy lab", "Abdallah will catch you out at night", "you will have a boring DU", "you will eat IASA's food", "you will have diarrhea", "you will slip"]
	indecisive_fortunes = []
	for time in range(3):
		indecisive_fortunes.append(fortunes[random.randint(0, len(fortunes) - 1)])
		fortunes.remove(indecisive_fortunes[-1])
	print(indecisive_fortunes)
	return render_template("indecisive.html", first_fortune=indecisive_fortunes[0], second_fortune=indecisive_fortunes[1], third_fortune=indecisive_fortunes[2])


if __name__ == "__main__":
	app.run(debug = True)