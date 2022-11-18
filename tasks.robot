*** Settings ***
Documentation     Template robot main suite.
Library           RPA.Browser.Selenium
Library           Bot.py
Library           GenericProcess.py
Task Teardown     Teardown

*** Tasks ***
RPA Task
    Setup
    Start