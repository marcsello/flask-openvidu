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
        app.config.setdefault('OPENVIDU_AUTO_FETCH', True)

        if not (app.config['OPENVIDU_URL'] and app.config['OPENVIDU_SECRET']):
            raise RuntimeError("OPENVIDU_URL and OPENVIDU_SECRET must be configured.")

        app.extensions = getattr(app, 'extensions', {})

        # This solution relies on OpenVidu class' internal locking for thread safety
        app.extensions['openvidu'] = pyopenvidu.OpenVidu(
            app.config['OPENVIDU_URL'],
            app.config['OPENVIDU_SECRET']
        )

    @ClassProperty
    @classmethod
    def connection(cls) -> pyopenvidu.OpenVidu:
        """
        Get or create the OpenVidu instance belongs to the current Flask application.

        If OPENVIDU_AUTO_FETCH is configured as True (this is the default), than fetch() will be called
        on the OpenVidu object before returning it at the first time accessing to it. This means only
        a single fetch() call during the handle of each request.

        :return: an OpenVidu instance configured according to the Flask configuration.
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'openvidu'):  # first time called during this request
                ctx.openvidu = current_app.extensions['openvidu']

                if current_app.config['OPENVIDU_AUTO_FETCH']:
                    ctx.openvidu.fetch()

            return ctx.openvidu
