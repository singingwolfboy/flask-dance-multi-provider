Flask-Dance Example App: Multiple Providers Edition
===================================================

This repository provides an example of how to use `Flask-Dance`_ with
with multiple OAuth providers simultaneously. This allows users to
link multiple services to their account, so that they can log into
the same account in several different ways.
This particular repository uses Google and GitHub as OAuth providers,
and it wires together the following Flask extensions:

* `Flask-Dance`_
* `Flask-SQLAlchemy`_
* `Flask-Login`_
* `Flask-Bcrypt`_
* `Flask-WTF`_

|heroku-deploy|

.. _Flask: http://flask.pocoo.org/docs/
.. _Flask-Dance: http://flask-dance.readthedocs.org/
.. _Flask-SQLAlchemy: http://flask-sqlalchemy.pocoo.org/
.. _Flask-Login: https://flask-login.readthedocs.io
.. _Flask-Bcrypt: https://flask-bcrypt.readthedocs.io
.. _Flask-WTF: https://flask-wtf.readthedocs.io
.. _Heroku: https://www.heroku.com/

.. |heroku-deploy| image:: https://www.herokucdn.com/deploy/button.png
   :target: https://heroku.com/deploy
   :alt: Deploy to Heroku
