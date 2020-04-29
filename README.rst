==============
Flask-OpenVidu
==============


.. image:: https://img.shields.io/pypi/v/flask-openvidu.svg
        :target: https://pypi.python.org/pypi/flask-openvidu

.. image:: https://img.shields.io/travis/marcsello/flask-openvidu.svg
        :target: https://travis-ci.com/marcsello/flask-openvidu

.. image:: https://readthedocs.org/projects/flask-openvidu/badge/?version=latest
        :target: https://flask-openvidu.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/2e8c279f75694c92892cb732b574e09c
        :target: https://www.codacy.com/manual/marcsello/flask-openvidu?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=marcsello/flask-openvidu&amp;utm_campaign=Badge_Grade


Adds OpenVidu_ support to your Flask application through PyOpenVidu_.

.. _OpenVidu: https://openvidu.io/
.. _PyOpenVidu: https://pypi.org/project/pyopenvidu/

* Free software: MIT license
* Documentation: https://flask-openvidu.readthedocs.io.

Simple example
--------------

A basic Flask app that lists the currently active sessions on the server::

    from flask import Flask
    from flask_openvidu import OpenVidu

    app = Flask(__name__)

    app.config["OPENVIDU_URL"] = "https://example.com:4443/"
    app.config["OPENVIDU_SECRET"] = "your_secret"

    ov = OpenVidu(app)

    @app.route('/sessions')
    def sessions():
        text = ""
        for session in ov.connection.sessions:
            text += session.id + "\n"

        return text


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
