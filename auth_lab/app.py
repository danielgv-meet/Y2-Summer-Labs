from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase
import firebase


firebaseConfig = {
  "apiKey": "AIzaSyB057zr6FS31fUqXSuvPuGwTgf4CU3_MNM",
  "authDomain": "auth-lab-1349a.firebaseapp.com",
  "projectId": "auth-lab-1349a",
  "storageBucket": "auth-lab-1349a.appspot.com",
  "messagingSenderId": "916347876212",
  "appId": "1:916347876212:web:aa74c8b48d817af88fb221",
  "databaseURL":"https://auth-lab-1349a-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
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
    username = request.form['username']
    full_name = request.form['fullname']
    user = {"full_name": full_name, "username": username, "email": email}
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      UID = login_session["user"]["localId"]
      db.child("Users").child(UID).set(user)
      # print(db.child("Users").child(UID).get().val())
      return redirect(url_for("home"))
    except:
      print("something went wrong")
      return render_template("error.html", error="The user already exist")     
  
   


@app.route("/signin", methods=['GET', 'POST'])
def sign_in():
  if request.method == 'GET':
    print("GET")
    return render_template("signin.html")
  else:
    email = request.form["email"]
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for("home"))
    except:
      print("The user is not existing")
      return render_template("error.html", error = "the user does not exist")
    

@app.route("/signout")
def signout():
  login_session['user'] = None
  auth.current_user = None
  login_session["quotes"] = []
  return redirect(url_for('sign_in'))


@app.route("/home", methods=["POST", "GET"])
def home():
  if request.method == "GET":
    return render_template("home.html")

  else:
    quotes = {"text": request.form["quote"], "said_by": request.form["teller"], "uid": login_session['user']["localId"]}
    db.child("Quotes").push(quotes)
    return redirect(url_for('thanks'))


@app.route("/thanks")
def thanks():
  return render_template("thanks.html")

@app.route("/display")
def display():
  return render_template("display.html", quotes = db.child("Quotes").get().val())


if __name__ == "__main__":
  app.run(debug=True)