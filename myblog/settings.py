import os
import pymysql
from flask_uploads import IMAGES
pymysql.install_as_MySQLdb()

__author__ = "yjw"

DEBUG = True
SECRET_KEY = "jsjkafhh8233gh7y8z8ycwheoih83u9hau934uo4#ho9hd3"
# 配置数据库执行文件
SQLALCHEMY_DATABASE_URI = "mysql://root:842655@localhost:3306/flask"

SQLALCHEMY_TRACK_MODIFICATIONS = False
# 图片上传路径
UPLOADED_PHOTO_DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   "static/uploads/")
# 头像上传格式
UPLOADED_PHOTO_ALLOW = IMAGES
