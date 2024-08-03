# -*- coding: utf-8 -*-
"""
File:       errorHandler.py
Time:       2024-07-22-18:05
User:       zhl
Details:    错误和响应后的页面处理
"""

from utils.log import Log
from flask import render_template, request


def notFoundErrorHandler(e):
    Log.danger(e)
    return render_template("error/404.html"), 404


def unauthorizedErrorHandler(e):
    Log.danger(e)
    return render_template('error/401.html'), 401


def internalErrorHandler(e):
    Log.danger(e)
    return render_template('error/500.html'), 500


def csrfErrorHandler(e):
    Log.danger(e)
    return render_template("error/400.html"), 400


def afterRequestLogger(response):
    match response.status:
        case "200 OK":
            Log.success(
                f"Adress: {request.remote_addr} | Method: {request.method} | Path: {request.path} | Scheme: {request.scheme} | Status: {response.status} | Content Length: {response.content_length} | Referrer: {request.referrer} | User Agent: {request.user_agent}",
            )
        case "304 NOT MODIFIED":
            pass  # 不打印日志

        case _:
            Log.info(
                f"Adress: {request.remote_addr} | Method: {request.method} | Path: {request.path} | Scheme: {request.scheme} | Status: {response.status} | Content Length: {response.content_length} | Referrer: {request.referrer} | User Agent: {request.user_agent}",
            )

    return response
