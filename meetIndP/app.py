from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your-secret-key'

firebaseConfig = {
  'apiKey': "AIzaSyAGB8GFQN4N4vI_pFsXDVDrHSdpLYYysvk",
  'authDomain': "meet-example2024.firebaseapp.com",
  'projectId': "meet-example2024",
  'storageBucket': "meet-example2024.appspot.com",
  'messagingSenderId': "104511305959",
  'appId': "1:104511305959:web:583cc9dde2b008e9b94a42",
  'measurementId': "G-6JPQ4XNJTT",
  'databaseURL': "https://auth-lab-1349a-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            user_dict = {"name": name, "email": email}
            db.child("Users").child(user_id).set(user_dict)
            login_session['user'] = user
            return redirect(url_for('main_page'))
        except Exception as e:
            return str(e)
    else:
        return render_template('signup.html')

@app.route('/login', methods=["GET", "POST"])
def signin():
    if request.method =="GET":
        return render_template("signin.html")
    else:
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            return redirect(url_for('main_page'))
        except:
            return "ERROR user does not exist"

@app.route('/main_page', methods=["POST", "GET"])
def main_page():
    if request.method == "GET":
        user_id = login_session['user']['localId']
        user_name = db.child('Users').child(user_id).child("name").get().val()
        return render_template('main.html', name=user_name)
    else:
        users_choice = request.form["users_choice"]
        login_session['users_choice'] = users_choice
        return redirect(url_for('learning'))

@app.route('/learning', methods=['GET'])
def learning():
    if login_session["users_choice"] == "kata":
        return render_template("kata.html")
    elif login_session["users_choice"] == "kumite":
        return render_template('kumite.html')
    else:
        return render_template("pe.html")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        db.child('feedback').child(login_session['user']['localId']).set(request.form['feedback'])
    return render_template('feedback.html')

@app.route('/display')
def display():
    return render_template('display.html', users=db.child('feedback').get().val())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



if __name__ == "__main__":
    app.run(debug=True)
