from tests.base_test import *
from core.conditions import empty
from core.tools import visit
from tests.pages.todomvc import *


class TestTodoMVC(BaseTest):

    def test_tasks_life_cycle(self):

        visit("http://todomvc.com/examples/troopjs_require/#")

        add("a")

        edit("a", "a edited")

        # complete
        toggle("a edited")
        filter_active()
        tasks.filter(visible).assure(empty)

        # create from active filter
        add("b")
        toggle("b")
        filter_completed()
        assert_visible_tasks("a edited", "b")

        # reopen from completed filter
        toggle("a edited")
        assert_visible_tasks("b")
        filter_active()
        assert_visible_tasks("a edited")
        filter_all()
        assert_tasks("a edited", "b")

        # clear completed
        clear_completed()
        assert_tasks("a edited")

        # complete all
        toggle_all()
        filter_active()
        tasks.filter(visible).assure(empty)

        # reopen all
        toggle_all()
        assert_visible_tasks("a edited")

        add("c")

        # delete by editing to ''
        edit("a edited", "")
        filter_all()
        assert_tasks("c")

        # delete
        delete("c")
        tasks.assure(empty)

