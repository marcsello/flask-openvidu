=====
Usage
=====

To use Flask-OpenVidu in a project, you have to import it to your Flask project::

    from flask_openvidu import OpenVidu


Configuration is handled by Flask's configuration solution. See configuration_ for more details::

    app = Flask(__name__)
    app.config["OPENVIDU_URL"] = "https://example.com:4443/"
    app.config["OPENVIDU_SECRET"] = "your_secret"

.. _configuration: configuration

In order to use this object when handling requests, you have to bind it to the application like this::


    openvidu = OpenVidu(app)

The so called factory pattern is supported as well::

    openvidu = OpenVidu()

    openvidu.init_app(app)

After everything is initialized properly, you can access to a PyOpenVidu_ object::


    @app.route('/sessions')
    def sessions():
        text = ""
        for session in openvidu.connection.sessions:
            text += session.id + "\n"

        return text

.. _PyOpenVidu: https://pypi.org/project/pyopenvidu/


Currently a new OpenVidu object is created for every request which is valid in that request context.
