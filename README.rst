==================
django-cloudmailin
==================

http://cloudmailin.com/

------------
Requirements
------------

* django >= 1.2.0

-------------
Configuration
-------------

settings.py
===========

Add to *INSTALLED_APPS*::

    'cloudmailin'

Usage
=====

MailHandler is a class based view. Since an application may have multiple
email addresses, they have to be registered with their own secret key and
callbacks. The callbacks can be reused if you want the same functionality for
different email addresses.

::

    from cloudmailin.views import MailHandler

    mail_handler = MailHandler()
    mail_handler.register_address(
        address='mysecretemail@cloudmailin.net',
        secret='mysupersecretkey',
        callback=my_callback_function
    )

The callback will receive the HTTP post variables as keyword arguments::

    def my_callback_function(**kwargs):
        # kwargs is a dict of cloudmailin post params
        pass

Then, in urls.py, register a URL pattern to act as the endpoint::

    url(r'^receive/mail/here/$', mail_handler)

