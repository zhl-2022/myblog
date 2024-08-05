from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone

uri = "mongodb+srv://zhl:zhlzhl@cluster0.u7z4pkb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['myblog']

# 创建 Users 集合并插入文档
users_collection = db['Users']
users_collection.insert_one({
    "userID": 1,
    "userName": "exampleUser",
    "email": "user@example.com",
    "password": "password123",
    "profilePicture": b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\xa0\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0bIDATx\xdacddbf\xa0\x040Q\xa4\x00\x00\x00\x00IEND\xaeB`\x82',  # 示例图片数据
    "timeStamp": datetime.now(timezone.utc),
    "isVerified": False
})

# 创建 Posts 集合并插入文档
posts_collection = db['Posts']
posts_collection.insert_one({
    "id": 1,
    "title": "Example Post",
    "tags": "example, post",
    "content": "This is an example post.",
    "banner": b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\xa0\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0bIDATx\xdacddbf\xa0\x040Q\xa4\x00\x00\x00\x00IEND\xaeB`\x82',  # 示例图片数据
    "author": "exampleUser",
    "views": 100,
    "timeStamp": datetime.now(timezone.utc),
    "lastEditTimeStamp": datetime.now(timezone.utc),
    "category": "example"
})

# 创建 Comments 集合并插入文档
comments_collection = db['Comments']
comments_collection.insert_one({
    "id": 1,
    "post": 1,
    "comment": "This is an example comment.",
    "user": "exampleUser",
    "timeStamp": datetime.now(timezone.utc),
    "parent_id": None,
    "parent_user": None
})
