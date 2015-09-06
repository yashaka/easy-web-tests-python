from operator import contains, eq
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from core import config

# todo: refactor conditions to accept element.finder, not element - to make implementation of conditions more secure


# this is an example of raw condition implemented from scratch
class example_condition_contain_text(object):
    def __init__(self, element, expected_text):
        self.element = element
        self.expected_text = expected_text
        self.actual_text = None

    def __call__(self, driver):
        try:
            self.actual_text = self.element.finder().text
            return self.expected_text in self.actual_text
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def __str__(self):
        return """ failed while
            waiting %s seconds
            for element found by: %s
            to contain text: %s
            while actual text: %s
        """ % (config.timeout,
               self.element,
               self.expected_text,
               self.actual_text)


class Condition(object):

    def __call__(self, driver):
        self.driver = driver
        try:
            return self.apply()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def __str__(self):
        try:
            return """
            failed while waiting %s seconds
            for %s found by: %s
            to assert %s%s%s
        """ % (config.timeout,
               self.identity(),
               self.entity(),
               self.__class__.__name__,
               """:
            expected: """ + str(self.expected()) if self.expected() else "",
               """
              actual: """ + str(self.actual()) if self.actual() else "")
        except Exception as e:
            return "\n type: %s \n msg: %s \n" % (type(e), e)

    def identity(self):
        return "element"

    def entity(self):
        return self.element

    def expected(self):
        return None

    def actual(self):
        return None

    def apply(self):
        return False


class CollectionCondition(Condition):

    def identity(self):
        return "elements"

    def entity(self):
        return self.elements


class text(Condition):
    def __init__(self, element, expected_text):
        self.element = element
        self.expected_text = expected_text
        self.actual_text = None

    def compare_fn(self):
        return contains

    def apply(self):
        self.actual_text = self.element.finder().text
        # return self.expected_text in self.actual_text
        return self.compare_fn()(self.actual_text, self.expected_text)

    def expected(self):
        return self.expected_text

    def actual(self):
        return self.actual_text


class exact_text(text):
    def compare_fn(self):
        return eq


class visible(Condition):
    def __init__(self, element):
        self.element = element

    def apply(self):
        return self.element.finder().is_displayed()


class css_class(Condition):

    def __init__(self, element, class_attribute_value):
        self.element = element
        self.expected_containable_class = class_attribute_value
        self.actual_class = None

    def apply(self):
        self.actual_class = self.element.get_attribute("class")
        return self.expected_containable_class in self.actual_class

    def expected(self):
        return self.expected_containable_class

    def actual(self):
        return self.actual()


#########################
# COLLECTION CONDITIONS #
#########################


class texts(CollectionCondition):

    def __init__(self, elements, *expected_texts):
        self.elements = elements
        self.expected_texts = expected_texts
        self.actual_texts = None

    def compare_fn(self):
        return contains

    def apply(self):
        self.actual_texts = [item.text for item in self.elements]
        return len(self.elements) == len(self.expected_texts) and \
            all(map(self.compare_fn(), self.actual_texts, self.expected_texts))

    def expected(self):
        return self.expected_texts

    def actual(self):
        return self.actual_texts


class exact_texts(texts):

    def compare_fn(self):
        return eq

class size(CollectionCondition):

    def __init__(self, elements, expected_size):
        self.elements = elements
        self.expected_size = expected_size
        self.actual_size = None

    def apply(self):
        self.actual_size = len(self.elements)
        return self.actual_size == self.expected_size

    def expected(self):
        return self.expected_size

    def actual(self):
        return self.actual_size


def empty(self):
    return size(self, 0)


class size_at_least(CollectionCondition):

    def __init__(self, elements, minimum_size):
        self.elements = elements
        self.minimum_size = minimum_size
        self.actual_size = None

    def apply(self):
        self.actual_size = len(self.elements)
        return self.actual_size >= self.minimum_size

    def expected(self):
        return self.minimum_size

    def actual(self):
        return self.actual_size
