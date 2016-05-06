from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseForbidden

from mongoengine import DoesNotExist
# Create your views here.


class Login(TemplateView):

    def get(self, request, *args, **kwargs):
        account_id = request.session.get('account_id', None)
        if account_id != None:
            next_url = "%s/?&au" %(callback,obj.sso_token, obj.account_id) 
            return HttpResponseRedirect(next_url)

        t = TemplateResponse(request, 'login.html', para)
        return t

