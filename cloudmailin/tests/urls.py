from django.conf.urls.defaults import *
from cloudmailin.views import MailHandler

def mail_stub(**kwargs):
    pass

def mail_500(**kwargs):
    raise Exception('this is a made up exception')

mail_handler = MailHandler()
mail_handler.register_address(
    address='animaginaryperson@example.com',
    secret='notactuallysecret',
    callback=mail_stub
)
mail_handler.register_address(
    address='500@example.com',
    secret='notactuallysecret',
    callback=mail_500
)

urlpatterns = patterns('',
    url(r'^mail/$', mail_handler),
)