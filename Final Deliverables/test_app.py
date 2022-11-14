from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def main_page():
    return redirect(url_for("dashboard"))


@app.route("/register")
def register():
    return render_template("customer_register.html")


@app.route("/login")
def login():
    return render_template("customer_login.html")


@app.route("/logout")
def logout1():
    return render_template("logout.html")


@app.route("/dashboard")
def dashboard():
    return render_template("customer_dashboard.html")


@app.route("/agent_dashboard")
def agent_dashboard():
    return render_template("agent_dashboard.html")


@app.route("/chat")
def chat():
    return render_template("chatroom.html")


@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


app.run(debug=True)
