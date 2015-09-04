from selenium.webdriver.common.keys import Keys

from core.conditions import texts, css_class, visible, exact_text
from core.tools import s, ss

tasks = ss("#todo-list>li")

def assert_tasks(*task_texts):
    tasks.assure(texts, *task_texts)


def assert_visible_tasks(*task_texts):
    tasks.filter(visible).assure(texts, *task_texts)


def add(task_name):
    s("#new-todo").send_keys(task_name + Keys.ENTER)


def edit(old_task_name, new_task_name):
    tasks.find(exact_text, old_task_name).s("label").double_click()
    tasks.find(css_class, "editing").s(".edit").set_value(new_task_name).press_enter()


def toggle(task_name):
    tasks.find(exact_text, task_name).s(".toggle").click()


def delete(task_name):
    tasks.find(exact_text, task_name).hover().s(".destroy").click()


def toggle_all():
    s("#toggle-all").click()


def clear_completed():
    s("#clear-completed").click()


def filter_all():
    s("[href='#/']").click()


def filter_active():
    s("[href*='active']").click()


def filter_completed():
    s("[href*='completed']").click()