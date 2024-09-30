from tfdocs.utils import hello_world, hash_path, clamp_string, flatten
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


@pytest.mark.parametrize(
    "input_string, max_length, expected_output",
    [
        # Test cases where string length is less than or equal to max_length
        ("hello", 10, "hello"),  # No clamping needed
        ("world", 5, "world"),  # Exactly the max length
        # Test cases where string length is greater than max_length
        ("hello world", 5, "he..."),  # Clamp and add ellipsis
        ("truncate me", 10, "truncat..."),  # Clamp and add ellipsis
        # Test case where max_length is less than 3
        ("small", 2, "..."),  # Can't show part of the string, just ellipsis
        # Test case with an empty string
        ("", 5, ""),  # Should return the empty string
    ],
)
def test_clamp_string(input_string, max_length, expected_output):
    assert clamp_string(input_string, max_length) == expected_output


def test_hasher():
    """
    This test ensures the hasher stays functional
    """
    exps = ["8dd066a9072cfaca57bcedd7f233432f", "b3983e305a7a18c356122f7df1496f14"]
    inps = [
        "test_value",
        "another_test_value",
    ]

    for inp, exp in zip(inps, exps):
        inp = hash_path(inp)
        assert inp == exp
