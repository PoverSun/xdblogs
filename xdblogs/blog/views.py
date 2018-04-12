# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from models import Author,Tags,Categorys,Articles
from forms import FrontLoginForm,FrontRegistForm,AddArticleForm,FrontResetPwdForm,EditArticleForm
from django.views.decorators.http import require_http_methods
import json
from decorator import front_logined_required
from utils import xdjson
from xdblogs.settings import PAGE_NUM
# Create your views here.


def index(request,page):
    c_page = int(page)
    articles = Articles.objects.filter(is_active=True).order_by('-pub_time').all()
    #文章总数
    article_counts = articles.count()
    all_pages = article_counts/PAGE_NUM
    if article_counts%PAGE_NUM > 0:
        all_pages = all_pages+1

    start = (c_page-1) * PAGE_NUM
    end = start + PAGE_NUM
    articles = articles[start:end]
    pages = []
    # 往前遍历
    temp_page = c_page - 1
    while temp_page >= 1:
        if temp_page % 5 == 0:
            break
        else:
            pages.append(temp_page)
            temp_page = temp_page -1

    # 往后遍历
    temp_page = c_page
    while temp_page <= all_pages:
        if temp_page % 5 == 0:
            pages.append(temp_page)
            break
        else:
            pages.append(temp_page)
            temp_page = temp_page+1

    author = Author.objects.all()
    context = {
        'articles':articles,
        'authors':author,
        't_page': c_page,
        'c_page':page,
        'all_pages':all_pages,
        'pages':pages
    }
    if hasattr(request,'front_user'):
        context['front_user']=request.front_user
    return render(request,'front_index.html',context)


#-----------------------关于页面
def about(request):

	return render(request,'front_about.html')


#-----------------------关于页面




#-----------------------联系页面
def contact(request):

	return render(request,'front_contact.html')
#-----------------------联系页面


#-----------------------login
@require_http_methods(['GET','POST'])
def front_login(request):
    if request.method == 'GET':
        return render(request, 'front_login.html')
    else:
        form = FrontLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            if remember_me:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)
            front_user = Author.objects.filter(email=email).first()

            if front_user:
                if front_user.check_password(password):
                    request.session['front_user']=front_user.name
                    return redirect(reverse('front_index'),page=1)
                else:
                    return render(request, 'front_login.html', {'error': '抱歉，密码错误，请重新输入！！'})
            else:
                return render(request, 'front_login.html', {'error': '此账户不存在，请重新输入！！'})
        else:
            return render(request, 'front_login.html', {'error': '表单验证失败，请重新输入！'})

#------------------------------------------logout
def front_logout(request):
    try:
        del request.session['front_user']
        return redirect(reverse('front_index'),page=1)
    except Exception,e:
        print e
        return redirect(reverse('front_index'),page=1)





#------------------------------------------regist

@require_http_methods(['GET','POST'])
def front_regist(request):
    if request.method == 'GET':
        return render(request,'front_regist.html')
    else:
        form = FrontRegistForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            if email:
                front_usermodel = Author.objects.filter(email=email).first()
                if not front_usermodel:
                    front_user = Author(name=username,email=email)
                    front_user.set_password(password)
                    front_user.save()
                    return render(request,'front_regist.html',{'info':'恭喜您！注册成功！'})
                else:
                    return render(request,'front_regist.html',{'error':'此邮箱已注册，请重新输入！'})
        else:
            return render(request,'front_regist.html',{'error':'表单验证失败！'})

#------------------------------------------regist_end

#-------------------------------------------add_article
@front_logined_required
@require_http_methods(['GET','POST'])
def front_add_article(request):
    if request.method == 'GET':
        categorys = Categorys.objects.all()
        tags = Tags.objects.all()
        context ={
            'categorys':categorys,
            'tags':tags
        }
        if hasattr(request,'front_user'):
            context['front_user']=request.front_user
        return render(request,'front_add_article.html',context)
    else:
        form =AddArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            subtitle = form.cleaned_data.get('subtitle')
            data = request.POST
            tags = request.POST.getlist('tags[]')
            context = {}
            for k,v in data.iteritems():
                context[k]=v
            category_name = context['category']#获取分类
            categoryModel = Categorys.objects.filter(name=category_name).first()
            current_user = request.front_user
            article_content = context['textarea_content']
            articleModel = Articles(title=title,subtitle=subtitle,
                                    categorys=categoryModel,author=current_user,content=article_content)
            articleModel.save()
            for tag in tags:
                tagModel = Tags.objects.filter(pk=tag).first()
                articleModel.tags.add(tagModel)
            data = {
                'code':200,
                'info':u'恭喜您！文章发布成功！'
            }
            return JsonResponse(data)
        else:
            return render(request,'front_add_article.html',{
                'error':'表单验证出错！'
            })
