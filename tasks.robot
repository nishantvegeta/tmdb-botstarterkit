*** Settings ***
Documentation     Template robot main suite.
Library           RPA.Browser.Selenium
Library           DefaultProcess.py
Library           Bot.py
Task Teardown     Teardown

*** Tasks ***
RPA Task
    SetUp Platform Components
    Start