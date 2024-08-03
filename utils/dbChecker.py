"""
This file contains the database schemas for the app.

The database consists of three tables:
1. Users: stores information about the users, including their username, email, password, profile picture, role, points, creation date, creation time, and verification status.
2. Posts: stores information about the posts, including their title, tags, content, author, date, time, views, last edit date, and last edit time.
3. Comments: stores information about the comments, including the post they are associated with, the comment text, the user who wrote the comment, the date, and the time.

This file contains functions to create the tables if they do not already exist, and to ensure that they have the correct structure.
"""

from constants import *
import sqlite3
from os import mkdir
from utils.log import Log
from utils.time import currentTime
from os.path import exists
from passlib.hash import sha512_crypt as encryption
import stat



def dbFolder():
    match exists(DB_FOLDER_ROOT):
        case True:
            Log.app(f'Database folder: "/{DB_FOLDER_ROOT}" found')
        case False:
            Log.danger(f'Database folder: "/{DB_FOLDER_ROOT}" not found')
            mkdir(DB_FOLDER_ROOT)
            Log.success(f'Database folder: "/{DB_FOLDER_ROOT}" created')

def usersTable():
    """
    Checks if the users' table exists in the database, and create it if it does not.
    Checks if default admin is true create an admin user with custom admin account settings if it is.

    Returns:
        None
    """
    match exists(DB_USERS_ROOT):
        case True:
            Log.app(f'Users database: "{DB_USERS_ROOT}" found')
        case False:
            Log.danger(f'Users database: "{DB_USERS_ROOT}" not found')
            open(DB_USERS_ROOT, "x")
            Log.success(f'Users database: "{DB_USERS_ROOT}" created')
    os.chmod(DB_USERS_ROOT, stat.S_IRUSR | stat.S_IWUSR)
    Log.sql(f"Connecting to '{DB_USERS_ROOT}' database")
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.sql)
    cursor = connection.cursor()
    try:
        cursor.execute("""select userID from users; """).fetchall()
        Log.app(f'Table: "users" found in "{DB_USERS_ROOT}"')
        connection.close()
    except:
        Log.danger(f'Table: "users" not found in "{DB_USERS_ROOT}"')
        usersTable = """
        create table if not exists Users(
            "userID"    integer not null unique,
            "userName"  text unique not null,
            "email" text unique not null,
            "password"  text not null,
            "profilePicture" text not null,
            "role"  text not null,
            "points"    integer not null,
            "timeStamp" text not null,
            "isVerified"    text not null,
            primary key("userID" autoincrement)
        );"""
        cursor.execute(usersTable)
        match DEFAULT_ADMIN:
            case True:
                password = encryption.hash(DEFAULT_ADMIN_PASSWORD)
                cursor.execute(
                    """
                    insert into Users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) \
                    values(?,?,?,?,?,?,?,?)
                    """,
                    (
                        DEFAULT_ADMIN_USERNAME,
                        DEFAULT_ADMIN_EMAIL,
                        password,
                        DEFAULT_ADMIN_PROFILE_PICTURE,
                        "admin",
                        DEFAULT_ADMIN_POINT,
                        currentTime(),
                        "True",
                    ),
                )
                connection.commit()
                Log.success(f'Admin: "{DEFAULT_ADMIN_USERNAME}" added to database as initial admin')
        connection.commit()
        connection.close()
        Log.success(f'Table: "users" created in "{DB_USERS_ROOT}"')


def postsTable():
    match exists(DB_POSTS_ROOT):
        case True:
            Log.app(f'Posts database: "{DB_POSTS_ROOT}" found')
        case False:
            Log.danger(f'Posts database: "{DB_POSTS_ROOT}" not found')
            open(DB_POSTS_ROOT, "x")
            Log.success(f'Posts database: "{DB_POSTS_ROOT}" created')
    os.chmod(DB_POSTS_ROOT, stat.S_IRUSR | stat.S_IWUSR)

    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)
    cursor = connection.cursor()
    try:
        cursor.execute("""select id from posts; """).fetchall()
        Log.app(f'Table: "posts" found in "{DB_POSTS_ROOT}"')
        connection.close()
    except:
        Log.danger(f'Table: "posts" not found in "{DB_POSTS_ROOT}"')
        postsTable = """
        CREATE TABLE "posts" (
            "id"    integer not null unique,
            "title" text not null,
            "tags"  text not null,
            "content"   text not null,
            "banner"    BLOB not null,
            "author"    text not null,
            "views" integer not null,
            "timeStamp" text not null,
            "lastEditTimeStamp" text not null,
            "category"  text not null,
            primary key("id" autoincrement)
        );"""
        cursor.execute(postsTable)
        connection.commit()
        connection.close()
        Log.success(f'Table: "posts" created in "{DB_POSTS_ROOT}"')


def commentsTable():
    match exists(DB_COMMENTS_ROOT):
        case True:
            Log.app(f'Comments database: "{DB_COMMENTS_ROOT}" found')
        case False:
            Log.danger(f'Comments database: "{DB_COMMENTS_ROOT}" not found')
            open(DB_COMMENTS_ROOT, "x")
            Log.success(f'Comments database: "{DB_COMMENTS_ROOT}" created')
    os.chmod(DB_COMMENTS_ROOT, stat.S_IRUSR | stat.S_IWUSR)

    Log.sql(f"Connecting to '{DB_COMMENTS_ROOT}' database")
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    connection.set_trace_callback(Log.sql)
    cursor = connection.cursor()
    try:
        cursor.execute("""select id from comments; """).fetchall()
        Log.app(f'Table: "comments" found in "{DB_COMMENTS_ROOT}"')
        connection.close()
    except:
        Log.danger(f'Table: "comments" not found in "{DB_COMMENTS_ROOT}"')
        commentsTable = """
        create table if not exists comments(
            "id"    integer not null,
            "post"  integer not null,
            "comment"   text not null,
            "user"  text not null,
            "timeStamp" text not null,
            "parent_id" integer,
            "parent_user" text,
            primary key("id" autoincrement),
            foreign key("parent_id") references comments("id")
        );"""
        cursor.execute(commentsTable)
        connection.commit()
        connection.close()
        Log.success(f'Table: "comments" created in "{DB_COMMENTS_ROOT}"')
