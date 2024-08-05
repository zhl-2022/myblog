from utils import *
from flask import render_template, flash, session, request, redirect, Blueprint, current_app
from constants import *
from routes import verify_recaptcha, verify_form
from bson import Binary
from models import Post
import base64
addBlueprint = Blueprint("add", __name__)


@addBlueprint.route("/add", methods=["GET", "POST"])
def add():
    if not session.get("isVerified"):
        flash(f"You are not logged in Or not Verified, Sorry!", "error")
        return redirect("/contact")
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        verify_form(CreatePostForm(request.form))
        postTitle = request.form["postTitle"]
        postTags = request.form["postTags"]
        postContent = request.form["postContent"]
        postBanner = request.files["postBanner"].read()
        postCategory = request.form["postCategory"]
        posts_collection = current_app.mongo_db['posts']
        post = Post(postTitle, postTags, postContent, postBanner, session["userName"], postCategory)
        try:
            posts_collection.insert_one(post.todict())
            flash("You earned 20 points by posting.", "success")
            return redirect("/")
        except Exception as e:
            flash(f"An error occurred while posting: {e}", "error")
    else:
        return render_template("add.html", siteKey=RECAPTCHA_SITE_KEY)
