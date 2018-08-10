from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String(64),unique=True,nullable=False)
    password = db.Column(db.String(128),nullable=False)
    icon = db.Column(db.String(500),nullable=True)
    # ablout_me
    about_me = db.Column(db.String(150),nullable=True)
    # 建立反向引用
    comments = db.relationship('Comment',backref='user')

    def __str__(self):
        return self.username

    def to_dict(self):
        return dict(id=self.id,
                    username=self.username,
                    icon=self.icon,
                    about_me=self.about_me,
                    comments=[comment.to_dict()for comment in self.comments])

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True)
    # 评论内容
    content = db.Column(db.String(500))
    # 外键关联
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    article_id = db.Column(db.Integer,db.ForeignKey("article.id"))

    def to_dict(self):
        return dict(id=self.id,
                    content=self.content,
                    user_id=self.user_id,
                    article_id=self.article_id)

# 多对多关系
ships = db.Table("ships",
    db.Column('user.id',db.Integer,db.ForeignKey("user.id")),
    db.Column('article.id',db.Integer,db.ForeignKey("article.id")))

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer,primary_key=True)
    # 文章标题
    titile = db.Column(db.String(500),nullable=False)
    # 内容
    content = db.Column(db.String(5000),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    users = db.relationship("User",secondary=ships,backref=
    db.backref("articles",lazy="dynamic"))
    # 反向应用
    comments = db.relationship("Comment",backref="article")

    def to_dict(self):
        return dict(id=self.id,
                    title=self.titile,
                    content=self.content,
                    user_id=self.user_id,
                    comments=[comment.to_dict()for comment in self.comments])

