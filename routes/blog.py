import base64
from flask import render_template, Blueprint, redirect, current_app

blogBlueprint = Blueprint("blog", __name__)


@blogBlueprint.route("/")
@blogBlueprint.route("/by=<by>/sort=<sort>")
def blog(by="timeStamp", sort="desc"):
    # byOptions = ["timeStamp", "title", "views", "category", "lastEditTimeStamp"]
    # sortOptions = ["asc", "desc"]
    posts_collection = current_app.mongo_db['posts']
    # 执行查询并排序
    posts = list(posts_collection.find().sort(by, 1 if sort.lower() == 'asc' else -1))
    # 将结果转换为列表
    for post in posts:
        post['_id'] = str(post['_id'])
        post['banner'] = base64.b64encode(post['banner']).decode('utf-8')

    # for i in range(len(posts)):
    #     post = list(posts[i])
    #     base64_image = base64.b64encode(post["banner"]).decode('utf-8')
    #     post["banner"] = base64_image
    #     posts[i] = post
    # match by:
    #     case "timeStamp":
    #         by = "Creation Date"
    #     case "lastEditTimeStamp":
    #         by = "Last Edit Date"
    # sortName = f"{by} {sort}".title()
    return render_template("blog.html", posts=posts, nums=len(posts))
