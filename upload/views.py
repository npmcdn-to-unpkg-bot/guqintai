#coding=utf8
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseForbidden
import json
# Create your views here.
import StringIO
import tempfile



#coding=utf-8
import oss2

endpoint = 'http://oss-cn-beijing.aliyuncs.com' # 假设你的Bucket处于杭州区域
auth = oss2.Auth('JP6rg2vUDyHM2cvm', 'w3VIomubT3hORRu661GFDiGPyTpxbO')
bucket = oss2.Bucket(auth, endpoint, 'xtuz-image')


class Index(TemplateView):

    def post(self, request, *args, **kwargs):
        para = {}
        f=request.FILES['file']
        filename = f.name
        ss = StringIO.StringIO()
        for chunk in f.chunks():
            ss.write(chunk)
        ss.seek(0)
        bucket.put_object('guqintai/' + filename, ss)
        return HttpResponse(json.dumps({'name':filename, 'error':'mis'}))
    
 

