from flask import Flask, session, request, url_for, redirect, render_template
from utils import auth, util
from os import urandom
import json

app = Flask(__name__)
app.secret_key = urandom(20)

@app.route("/", methods=["GET", "POST"])
def home():
    if len(session.keys())==0:
        return render_template('account.html')
    else:
        return render_template("home.html", username=session["username"])

@app.route("/authenticate/", methods=['POST'])
def authenticate():
    un = request.form["handle"]

    if request.form["type"] == "register":
        ps1 = request.form["pass1"]
        ps2 = request.form["pass2"]
        regRet = auth.register(un, ps1, ps2)#returns an error/success message
        return render_template("account.html", regerror=regRet)

    else:
        pw = request.form["pass"]
        text = auth.login(un, pw)#error message
        if text == "":#if no error message, succesful go back home
            session["username"] = un
            print text
            return redirect(url_for('home'))
        return render_template("account.html", logerror=text)


@app.route("/auth/", methods=['POST'])
def oauth():
    url = auth.getRedirectLink()
    if auth.updated(session["username"]):
        return render_template("home.html",
                username=session["username"],
                message = "Already Authenticated!")
    return redirect(url)


@app.route("/about/")
def about():
    return render_template("home.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
