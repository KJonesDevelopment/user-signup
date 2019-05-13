from flask import Flask, request, redirect 
import jinja2
import os
import re
import cgi

app = Flask(__name__)
app.config["DEBUG"] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape = True)

@app.route("/", methods = ["GET", "POST"])
def index():
    template = jinja_env.get_template('greeting.html')
    success = jinja_env.get_template('success.html')
    if request.method == "POST":
        username = cgi.escape(request.form['username'])
        errorUsername = is_username(username)
        email = cgi.escape(request.form['email'])
        errorEmail = is_email(email)
        if email == "":
                errorEmail = "";
        password = cgi.escape(request.form['password'])
        errorPassword = is_password(password)
        verify = cgi.escape(request.form['verify'])
        errorVerify = is_verify(verify, password)
        for i in [errorUsername, errorEmail, errorPassword, errorVerify]:
            if i != "":
                return template.render(username=username, email=email, errorUsername=errorUsername, errorEmail = errorEmail, errorPassword = errorPassword, errorVerify = errorVerify)
        return redirect("/somuchsuccess" + "?username=" + username)
    return template.render()

def is_email(email):
    email = email.lower()
    if not re.match(r"[a-z][a-z\d.-_&]*[@][a-z\d.-_]+[.][a-z]{2,5}", email):
        return "Fool, that's not an e-mail!"
    return  ""

def is_password(password):
    if len(password)> 3 and len(password) < 20: 
        return ""
    return "Please choose a password between 3 and 20 characters, thank you!"

def is_username(username):
    if len(username) > 3 and len(username) < 20: 
        return ""
    return "Please choose a name between 3 and 20 characters, thank you!"

def is_verify(verify, password):
    if verify == password:
        return ""
    return "Your passwords did not match, please try again!"

@app.route("/somuchsuccess", methods=["GET"])
def success():
    template = jinja_env.get_template('success.html')
    username = request.args.get('username')
    return template.render(username=username)
    #return render_template("file.html", username=username)


app.run()

