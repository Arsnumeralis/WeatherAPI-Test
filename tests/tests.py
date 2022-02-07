from tkinter.tix import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import sys

#data for querying cities
api_key = "9d50450a48809637b4862bdcb125927d"
cities = {
    "london": {
        "name":"London",
        "htmlid":"lnd",
        "apiid":"2643743"
        },
    "paris": {
        "name":"Paris",
        "htmlid":"par",
        "apiid":"2988507"
    },
    "newyork": {
        "name":"New York",
        "htmlid":"nyc",
        "apiid":"5128581"
    },
    "delhi": {
        "name":"Delhi",
        "htmlid":"del",
        "apiid":"2650225"
    },
    "tokyo": {
        "name":"Tokyo",
        "htmlid":"tok",
        "apiid":"2988507"
    }
}

#installs driver automatically - user needs to ensure they have Google Chrome installed before running
s=Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

#having it as a function prevents the window from closing immediately (likely due to garbage collection)
def launcher():
    driver = webdriver.Chrome(service=s, options=options)
    #when running the script, paste the url of the web-app as a command line argument
    driver.get(r"http://127.0.0.1:5000/")
    return driver

#if no error, t01 passed.
driver = launcher()

def test_case_query(city_id):
    selection1 = driver.find_element_by_id("city_select")
    selection1.click()
    time.sleep(1)
    selection2 = driver.find_element_by_id(city_id)
    selection2.click()
    time.sleep(1)
    submission = driver.find_element_by_id("sub")
    return submission.click()

for city in cities:
    test_case_query(cities[city]["htmlid"])



