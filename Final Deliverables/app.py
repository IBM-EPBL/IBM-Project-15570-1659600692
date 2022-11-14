from models import TicketStatus
from models import Ticket
from flask import Flask, render_template, redirect, url_for, g, session, request
from flask_login import current_user, LoginManager, login_user, logout_user
from db import IBMdb2
import json
from models import User, UserType, Ticket
import uuid
from utils import login_required

app = Flask(__name__)
app.secret_key = "?????"

# Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# db
with open("db2.json") as f:
    creds = json.load(f)
db = IBMdb2(creds["connection"]["db2"])


@login_manager.user_loader
def load_user(uid):
    print("UID", uid)
    return db.get_user(uid)


# CUSTOMER ROUTES


@app.route("/")
def main_page():
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            str(uuid.uuid4()),
            request.form["name"],
            request.form["email"],
            request.form["password"],
            UserType.CUSTOMER,
            request.form["language"],
        )

        if db.create_user(user):
            return redirect(url_for("login"))
        else:
            return render_template("customer_register.html", error="Invalid user data")
    return render_template("customer_register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db.validate_user(email, password)
        if user:
            login_user(user, remember=True)
            session["user"] = user
            user.role = UserType(int(user.role))
            print("login", user)
            # TODO use the next parameter
            if current_user.role == UserType.CUSTOMER:
                return redirect(url_for("dashboard"))
            elif current_user.role == UserType.AGENT:
                return redirect(url_for("agent_dashboard"))
            elif current_user.role == UserType.ADMIN:
                return redirect(url_for("admin_dashboard"))
        else:
            return render_template("customer_login.html", error="Invalid credentials")
    else:
        return render_template("customer_login.html")


@app.route("/logout")
@login_required(UserType.CUSTOMER)
def logout():
    # TODO or redirect to main_page
    logout_user()
    return render_template("logout.html")


@app.route("/dashboard")
@login_required(UserType.CUSTOMER)
def dashboard():
    tickets = db.get_tickets_for_user(current_user)
    ticket_stats = {"open": 0, "closed": 0, "assigned": 0, "total": 0}
    for ticket in tickets:
        ticket_stats["total"] += 1
        if ticket.status == TicketStatus.OPEN:
            ticket_stats["open"] += 1
        elif ticket.status == TicketStatus.CLOSED:
            ticket_stats["closed"] += 1
        elif ticket.status == TicketStatus.IN_PROGRESS:
            ticket_stats["assigned"] += 1

    return render_template(
        "customer_dashboard.html", user=current_user, tickets=tickets, ticket_stats=ticket_stats
    )


@app.route("/create_ticket", methods=["GET", "POST"])
@login_required(UserType.CUSTOMER)
def create_ticket():
    if request.method == "POST":
        ticket = db.create_ticket(
            Ticket.from_request(current_user, request.form["title"], request.form["description"])
        )
        return redirect(url_for("dashboard"))
    else:
        return render_template("create_ticket.html")


# AGENT ROUTES
@app.route("/agent_dashboard")
@login_required(UserType.AGENT)
def agent_dashboard():
    return render_template("agent_dashboard.html")


# ADMIN ROUTES
@app.route("/admin_dashboard")
@login_required(UserType.ADMIN)
def admin_dashboard():
    return render_template("admin_dashboard.html")


app.run(debug=True)
