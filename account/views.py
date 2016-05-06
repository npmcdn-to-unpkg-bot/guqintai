#coding=utf8
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseForbidden

from mongoengine import DoesNotExist
from models import Account
# Create your views here.


class Login(TemplateView):

    def get(self, request, *args, **kwargs):
        account_id = request.session.get('account_id', None)
        if account_id != None:
            next_url = "/" 
            return HttpResponseRedirect(next_url)
        para = {}
        t = TemplateResponse(request, 'login.html', para)
        return t
    

    def post(self, request, *args, **kwargs):
        d = request.POST.dict()
        username = d['username']
        password = d['password']

        try:
            o = Account.objects.get(username=username) 
            if o.password == password:
                request.session['account_id'] = o.id
                request.session['username'] = username
                next_url = "/" 
                return HttpResponseRedirect(next_url)
            else:
                para = {'error': '密码错误'}
                t = TemplateResponse(request, 'login.html', para)
                
        except DoesNotExist:
            para = {'error': '账号不存在'}
            t = TemplateResponse(request, 'login.html', para)
        return t
    
    
class Logout(TemplateView):

    def get(self, request, *args, **kwargs):
  
        account_id = request.session.pop('account_id', None)
       
        return HttpResponseRedirect('/blog/')
            
        


