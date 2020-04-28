import flask
import pytest
import pyopenvidu
from flask_openvidu import OpenVidu
from requests.auth import HTTPBasicAuth


@pytest.fixture
def flask_app():
    yield flask.Flask(__name__)


def test_returns_openvidu_instance(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    ov = OpenVidu(flask_app)

    assert pyopenvidu.OpenVidu.fetch.call_count == 0

    with flask_app.app_context():
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)

    assert pyopenvidu.OpenVidu.fetch.call_count == 1

    with flask_app.app_context():
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)

    assert pyopenvidu.OpenVidu.fetch.call_count == 2


def test_config_match(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    ov = OpenVidu(flask_app)

    with flask_app.app_context():
        assert ov.connection._session.auth == HTTPBasicAuth("OPENVIDUAPP", "test")
        assert ov.connection._session.base_url == "test"


def test_raise_error_on_missing_config(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)
    ov = OpenVidu(flask_app)

    with pytest.raises(RuntimeError):
        with flask_app.app_context():
            a = ov.connection


def test_init_later(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    ov = OpenVidu()
    assert pyopenvidu.OpenVidu.fetch.call_count == 0

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"

    ov.init_app(flask_app)

    assert pyopenvidu.OpenVidu.fetch.call_count == 0

    with flask_app.app_context(): # should not throw exception
        a = ov.connection

