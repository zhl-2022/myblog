"""
This file contains the routes for the Flask application.

The Blueprint "index" is used to define the home page of the application.
The route "/" maps the index function to the home page.

The index function retrieves all posts from the database and passes them to the 404.html.jinja template.

The posts variable is passed to the 404.html.jinja template as a list of dictionaries.

The 404.html.jinja template displays the title and content of each post.
"""
import base64
from utils import Log
from flask import render_template, Blueprint, redirect
from routes import get_db1
blogBlueprint = Blueprint("blog", __name__)


@blogBlueprint.route("/")
@blogBlueprint.route("/by=<by>/sort=<sort>")
def blog(by="timeStamp", sort="desc"):
    """
    This function maps the home page route ("/") to the index function.

    It retrieves all posts from the database and passes them to the 404.html.jinja template.

    The posts variable is passed to the 404.html.jinja template as a list of dictionaries.

    The 404.html.jinja template displays the title and content of each post.

    Parameters:
    by (str): The field to sort by. Options are "timeStamp", "title", "views", "category", "lastEditTimeStamp".
    sort (str): The order to sort in. Options are "asc" or "desc".

    Returns:
    The rendered template of the home page with sorted posts according to the provided sorting options.
    """

    byOptions = ["timeStamp", "title", "views", "category", "lastEditTimeStamp"]
    sortOptions = ["asc", "desc"]

    match by not in byOptions or sort not in sortOptions:
        case True:
            Log.warning(
                f"The provided sorting options are not valid: By: {by} Sort: {sort}"
            )
            return redirect("/")

    db_post = get_db1()
    cursor_post = db_post.cursor()
    cursor_post.execute(f"select * from posts order by {by} {sort}")
    posts = cursor_post.fetchall()

    for i in range(len(posts)):
        post = list(posts[i])
        base64_image = base64.b64encode(post[4]).decode('utf-8')
        post[4] = base64_image
        posts[i] = post

    match by:
        case "timeStamp":
            by = "Creation Date"
        case "lastEditTimeStamp":
            by = "Last Edit Date"
    sortName = f"{by} {sort}".title()
    Log.info(f"Sorting posts on index page by: {sortName}")
    return render_template("blog.html", posts=posts, nums=len(posts))
