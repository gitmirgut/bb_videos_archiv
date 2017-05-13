import os
import os.path

import pytest


# add marker for incremental testing
# http://doc.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


test_dir = os.path.dirname(__file__)


@pytest.fixture
def main_indir():
    return os.path.join(test_dir, 'data', 'in')


@pytest.fixture
def main_outdir():
    out_path = os.path.join(test_dir, 'data', 'out')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    return out_path