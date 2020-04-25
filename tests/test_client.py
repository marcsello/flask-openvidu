import flask
import pytest
import pyopenvidu
from flask_openvidu import OpenVidu
from requests.auth import HTTPBasicAuth


@pytest.fixture
def flask_app():
    yield flask.Flask(__name__)


def test_returns_openvidu_instance(mocker, flask_app):
    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    OpenVidu.init_app(flask_app)
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    with flask_app.app_context():
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)

    pyopenvidu.OpenVidu.fetch.assert_called_once()


def test_config_match(mocker, flask_app):
    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    OpenVidu.init_app(flask_app)
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    with flask_app.app_context():
        assert OpenVidu.connection._session.auth == HTTPBasicAuth("OPENVIDUAPP", "test")
        assert OpenVidu.connection._session.base_url == "test"


def test_raise_error_on_missing_config(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)
    OpenVidu.init_app(flask_app)

    with flask_app.app_context():
        with pytest.raises(RuntimeError):
            OpenVidu.connection
