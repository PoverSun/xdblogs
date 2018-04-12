# -*- coding: utf-8 -*-

from django.forms import forms
from django.forms import CharField,EmailField,BooleanField


#注册验证

class FrontRegistForm(forms.Form):
    username = CharField(min_length=4,error_messages={"required": "用户名最少4位数",})
    email = EmailField(required=True)
    password = CharField(min_length=6,error_messages={"required": "用户名最少6位数",})



    #等录验证
class FrontLoginForm(forms.Form):
    email = EmailField(min_length=4)
    password = CharField(min_length=6)
    remember_me = BooleanField(required=False)

#add_article
class AddArticleForm(forms.Form):
    title = CharField(min_length=6,error_messages={'required':u'标题不能为空！'})
    subtitle = CharField(required=False)

#edit_article
class EditArticleForm(AddArticleForm):
    pass

#update_password

class FrontResetPwdForm(forms.Form):
    password = CharField(required=True)
    new_password = CharField(min_length=6)
    repeat_password = CharField(min_length=6)