from ..utils import *
from flask import render_template, flash, session, request, redirect, Blueprint
from ..constants import *
from . import verify_recaptcha, addPoints, verify_form
from ..factory import get_db2, get_db1

addBlueprint = Blueprint("add", __name__)


@addBlueprint.route("/add", methods=["GET", "POST"])
def add():
    if session.get("role") != 'admin':
        flash(f"You are not logged in Or not an administrator Sorry!", "error")
        return redirect("/contact")
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        verify_form(CreatePostForm(request.form))
        postTitle = request.form["postTitle"]
        postTags = request.form["postTags"]
        postContent = request.form["postContent"]
        postBanner = request.files["postBanner"].read()
        postCategory = request.form["postCategory"]
        print(f"postContent {postContent}")
        db_post = get_db1()
        cursor_post = db_post.cursor()
        cursor_post.execute("insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category)  values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (postTitle, postTags, postContent, postBanner, session["userName"], 0, currentTime(), currentTime(), postCategory))
        db_post.commit()
        Log.success(f'Post: "{postTitle}" posted by "{session["userName"]}"')
        addPoints(20, session["userName"])
        flash("You earned 20 points by posting.", "success")
        return redirect("/")
    else:
        return render_template("add.html", siteKey=RECAPTCHA_SITE_KEY)
