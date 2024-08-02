# -*- coding: utf-8 -*-
"""
File:       __init__.py
Time:       2024-07-17-08:16
User:       zhl

此模块包含一些工具函数
"""
from .errorHandler import *
from .form import *


# 用于处理日期和时间相关的操作。
from .time import currentDate, currentTime, currentTimeStamp, currentTimeZone

# 用于记录日志消息。
from .log import Log


from .dbChecker import dbFolder, usersTable, postsTable, commentsTable
