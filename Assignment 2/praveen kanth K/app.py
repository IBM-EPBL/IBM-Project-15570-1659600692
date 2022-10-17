from distutils.log import debug
from flask import Flask, redirect, url_for,render_template 

app = Flask(__name__)


@app.route("/")  
def home():
	return render_template("index.html")

@app.route("/about")  
def about():
	return render_template("about.html")

@app.route("/signin")  
def signin():
	return render_template("signin.html")

@app.route("/signup")  
def signup():
	return render_template("signup.html")


@app.route("/thank")  
def thank():
	return render_template("thank.html")

    
if __name__ == "__main__":
    app.run(debug=True)