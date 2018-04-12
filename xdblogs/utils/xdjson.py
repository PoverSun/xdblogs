# -*- coding: utf-8 -*-
from django.http import JsonResponse


# 请求正常的json返回函数
def json_result(code=200,message='',data={},kwargs={}):
	json = {'code':code,'message':message,'data':data}
	if kwargs.keys():
		# 把json和kwargs合并成一个字典
		for k,v in kwargs.items():
			json[k] = v
	return JsonResponse(json)

def json_params_error(message=''):
	"""
		请求参数错误
	"""
	return json_result(code=400,message=message)

def json_unauth_error(message=''):
	"""
		没有权限访问
	"""
	return json_result(code=401,message=message)

def json_method_error(message=''):
	"""
		请求方法错误
	"""
	return json_result(code=405,message=message)
