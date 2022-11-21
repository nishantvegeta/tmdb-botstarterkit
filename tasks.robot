*** Settings ***
Documentation     Template robot main suite.
Library           RPA.Browser.Selenium
Library           Bot.py
Task Teardown     Teardown

*** Tasks ***
RPA Task
    Setup Platform Components
    Start