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
    ov = OpenVidu(flask_app)

    pyopenvidu.OpenVidu.fetch.assert_called_once()

    with flask_app.app_context():
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)

    assert pyopenvidu.OpenVidu.fetch.call_count == 2

    with flask_app.app_context():
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)

    assert pyopenvidu.OpenVidu.fetch.call_count == 3


def test_returns_openvidu_instance_no_autofetch(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"
    flask_app.config["OPENVIDU_AUTO_FETCH"] = False
    ov = OpenVidu(flask_app)

    pyopenvidu.OpenVidu.fetch.assert_called_once()

    with flask_app.app_context():
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)

    pyopenvidu.OpenVidu.fetch.assert_called_once()

    with flask_app.app_context():
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)
        assert isinstance(ov.connection, pyopenvidu.OpenVidu)

    pyopenvidu.OpenVidu.fetch.assert_called_once()


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

    with pytest.raises(RuntimeError):
        ov = OpenVidu(flask_app)


def test_init_later(mocker, flask_app):
    mocker.patch.object(pyopenvidu.OpenVidu, "fetch", autospec=True)

    ov = OpenVidu()
    assert pyopenvidu.OpenVidu.fetch.call_count == 0

    flask_app.config["OPENVIDU_URL"] = "test"
    flask_app.config["OPENVIDU_SECRET"] = "test"

    ov.init_app(flask_app)

    pyopenvidu.OpenVidu.fetch.assert_called_once()
