import flask
import pytest
import pyopenvidu
from flask_openvidu import OpenVidu
from requests.auth import HTTPBasicAuth


@pytest.fixture
def flask_app():
    yield flask.Flask(__name__)


def test_returns_openvidu_instance_autofetch(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    OpenVidu.init_app(flask_app)

    pyopenvidu.OpenVidu.fetch.assert_called_once()

    with flask_app.app_context():
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)

    assert pyopenvidu.OpenVidu.fetch.call_count == 2

    with flask_app.app_context():
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)

    assert pyopenvidu.OpenVidu.fetch.call_count == 3



def test_returns_openvidu_instance_no_autofetch(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    flask_app.config["OPENVIDU_AUTO_FETCH"] = False
    OpenVidu.init_app(flask_app)

    pyopenvidu.OpenVidu.fetch.assert_called_once()

    with flask_app.app_context():
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)

    pyopenvidu.OpenVidu.fetch.assert_called_once()

    with flask_app.app_context():
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)
        assert isinstance(OpenVidu.connection, pyopenvidu.OpenVidu)

    pyopenvidu.OpenVidu.fetch.assert_called_once()


def test_config_match(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    OpenVidu.init_app(flask_app)

    with flask_app.app_context():
        assert OpenVidu.connection._session.auth == HTTPBasicAuth("OPENVIDUAPP", "test")
        assert OpenVidu.connection._session.base_url == "test"


def test_raise_error_on_missing_config(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    with pytest.raises(RuntimeError):
        OpenVidu.init_app(flask_app)
