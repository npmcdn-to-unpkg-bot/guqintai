#coding=utf8
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime

from mongoengine import DoesNotExist
from mongoengine.queryset.visitor import Q
from models import Article

from markdown import markdown 

# Create your views here.
class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        d = request.GET.dict()
        para = {}
        page_num = int(d.get('page_num', 1))
        if page_num < 1:
            page_num = 1 
 
        try:
            item_num = 10
           
            page_start = (page_num -1 )* item_num
            page_end = page_num * item_num 

            total_num = Article.objects.count()  
            
            last_page = max(0, page_num-1)
            total_page = (total_num/item_num)+ 1
            end_page = total_page 
            next_page = min(end_page, page_num+1)

            a_list = list(Article.objects.filter(status=1).order_by('-create_time')[page_start:page_end])
            for i in a_list:
                i.content = markdown(i.content)
            para.update({"page_num": page_num,
                     "last_page": last_page,
                     "next_page": next_page,
                     'end_page': end_page,
                     'total_page': total_page,
                     'article_list': a_list})
        except DoesNotExist:
            para = {'article_list': None}
        para.update({'index_page':True})
        t = TemplateResponse(request, 'index.html', para)
        return t
    
    
class Post(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.session.get('account_id', None) is None:
            return HttpResponseRedirect('/account/login')
        para = {}
        t = TemplateResponse(request, 'post.html', para)
        return t
    
    
    def post(self, request, *args, **kwargs):
        if request.session.get('account_id', None) is None:
            return HttpResponseRedirect('/account/login')

        d = request.POST.dict()
        i = Article()
        account_id = request.session['account_id']
        i.account_id = str(account_id)
        i.username = request.session['username']
       
        tag = d.get('tag', None)   
        i.tag = tag.split(';')
        i.category = int(d['category'])
        i.head_image = d.get('head_image', None)
        i.title = d['title']
        i.content = d['content'] 
        i.status = 1
        i.save()

        return HttpResponseRedirect('/blog')

class Edit(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.session.get('account_id', None) is None:
            return HttpResponseRedirect('/account/login')
        article_id = kwargs['id']
        try:
            a = Article.objects.get(id=article_id)
            kwargs['article'] = a
        except DoesNotExist:
            pass
        t = TemplateResponse(request, 'post.html', kwargs)
        return t
    
    
    def post(self, request, *args, **kwargs):
        if request.session.get('account_id', None) is None:
            return HttpResponseRedirect('/account/login')

        article_id = kwargs['id']
        try:
            i = Article.objects.get(id=article_id)
            d = request.POST.dict()
       
            tag = d.get('tag', None)   
            i.tag = tag.split(';')
            i.category = int(d['category'])
            i.head_image = d.get('head_image', None)
            i.title = d['title']
            i.content = d['content'] 
            i.status = 1
            i.save()
        except DoesNotExist:
            pass

        return HttpResponseRedirect('/blog')


class List(TemplateView):

    def get(self, request, *args, **kwargs):
        d = request.GET.dict()
        category = int(d.get('category', 3))
        page_num = int(d.get('page_num', 1))
        if page_num < 1:
            page_num = 1 
        

        try:
            item_num = 10
           
            page_start = (page_num -1 )* item_num
            page_end = page_num * item_num 

            total_num = Article.objects.filter(category=category, status=1).count()  
            
            last_page = max(0, page_num-1)
            total_page = (total_num/item_num)+ 1
            end_page = total_page 
            next_page = min(end_page, page_num+1)


            a_list = list(Article.objects.filter(category=category, status=1).order_by('-create_time'))[page_start:page_end]

            for i in a_list:
                i.content = markdown(i.content)
            para = {'article_list': a_list}
            para.update({'category':category,
                     "page_num": page_num,
                     "last_page": last_page,
                     "next_page": next_page,
                     'end_page': end_page,
                     'total_page': total_page,})

        except DoesNotExist:
            para = {'article_list': None}

        t = TemplateResponse(request, 'list.html', para)
        return t
    
 
class Detail(TemplateView):

    def get(self, request, *args, **kwargs):
        article_id = kwargs['id']
        try:
            a = Article.objects.get(id=article_id)
            a.content = markdown(a.content)

            para = {'article': a}
        except DoesNotExist:
            para = {'article': None}
        t = TemplateResponse(request, 'detail.html', para)
        return t
    
 
class Archive(TemplateView):

    def get(self, request, *args, **kwargs):
        year = int(kwargs['id'])
        d = request.GET.dict()
        page_num = int(d.get('page_num', 1))
        if page_num < 1:
            page_num = 1 
        

        try:
            item_num = 2
           
            page_start = (page_num -1 )* item_num
            page_end = page_num * item_num 

            start = datetime(year, 1, 1)
            end = datetime(year, 12, 31)
            
            total_num = Article.objects(Q(status=1) & Q(create_time__gte=start) & Q(create_time__lte=end)).count()  
            last_page = max(0, page_num-1)
            total_page = (total_num/item_num)+ 1
            end_page = total_page 
            next_page = min(end_page, page_num+1)


            a_list = list(Article.objects(Q(create_time__gte=start)& Q(create_time__lte=end)).order_by('-create_time'))[page_start:page_end]

            for i in a_list:
                i.content = markdown(i.content)
            para = {'article_list': a_list}
            para.update({"page_num": page_num,
                     "last_page": last_page,
                     "next_page": next_page,
                     'end_page': end_page,
                     'total_page': total_page,})

        except DoesNotExist:
            para = {'article_list': None}

        t = TemplateResponse(request, 'list.html', para)
        return t


class Delete(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.session.get('account_id', None) is None:
            return HttpResponseRedirect('/account/login')
        article_id = kwargs['id']
        try:
            a = Article.objects.get(id=article_id)
            a.status = -1
            a.save()

        except DoesNotExist:
            pass
        refer = request.META.get('HTTP_REFERER', None)
        if refer:
            return HttpResponseRedirect(refer)
        else:
            return HttpResponseRedirect('/')

class Admin(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.session.get('account_id', None) is None:
            return HttpResponseRedirect('/account/login')
 
        d = request.GET.dict()
        category = int(d.get('category', 3))
        page_num = int(d.get('page_num', 1))
        if page_num < 1:
            page_num = 1 
        

        try:
            item_num = 10
           
            page_start = (page_num -1 )* item_num
            page_end = page_num * item_num 

            total_num = Article.objects.count()  
            
            last_page = max(0, page_num-1)
            total_page = (total_num/item_num)+ 1
            end_page = total_page 
            next_page = min(end_page, page_num+1)


            a_list = list(Article.objects.order_by('-create_time'))[page_start:page_end]

            for i in a_list:
                i.content = markdown(i.content)
            para = {'article_list': a_list}
            para.update({'category':category,
                     "page_num": page_num,
                     "last_page": last_page,
                     "next_page": next_page,
                     'end_page': end_page,
                     'total_page': total_page,})

        except DoesNotExist:
            para = {'article_list': None}

        t = TemplateResponse(request, 'list.html', para)
        return t
    
 
