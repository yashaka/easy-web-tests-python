import pytest
from selenium import webdriver
import core.config


@pytest.fixture(scope='class')
def setup(request):
    core.config.browser = webdriver.Firefox()

    def teardown():
        core.config.browser.quit()

    request.addfinalizer(teardown)


@pytest.mark.usefixtures("setup")
class BaseTest(object):
    pass