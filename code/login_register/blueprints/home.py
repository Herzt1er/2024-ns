from flask import Blueprint, render_template, session, redirect, url_for, request

home = Blueprint("home", __name__, url_prefix="/")

@home.route("/")
def welcome():
    return render_template("index.html")
   

@home.route("/index")
def index():
    user= g.user
    files = File.query.filter(File.user_id == user.user_id).all()
    return render_template("index.html", username=user.username, files=files)
   