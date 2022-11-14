import ibm_db
import ibm_db_dbi

from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models import Ticket, User, UserType
from utils import valid_user_data
from typing import Optional


class IBMdb2:
    def __init__(self, db2):
        self.conn = ibm_db.connect(
            f"DATABASE={db2['database']};HOSTNAME={db2['hosts'][0]['hostname']};PORT={db2['hosts'][0]['port']};PROTOCOL=TCPIP;UID={db2['authentication']['username']};PWD={db2['authentication']['password']};SECURITY=SSL",
            "",
            "",
        )
        ibm_db.autocommit(self.conn, ibm_db.SQL_AUTOCOMMIT_ON)

    def create_user(self, user: User):
        if not valid_user_data(user):
            return False

        insert_stmt = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare(self.conn, insert_stmt)
        params = (
            str(uuid.uuid4()),
            user.name,
            user.email,
            generate_password_hash(user.password),
            user.role.value,
            user.language if isinstance(user.language, str) else user.language.value,
        )
        ibm_db.execute(stmt, params)
        return True

    def get_user(self, uid):
        stmt = ibm_db.prepare(self.conn, "SELECT * FROM users WHERE uid = ?")
        ibm_db.bind_param(stmt, 1, uid)
        ibm_db.execute(stmt)

        user_data = ibm_db.fetch_tuple(stmt)
        print("get_user data", user_data)
        if user_data:
            user = User(*user_data)
            user.role = UserType(int(user.role))
            return user
        return None

    def get_user_from_email(self, email):
        stmt = ibm_db.prepare(self.conn, "SELECT * FROM users WHERE email = ?")
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)

        user_data = ibm_db.fetch_tuple(stmt)
        if user_data:
            user = User(*user_data)
            user.role = UserType(int(user.role))
            return user
        return None

    def validate_user(self, email, password) -> Optional[User]:
        # Save a db call
        if not valid_user_data(User("", "DUMMY_USER", email, password, UserType.ANY)):
            return None
        user = self.get_user_from_email(email)
        if user and check_password_hash(user.password, password):
            return user
        return None

    def create_ticket(self, ticket: Ticket):
        insert_stmt = "INSERT INTO tickets (uid, author, title, description, priority, status) VALUES (?, ?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare(self.conn, insert_stmt)
        params = (
            str(uuid.uuid4()),
            ticket.author.uid,
            ticket.title,
            ticket.description,
            ticket.priority.value,
            ticket.status.value,
        )
        ibm_db.execute(stmt, params)
        return True

    def get_tickets_for_user(self, user: User):
        stmt = ibm_db.prepare(self.conn, "SELECT * FROM tickets WHERE author = ?")
        ibm_db.bind_param(stmt, 1, user.uid)
        ibm_db.execute(stmt)

        tickets = []
        row = ibm_db.fetch_tuple(stmt)
        while row:
            tickets.append(Ticket.from_tuple(user, row))
            row = ibm_db.fetch_tuple(stmt)
        return tickets
