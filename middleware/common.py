#coding=utf8
import json
import traceback
class ExceptionMiddleware(object):
    def __init__(self):
        #self.log = logging.getLogger('api')
        pass

    def process_exception(self, request, exception): 
        ex = traceback.format_exc()
        print ex
        #self.log.info('code:500 ' + request.path + '\r\n' + ex)
        return HttpResponse(json.dumps({'info': str(exception), 'code':500, 'ret':None}))  
