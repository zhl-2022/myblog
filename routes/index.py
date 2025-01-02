# -*- coding: utf-8 -*-
"""
File:       index.py
Time:       2025-01-02-22:05
User:       zhl
Details:       
"""
from flask import render_template, Blueprint

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/index")
def blog(by="timeStamp", sort="desc"):
    return render_template("index.html")