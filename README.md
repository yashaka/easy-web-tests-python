# Easy Selenium tests in Python demo

This is a notes project for demo on how to write easy selenium tests in Python (of [Selenide](http://selenide.org) style). 
Demo was shown in Cogniance, 03.09.2015

This project was inspired also by [Selene](https://github.com/yashaka/selene/) which is an attempt to implement [Selenide](http://selenide.org) + [htmlelements](https://github.com/yandex-qatools/htmlelements) in Python.

It differs from Selene
* by using Selenium explicit waits under the hood (Selene implements its own explicit waits)
* by using Selenium style of expected conditions to be used with explicit waits
* only manual webdriver creation (Selene creates and closes driver automatically)
* no Element Widgets support (like in htmlelements), though can be added soon rather easy
* no screenshots in error messages (though can be added very easy)
This simplified the implementation a lot, but have some drawbacks becuase selenium's expected conditions are not handy in use, limiting the possibilities.

## To start writing tests
* install python 
* install selenium and pytest
* install IDE (e.g. PyCharm CE)
* clone or download the repo
* open in IDE
* write your own tests under the tests folder
* run them from command line via py.test command executed from the project folder

(google on installation guides for all tools)

## TODOs
* add more docs and howtos on insallation and usage, etc.
* add "one test per feature" style tests with before/after hooks for clearing data
* tag smoke tests

## Extra notes

### About PageObjects

This version of the project contains all "helpers to work with page's elements" in a separate PageObject implemented
as a simple Python module. 
On the lesson we used all helpers just inside the python file with test itself: http://pastebin.com/VmeQ6C3B

Just remember that PageObject as a template is needed:

* NOT ONLY to gather (encapsulate) things of one context ("elements and action/helper/step-methods to work with a specific page")

* BUT mainly for code reuse

i.e. if so far you used all these helpers only in one file, there is no actual need to move them into separate one;)

Some companies do not use PageObject pattern because structure their tests in the way that these helpers are used only in one file.
Though this is of course not a general recommended principle. Everything should be applied in context.
Sometimes it will work, sometimes not.