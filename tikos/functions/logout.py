from flask import session

def logout_app():
    session.pop("login")
