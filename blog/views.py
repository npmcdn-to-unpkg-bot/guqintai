from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseForbidden

from mongoengine import DoesNotExist
from models import Article

from markdown import markdown 

# Create your views here.
class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        para = {}
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

        d = request.POST
        i = Article()
        account_id = request.session['account_id']
        i.account_id = str(account_id)
        i.username = request.session['username']
    
        i.category = int(d['category'])
        i.head_image = d.get('head_image', None)
        i.title = d['title']
        i.content = d['content'] 
        i.save()

        return HttpResponseRedirect('/blog')

class List(TemplateView):

    def get(self, request, *args, **kwargs):
        d = request.GET.dict()
        category = int(d.get('category', 1))
        try:
            a_list = list(Article.objects.filter(category=category).order_by('-create_time'))
            print type(a_list)
            for i in a_list:
                i.content = markdown(i.content)
            para = {'article_list': a_list}
        except DoesNotExist:
            para = {'article_list': None}
        t = TemplateResponse(request, 'list.html', para)
        return t
    
 
    
