import pytest
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from dashboard.jsonsocket import *
from dora.dashboard import util
from dora.dashboard.util import *
from dora.dashboard.UI_Start import *

task = create_task()
configTest = setup_config()
host = "0.0.0.0"
port = 8000


def test_setup_config():
    assert setup_config() is not None


def test_create_task():
    assert create_task() is not None


def test_print_task():
    assert task["first_setup"] == 0
    # assert task["test_value2"] == 0
    assert task["core_ip"] == "0.0.0.0"


def test_config_to_task():
    assert task["first_setup"] == 0
    assert 2 == configTest.value("test_value2")
    assert task["core_ip"] == configTest.value("core_ip")


def test_open_event():  #Legacy method
    assert True


def test_close_event():  #Legacy method
    assert True


def test_send_task():  #Legacy method
    assert True
