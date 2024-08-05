# -*- coding: utf-8 -*-
"""
File:       models.py
Time:       2024-08-04-21:16
User:       zhl
Details:       
"""
from constants import USER_PROFILE_PICTURE, RADIUS_PROFILE_PICTURE
from utils.time import currentTime


class User:
    def __init__(self, userName, email, password, profilePicture=None, timeStamp=None, isVerified=False):
        self.userName = userName
        self.email = email
        self.password = password
        self.profilePicture = profilePicture if profilePicture else f"{USER_PROFILE_PICTURE}{userName}{RADIUS_PROFILE_PICTURE}"
        self.timeStamp = timeStamp if timeStamp else currentTime()
        self.isVerified = isVerified

    def todict(self):
        return self.__dict__


class Post:
    def __init__(self, title, tags, content, banner, author, category):
        self.title = title
        self.tags = tags
        self.content = content
        self.banner = banner
        self.author = author
        self.views = 0
        self.timeStamp = currentTime()
        self.lastEditTimeStamp = currentTime()
        self.category = category

    # def save(self):
    #     db.posts.insert_one(self.__dict__)
    def todict(self):
        return self.__dict__


class Comment:
    def __init__(self, post, comment, user, parent_id=None, parent_user=None):
        self.post = post
        self.comment = comment
        self.user = user
        self.timeStamp = currentTime()
        self.parent_id = parent_id
        self.parent_user = parent_user

    # def save(self):
    #     db.comments.insert_one(self.__dict__)
    def todict(self):
        return self.__dict__
