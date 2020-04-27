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

        Note: If app provided, an initial fetch() will be issued, as the OpenVidu object is created.

        :param app: Optional Flask application to be bound.
        """
        self.app = app
        if app:
            self.init_app(app)

    @staticmethod
    def init_app(app):
        """
        Initialize the OpenVidu object according to Flask config.

        Note: Calling this function will do an initial fetch() call, as the OpenVidu object is created.

        :param app: Flask application to be bound.
        """
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

    @property
    def connection(self) -> pyopenvidu.OpenVidu:
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
