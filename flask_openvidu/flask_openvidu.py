"""Main module."""
import pyopenvidu
from flask import current_app, _app_ctx_stack


class ClassProperty(property):  # This is an ugly solution, but we want to use class level properties
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class OpenVidu(object):
    """
    This is a static class that provides you an OpenVidu object configured by Flask.
    """

    # Yup, this class does only support a similar pattern to the standard Flask extension's factory pattern
    # This is used so that you do not have to create an instance of this class to cause import problems all around your app
    # If you will ever need the traditional pattern for some reason, feel free to open a pull request

    def __init__(self):
        raise RuntimeError("This is a static class\nUse OpenVidu.connection to access the OpenVidu instance")

    @staticmethod
    def init_app(app):
        app.config.setdefault('OPENVIDU_URL', None)
        app.config.setdefault('OPENVIDU_SECRET', None)

    @staticmethod
    def connect() -> pyopenvidu.OpenVidu:
        if not (current_app.config['OPENVIDU_URL'] and current_app.config['OPENVIDU_SECRET']):
            raise RuntimeError("OPENVIDU_URL and OPENVIDU_SECRET must be configured.")

        return pyopenvidu.OpenVidu(
            current_app.config['OPENVIDU_URL'],
            current_app.config['OPENVIDU_SECRET']
        )

    @ClassProperty
    @classmethod
    def connection(cls) -> pyopenvidu.OpenVidu:
        """
        Get or create the OpenVidu instance belongs to the current Flask application.

        :return: an OpenVidu instance configured according to the Flask configuration.
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'openvidu'):
                ctx.openvidu = cls.connect()
            return ctx.openvidu
