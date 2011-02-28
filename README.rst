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

Make sure the *CLOUDMAILIN_SECRET* setting is the correct secret key::

    CLOUDMAILIN_SECRET = 'whatever-your-key-is'
