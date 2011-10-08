from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from cloudmailin.views import generate_signature as real_generate_signature
import hashlib
import os

# generic utilities

PWD = os.path.abspath(os.path.dirname(__file__))

def load_email(filename):
    mail_dir = os.path.join(PWD, 'test', 'mail', filename)
    f = open(mail_dir)
    content = f.read()
    f.close()
    return content

# cloudmailin tests

SECRET = 'notactuallysecret'

BASE_PARAMS = {
    'message': load_email('message.txt'),
    'plain': load_email('plain.txt'),
    'html': load_email('html.txt'),
    'to': '<animaginaryperson@example.com>',
    'disposable': '',
    'from': 'anotherperson@example.com',
    'subject': 'Hi, this is my email',
}

def generate_signature(params, secret):
    sig = "".join(params[k] for k in sorted(params.keys()))
    sig = hashlib.md5(sig + secret).hexdigest()
    return sig

class CloudMailinTestCase(TestCase):

    urls = 'cloudmailin.test.urls'

    def test_get(self):
        resp = self.client.get('/mail/')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.content, "recipient address is not found")

    def test_post(self):
        params = BASE_PARAMS.copy()
        params['signature'] = generate_signature(params, SECRET)
        resp = self.client.post('/mail/', params)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.content, "")

    def test_post_disposable(self):
        params = BASE_PARAMS.copy()
        params['to'] = '<animaginaryperson+disposable@example.com>'
        params['signature'] = generate_signature(params, SECRET)
        resp = self.client.post('/mail/', params)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.content, "")

    def test_post_noparams(self):
        resp = self.client.post('/mail/')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.content, "recipient address is not found")

    def test_post_invalidsig(self):
        params = BASE_PARAMS.copy()
        params['signature'] = generate_signature(params, SECRET) + "!"
        resp = self.client.post('/mail/', params)
        self.assertEquals(resp.status_code, 403)
        self.assertEquals(resp.content, "invalid message signature")

    def test_post_invalidrecipient(self):
        params = BASE_PARAMS.copy()
        params['to'] = '<aninvalidemailaddress@example.com>'
        params['signature'] = generate_signature(params, SECRET)
        resp = self.client.post('/mail/', params)
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.content, "recipient address is not found")

    def test_post_500(self):
        params = BASE_PARAMS.copy()
        params['to'] = '<500@example.com>'
        params['signature'] = generate_signature(params, SECRET)
        resp = self.client.post('/mail/', params)
        self.assertEquals(resp.status_code, 500)
        self.assertEquals(resp.content, "this is a made up exception")

    def test_signature(self):
        self.assertEquals(
            real_generate_signature(BASE_PARAMS, SECRET),
            generate_signature(BASE_PARAMS, SECRET),
        )

