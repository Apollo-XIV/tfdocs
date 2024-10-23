import pytest
import logging
from unittest.mock import patch
from tfdocs.db.test_handler import MockDb
from tfdocs.models.blocks.provider import Provider

log = logging.getLogger()


class MockProvider(Provider):
    _db = MockDb()


@pytest.mark.parametrize(
    "case, exp",
    [
        ("registry.terraform.io/hashicorp/archive", "3c09cf2d1f63e6886c1ff5bd2a9fa49d"),
        ("registry.terraform.io/hashicorp/null", "b68b2e47df542636676cf4c527b75aa0"),
        ("registry.terraform.io/hashicorp/time", "85c7eb5ef45cc843ad01660e75695dce"),
    ],
)
def test_from_name(case, exp):
    subject = MockProvider.from_name(case)
    assert subject.id == exp


def test_list_all():
    exp = {
        "registry.terraform.io/hashicorp/archive",
        "registry.terraform.io/hashicorp/null",
        "registry.terraform.io/hashicorp/time",
    }
    subjects = MockProvider.list_all()
    assert {s.name for s in subjects} == exp
