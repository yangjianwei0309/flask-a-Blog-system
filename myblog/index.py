from flask import Flask,render_template
from flask_uploads import UploadSet,configure_uploads
from PIL import Image
from comment.views import article
from user.models import db,User,Article

app = Flask(__name__,template_folder="../templates",static_folder="../static")

app.config.from_object("myblog.settings")
# db初始化
db.init_app(app)
# 博客首页视图函数
@app.route('/')
def index():
    articles = Article.query.all() # list
    articles_list = []
    # 遍历文章对象列表
    for article in articles:
        article_dict = article.to_dict()
        article_user = User.query.get(article.user_id)
        article_dict["user"] = article_user.username
        articles_list.append(article_dict)
    return render_template('index.html',articles=articles_list)

# 注册蓝图(user)
from user.views import user
app.register_blueprint(user,url_prefix="/user")
# 注册蓝图(article)
app.register_blueprint(article,url_prefix="/article")

# 创建上传对象的实例
photo = UploadSet("photo",Image)
# 配置
configure_uploads(app,photo)