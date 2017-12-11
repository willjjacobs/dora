import pytest
from dora.__main__ import main


@pytest.mark.parametrize("test_input,expected", [
    pytest.param(
        "dora server",
        0,
        marks=pytest.mark.skip(
            reason="This continues to run and does not return")),
    pytest.param(
        "dora client",
        0,
        marks=pytest.mark.skip(
            reason="This continues to run and does not return")),
    ("dora", 1),
    ("dora hello", 1),
    ("dora three args", 1),
])
def test_main_args(test_input, expected):
    assert main(test_input) == expected
