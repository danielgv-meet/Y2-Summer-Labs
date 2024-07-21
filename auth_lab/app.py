from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB057zr6FS31fUqXSuvPuGwTgf4CU3_MNM",
  "authDomain": "auth-lab-1349a.firebaseapp.com",
  "projectId": "auth-lab-1349a",
  "storageBucket": "auth-lab-1349a.appspot.com",
  "messagingSenderId": "916347876212",
  "appId": "1:916347876212:web:aa74c8b48d817af88fb221",
  "databaseURL":""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = 'super-secret-key'

@app.route("/", methods=['GET', 'POST'])
def sign_up():
  if request.method == 'GET':
    return render_template('signup.html')
  else:
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
    except:
      print("something went wrong")
    login_session["quotes"] = [] 
    return redirect("/home")
    


@app.route("/signin", methods=['GET', 'POST'])
def sign_in():
  if request.method == 'GET':
    print("GET")
    return render_template("signin.html")
  else:
    login_session["email"] = request.form["email"]
    login_session["password"] = request.form['password']
    login_session["quotes"] = []
    return redirect(url_for("home"))

@app.route("/signout")
def signout():
  login_session['user'] = None
  auth.current_user = None
  return redirect(url_for('sign_in'))

@app.route("/home", methods=["POST", "GET"])
def home():
  if request.method == "GET":
    return render_template("home.html")
  else:
    login_session["quotes"].append(request.form["quote"])
    login_session.modified = True
    return redirect(url_for('thanks'))


@app.route("/thanks")
def thanks():
  return render_template("thanks.html")

@app.route("/display")
def display():
  return render_template("display.html", quotes = login_session["quotes"])

if __name__ == "__main__":
  app.run(debug=True)