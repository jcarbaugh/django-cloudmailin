from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
import hashlib

class MailHandler(object):
    
    csrf_exempt = True
    
    def __init__(self, *args, **kwargs):
        super(MailHandler, self).__init__(*args, **kwargs)
        self._addresses = {}
    
    def __call__(self, request, *args, **kwargs):
        
        to = request.POST.get('to', None)
        addr = self._addresses.get(to, None)
        
        if addr is None:
            return HttpResponseNotFound("recipient address is not found", mimetype="text/plain")
        
        if not self.is_valid_signature(request.POST, addr['secret']):
            return HttpResponseForbidden("invalid message signature", mimetype="text/plain")
        
        try:
            addr['callback'](**request.POST)
        except Exception, e:
            return HttpResponseServerError(e.message)
        
        resp = HttpResponse("")
        resp.csrf_exempt = True
        return resp
    
    def is_valid_signature(self, params, secret):
        
        if 'signature' in params:
        
            sig = "".join(params[k] for k in sorted(params.keys()) if k != "signature")
            sig = hashlib.md5(sig + secret).hexdigest()
        
            return params['signature'] == sig
    
    def register_address(self, address, secret, callback):
        self._addresses["<%s>" % address] = {
            'secret': secret,
            'callback': callback,
        }
        return True
    
    def unregister_address(self, address):
        if address in self._addresses:
            del self._addresses[address]
            return True
        return False