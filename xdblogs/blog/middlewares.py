# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from models import Author

class FrontUserMiddleWare(MiddlewareMixin):

    def process_request(self,request):
        front_username = request.session.get('front_user')
        front_user = Author.objects.filter(name=front_username).first()
        if front_user:
            if not hasattr(request,'front_user'):
                setattr(request,'front_user',front_user)

