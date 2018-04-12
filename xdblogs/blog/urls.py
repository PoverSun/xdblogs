# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date:   2018-01-15 10:45:44
# @Last Modified by:   xiaodong
# @Last Modified time: 2018-01-15 12:06:30

from django.conf.urls import url
from blog import views


urlpatterns = [
	url(r'^(?P<page>[\d]{1,2})/$',views.index,name='front_index'),
	url(r'^/$',views.index,name='front_index'),
	url(r'^about/$',views.about,name='front_about'),
	url(r'^contact/$',views.contact,name='front_contact'),
	url(r'^test/$',views.test,name='test'),
	url(r'^front_login/$',views.front_login,name='front_login'),
	url(r'^front_regist/$',views.front_regist,name='front_regist'),
	url(r'^add_article/$',views.front_add_article,name='front_add_article'),
	url(r'^edit_article/(?P<uid>[\w\-]+)/$',views.front_edit_article,name='front_edit_article'),
	url(r'^front_article_detail/(?P<uid>[\w\-]+)/$',views.front_article_detail,name='front_article_detail'),
	url(r'^front_logout/$',views.front_logout,name='front_logout'),
	url(r'^front_settings/$',views.front_settings,name='front_settings'),
	url(r'^front_reset_pwd/$',views.front_reset_pwd,name='front_reset_pwd'),
	url(r'^front_article_delete/(?P<uid>[\w\-]+)/$',views.front_article_delete,name='front_article_delete'),
	url(r'^front_restore_delete/(?P<uid>[\w\-]+)/$',views.front_restore_delete,name='front_restore_delete'),
]