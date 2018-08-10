import json
from flask import Blueprint,request,render_template,jsonify
from user.models import db, Article,Comment
from common_function import after_login

article = Blueprint("article",__name__)

@article.route("/write/",methods=["GET","POST"])
@after_login
def write():
    if request.method == "GET":
        return render_template("article/write.html")
    elif request.method == "POST":
        data = json.loads(request.data.decode())
        user_id = data.get("user_id")
        title = data.get("title")
        content = data.get("content")
        if user_id == "":
            warn = "您还没有登录，请登录后再发表！"
        article = Article(titile=title,content=content,user_id=user_id)
        # 提交到数据库
        db.session.add(article)
        db.session.commit()
        return jsonify("发表成功！")

@article.route("/<pk>/",methods=["GET","POST"])
def show(pk):
    if request.method == "GET":
        # 获取所有的文章
        article = Article.query.get(pk)
        article_dict = article.to_dict()
        for comment in article_dict["comments"]:
            # 获得评论对象
            comment_obj = Comment.query.get(comment.get("id"))
            comment["username"] = comment_obj.user.username
        return render_template('article/show_article.html',article=article_dict)

    elif request.method == "POST":
        data = request.data.decode()
        # 转为字典数据
        data_dict = json.loads(data)
        if data_dict.get("user_id") == "":
            return jsonify("您还没有登录,请先登录后再评论")
        content = data_dict.get("data")
        user_id = data_dict.get("user_id")
        article_id = data_dict.get("article_id")
        # 判断是否为空
        if content == "":
            warn = "请输入文字再提交！"
            return jsonify(warn)
        else:
            comment = Comment(content=content,user_id=user_id,article_id=article_id)
            db.session.add(comment)
            db.session.commit()
            return jsonify("发表成功")

