"""Main module."""
import pyopenvidu
from flask import current_app, _app_ctx_stack


class OpenVidu(object):
    """
    This class provides a OpenVidu instance instantiated by the values configured.
    Multiple Flask applications are supported natively.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('OPENVIDU_URL', None)
        app.config.setdefault('OPENVIDU_SECRET', None)

    def connect(self):
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
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'openvidu'):
                ctx.openvidu = self.connect()
            return ctx.openvidu
