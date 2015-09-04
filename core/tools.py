from core import config
from core.elements import SmartElement, SmartElementsCollection


def visit(url):
    config.browser.get(url)


def s(css_selector):
    return SmartElement(css_selector)


def ss(css_selector):
    return SmartElementsCollection(css_selector)

