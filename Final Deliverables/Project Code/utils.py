from flask import current_app
from models import User
import re
from models import UserType
from functools import wraps
from flask_login import current_user


def valid_user_data(user: User):
    if not user.name or not user.email or not user.password:
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        return False
    return True


def login_required(role: UserType = UserType.ANY):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print(current_user, "ADA")
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            print("Login requed?", role, current_user.role)
            if role != UserType.ANY and current_user.role != role:
                return current_app.login_manager.unauthorized()

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
