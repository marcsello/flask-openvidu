"""Main module."""
import pyopenvidu
from flask import current_app, _app_ctx_stack


class OpenVidu(object):
    """
    This class provides an OpenVidu object configured by Flask.
    """

    def __init__(self, app=None):
        """
        Initialize the OpenVidu object according to Flask config.
        Factory pattern is supported as well. See `init_app()`.

        Note: If app provided, an initial fetch() will be issued, as the OpenVidu object is created.

        :param app: Optional Flask application to be bound.
        """
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the OpenVidu object according to Flask config.

        Note: Calling this function will do an initial fetch() call, as the OpenVidu object is created.

        :param app: Flask application to be bound.
        """
        app.config.setdefault('OPENVIDU_URL', None)
        app.config.setdefault('OPENVIDU_SECRET', None)

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['openvidu'] = self

    def connect(self) -> pyopenvidu.OpenVidu:
        """
        Creates a new openvidu session instance that belongs to the current Flask application.

        :return: an OpenVidu instance configured according to the Flask configuration.
        """

        if not (current_app.config['OPENVIDU_URL'] and current_app.config['OPENVIDU_SECRET']):
            raise RuntimeError("OPENVIDU_URL and OPENVIDU_SECRET must be configured.")

        return pyopenvidu.OpenVidu(
            current_app.config['OPENVIDU_URL'],
            current_app.config['OPENVIDU_SECRET']
        )

    @property
    def connection(self) -> pyopenvidu.OpenVidu:
        """
        Get or create the OpenVidu instance belongs to the current Flask application.

        Because of constructing a new object for every request, fetch() will be automatically called
        at the first time accessing to it in the request context. This means only
        a single fetch() call during the handle of each request.

        :return: an OpenVidu instance configured according to the Flask configuration.
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'openvidu'):  # first time called during this request
                ctx.openvidu = self.connect()

            return ctx.openvidu