#-------------------------------------------add_article-end

#--------------------------------------------edit_article
@front_logined_required
@require_http_methods(['GET','POST'])
def front_edit_article(request,uid=''):
    if request.method == 'GET':
        article = Articles.objects.filter(pk=uid).first()
        categorys = Categorys.objects.all()
        tags = Tags.objects.all()
        context = {
            'article':article,
            'categorys':categorys,
            'tags':tags,
            'front_user':request.front_user
        }
        return render(request,'front_edit_article.html',context)
    else:
        form = EditArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            subtitle = form.cleaned_data.get('subtitle')
            data = request.POST
            tags = request.POST.getlist('tags[]')
            context = {}
            for k, v in data.iteritems():
                context[k] = v
            category_name = context['category']  # 获取分类
            categoryModel = Categorys.objects.filter(name=category_name).first()
            current_user = request.front_user
            article_content = context['textarea_content']
            articleModel = Articles.objects.filter(pk=uid).first()
            articleModel.title=title
            articleModel.subtitle =subtitle
            articleModel.categorys = categoryModel
            articleModel.author = current_user
            articleModel.content = article_content
            articleModel.save()
            for tag in tags:
                tagModel = Tags.objects.filter(pk=tag).first()
                articleModel.tags.add(tagModel)
            return xdjson.json_result(message=u'恭喜您！文章修改成功！')
        else:
            return xdjson.json_method_error(message=u'表单验证出错！')

#--------------------------------------------edit_article_end

#-----------------------------------------------article-delete
@front_logined_required
@require_http_methods(['GET'])
def front_article_delete(request,uid=''):
    article = Articles.objects.filter(pk=uid).first()
    if article:
        article.is_active = False
        article.save()
        return redirect(reverse('front_settings'))

    else:
        return xdjson.json_method_error(message=u'此文章不存在，无法移除！')


@front_logined_required
@require_http_methods(['GET'])
def front_restore_delete(request,uid=''):
    article = Articles.objects.filter(pk=uid).first()
    if article:
        article.is_active = True
        article.save()
        return redirect(reverse('front_settings'))

    else:
        return xdjson.json_method_error(message=u'此文章不存在，无法操作！')
#-----------------------------------------------article-delete——end


#article_detail_page
def front_article_detail(request,uid=''):
    article = Articles.objects.filter(pk=uid).first()

    if not article:
        return HttpResponse(u'此文章不存在!')

    else:
        category = article.categorys

        context ={
            'article':article,
            'category':category
        }
        if hasattr(request, 'front_user'):
            context['front_user']=request.front_user
        return render(request,'front_article_detail.html',context)

#------------------------------------------article_detail_end
@front_logined_required
@require_http_methods(['GET'])
def front_settings(request):
    user = request.front_user
    articles = Articles.objects.filter(author=user).all()
    context = {
        'front_user':user,
        'articles':articles
    }
    return render(request, 'front_settings.html',context)


@front_logined_required
@require_http_methods(['POST'])
def front_reset_pwd(request):
    form = FrontResetPwdForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        new_password = form.cleaned_data.get('new_password')
        repeat_password = form.cleaned_data.get('repeat_password')
        if password:
            user = request.front_user
            if user.check_password(password):
                if new_password == repeat_password:
                    userModel = Author.objects.filter(pk=user.uid).first()
                    userModel.set_password(new_password)
                    return xdjson.json_result(message=u'恭喜您！密码修改成功！')
                else:
                    return xdjson.json_params_error(message=u'两次密码输入不一致，请重新输入！')
            else:
                return xdjson.json_params_error(message=u'原始密码错误！请重新输入！')
        else:
            return xdjson.json_params_error(message=u'表单验证出错，原始密码不能为空')
    else:
        return xdjson.json_params_error(message=u'密码输入不能少于6位数，请重新输入！')



def test(request):
    title = u'何以解忧，唯有前行！'
    subtitle = u'何以解忧，唯有杜康'
    content = u'我其实很久以前就读了东野圭吾的《解忧杂货店》，感觉这是一本最不像东野圭吾的小说，没有他一贯的引人注目的悬疑和推理，看似十分凌乱。初读的时候，很容易被众多的人物和错乱的时空搞得莫名奇妙。但是，当你真正读懂读通，理清了小说的时间顺序和人物关系，你就会发现它仍旧是东野圭吾的风格，故事缜密又奇妙。'
    author = Author.objects.filter(name='xiaoxiao').first()
    categorys = Categorys.objects.get(pk=3)
    tag = Tags.objects.get(pk=3)
    article = Articles(title=title,subtitle=subtitle,content=content,author=author,categorys=categorys)
    # article = Articles.objects.all().first()
    for i in range(50):
        article.save()
        article.tags.add(tag)
    return HttpResponse('success')





