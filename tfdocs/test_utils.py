from tfdocs.utils import hello_world
import pytest


@pytest.mark.parametrize(
    "case, exp",
    [
        ("world", "hello, world!"),
        ("test", "hello, test!"),
        ("", "hello, world!"),
    ],
)
def test_hello_world(case, exp):
    assert hello_world(case) == exp
