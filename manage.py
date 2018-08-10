from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from myblog.index import app
from user.models import db

# 创建管理对象
manager = Manager(app)

migrate = Migrate(app=app,db=db)
# 添加指令集
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()
