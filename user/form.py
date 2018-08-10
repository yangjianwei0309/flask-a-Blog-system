from flask_wtf import FlaskForm
from flask_uploads import UploadSet,configure_uploads
# from wtforms.fields import core
# from wtforms.fields import html5
from wtforms.fields import simple
from wtforms.validators import EqualTo
from wtforms import validators
from wtforms import widgets

class LoginForm(FlaskForm):
    username = simple.StringField(label="用户名",
    # 表单数据验证
    validators = [
        validators.DataRequired(message='用户名不能为空')
    ],
    widget=widgets.TextInput(),
    render_kw={'class':'form-control',
               "placeholder":"用户名"}
    )
    password = simple.PasswordField(label="密 码",
    validators=[
        validators.DataRequired(message='密码不能为空')
    ]
    ,widget=widgets.PasswordInput(),
    render_kw={'class':'form-control',
               "placeholder":"密码"}
    )

class RegisterForm(FlaskForm):
    username = simple.StringField(label="请输入用户名：",
    validators=[
        validators.DataRequired(message="用户名不能为空"),
        validators.Length(min=6, max=18, message='用户名长度必须大于%(min)d,且小于%(max)d')
    ],
    widget=widgets.TextInput(),render_kw={"class":"form-control"}
    )
    password = simple.StringField(label="请输入密码：",
    validators=[
        validators.DataRequired(message="密码不能为空"),
        validators.Length(min=8,message="密码至少%(min)d位"),
        validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
                                "[A-Za-z\d~!@#$%^&*()_+]{8,}",
                          message="密码至少包含1个小写和大写字母以及1个数字")
    ],
    widget=widgets.PasswordInput(),render_kw={"class":"form-control"})
    # 确认密码
    password2 = simple.StringField(label="请确认密码：",
    validators=[
        validators.DataRequired(message="请确认您的密码"),
        EqualTo("password",message="两次密码输入不一致")
    ],
    widget=widgets.PasswordInput(),render_kw={"class":"form-control",
                                              "placeholder":"确认密码"}
    )


