# -*- coding: utf-8 -*-
from django.shortcuts import reverse,redirect

def front_logined_required(func):
    def wrapper(request,*args,**kwargs):
        user = request.session.get('front_user')
        if user:
            return func(request,*args,**kwargs)

        else:
            return redirect(reverse('front_login'))

    return wrapper