from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait

from conditions import *
from core import config


def actions():
    return ActionChains(config.browser)


class WaitingFinder(object):

    def __init__(self):
        self.locator = None
        self.default_conditions = {}

    def finder(self):
        pass

    def __getattr__(self, item):
        for condition_class, condition_args in self.default_conditions.items():
            self.assure(condition_class, *condition_args)
        return getattr(self.finder(), item)

    def assure(self, condition_class, *condition_args):
        condition = condition_class(self, *condition_args)
        WebDriverWait(config.browser, config.timeout).until(condition, condition)
        return self

    def __str__(self):
        return self.locator


class RootSElement(object):
    def __getattr__(self, item):
        return getattr(config.browser, item)


class SmartElement(WaitingFinder):
    def __init__(self, css_selector, context=RootSElement()):
        self.locator = css_selector
        self.context = context
        self.default_conditions = {visible: []}

    def finder(self):
        return self.context.find_element_by_css_selector(self.locator)

    # def __getattr__(self, item):
    #     self.assure(visible)
    #     return getattr(self.finder(), item)

    def within(self, context):
        self.context = context
        return self

    def s(self, css_locator):
        return SmartElement(css_locator, self)

    def ss(self, css_locator):
        return SmartElementsCollection(css_locator, self)

    def double_click(self):
        actions().double_click(self).perform()
        return self

    def set_value(self, new_text_value):
        self.clear()
        self.send_keys(new_text_value)
        return self

    def press_enter(self):
        self.send_keys(Keys.ENTER)
        return self

    def hover(self):
        actions().move_to_element(self).perform()
        return self


class SmartElementWrapper(SmartElement):
    def __init__(self, smart_element, locator=None):
        self._wrapped_element = smart_element
        super(SmartElementWrapper, self).__init__(locator or smart_element.locator)

    def finder(self):
        return self._wrapped_element


class SmartElementsCollection(WaitingFinder):
    def __init__(self, css_selector, context=RootSElement(), wrapper_class=SmartElementWrapper):
        self.locator = css_selector
        self.context = context
        self._wrapper_class = wrapper_class
        self.default_conditions = []

    def finder(self):
        return [self._wrapper_class(webelement, '%s[%s]' % (self.locator, index))
                for index, webelement in enumerate(self.context.find_elements_by_css_selector(self.locator))]

    def filter(self, condition_class, *condition_args):
        filtered_elements = [selement for selement in self.finder()
                             if condition_class(selement, *condition_args)(config.browser)]
        return SmartElementsCollectionWrapper(filtered_elements, self.locator + "[filtered by ...]") # todo: refactor to be verbose

    def find(self, condition_class, *condition_args):
        return self.filter(condition_class, *condition_args)[0]

    # def __getattr__(self, item):
    #     return getattr(self.finder(), item)

    def __getitem__(self, item):
        self.assure(size_at_least, item + 1)
        return self.finder().__getitem__(item)

    def __len__(self):
        return self.finder().__len__()

    def __iter__(self):
        return self.finder().__iter__()


class SmartElementsCollectionWrapper(SmartElementsCollection):
    def __init__(self, smart_elements_list, locator):
        self.wrapped_elements_list = smart_elements_list
        super(SmartElementsCollectionWrapper, self).__init__(locator)

    def finder(self):
        return self.wrapped_elements_list