# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here
from models import Author,Articles,Categorys,Tags


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','email','is_active')
    search_fields = ('name','email')

class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title','pub_time','author','update_time')
    list_filter = ('title','pub_time','author','update_time')

admin.site.register(Author,AuthorAdmin)
admin.site.register(Articles,ArticlesAdmin)
admin.site.register(Categorys)
admin.site.register(Tags)