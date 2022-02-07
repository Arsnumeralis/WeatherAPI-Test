from cgi import test
from operator import contains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

if __name__ == "__main__":
    #data for querying cities
    api_key = "9d50450a48809637b4862bdcb125927d"
    cities = {
        "London": {
            "name":"London",
            "html_id":"lnd",
            "api_id":"2643743"
            },
        "Paris": {
            "name":"Paris",
            "html_id":"par",
            "api_id":"2988507"
        },
        "New York": {
            "name":"New York",
            "html_id":"nyc",
            "api_id":"5128581"
        },
        "Delhi": {
            #name for Delhi in Hindi
            "name":"दिल्ल",
            "html_id":"del",
            "api_id":"2650225"
        },
        "Tokyo": {
            #name for Tokyo in Japanese
            "name":"東京都",
            "html_id":"tok",
            "api_id":"1850147"
        }
    }

    #installs driver automatically - user needs to ensure they have Google Chrome installed before running
    s=Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    tested = ["Tests completed:"]
    #having it as a function prevents the window from closing immediately (likely due to garbage collection)
    def launcher(url):
        driver = webdriver.Chrome(service=s, options=options)
        #when running the script, paste the url of the web-app as a command line argument
        driver.get(url)
        return driver

    #function to close the driver
    def close_down(driver):
        driver.close()

    #if no error, t01 passed.
    driver = launcher(r"http://127.0.0.1:5000/")
    if driver:
        print("T1 PASSED")
        tested.append("T1 PASSED")
    else:
        print("T1 FAILED")
        tested.append("T01 FAILED")
    
    #funtion to make a weather query on the webpage
    def test_case_query(city_id):
        selection1 = driver.find_element_by_id("city_select")
        selection1.click()
        time.sleep(1)
        selection2 = driver.find_element_by_id(city_id)
        selection2.click()
        time.sleep(1)
        submission = driver.find_element_by_id("sub")
        return submission.click()

    #function to collect the data from webpage
    def test_case_data_collection(display_data = None):
        if display_data == None:
            display_data = []
        city_name = driver.find_element_by_tag_name("h2")
        display_data.append(city_name.text)
        table = driver.find_element_by_xpath('/html/body/table/tbody')
        driver.execute_script("arguments[0].click();", table)
        time.sleep(2)
        display_data.append([item.text for item in table.find_elements_by_xpath("/html/body/table/tbody/tr")])
        return display_data

    #function to collect the data from api
    def api_data_collection(api_data = None):
        if api_data == None:
            api_data = []
        city_name = api_driver.find_element_by_xpath("/html/body/div[1]")
        api_data.append(city_name.text)
        temp_value = api_driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]")
        #ensuring the temp value doesn't have °C
        api_data.append(temp_value.text[-7:-3])
        humidity_value = api_driver.find_element_by_xpath("/html/body/div[2]/div[3]")
        api_data.append(humidity_value.text)
        return api_data


#tests T2-T6
    try:
        for idx, city in enumerate(cities):
            display_data = None
            test_case_query(cities[city]["html_id"])
            time.sleep(1)
            display_data = (test_case_data_collection())
            # print(display_data)
            #checks if temperature values are in °C
            if "°C" not in display_data[1][0] or "°C" not in display_data[1][3] or "°C" not in display_data[1][4]:
                print(display_data[1][0], display_data[1][3], display_data[1][4])
                print(f"T{idx + 2} FAILED - temperature not displayed in °C")
                tested.append(f"T{idx + 2} FAILED - temperature not displayed in °C")
                continue
            #checks if humidity values are in %
            if r"%" not in display_data[1][1]:
                print(f"T{idx + 2} FAILED - humidity not displayed in %")
                tested.append(f"T{idx + 2} FAILED - humidity not displayed in %")
                continue
            #checks if names are correct for non-English name cities
            if idx == 3:
                if display_data[0] != cities["Delhi"]["name"]:
                    print(f"T{idx + 2} FAILED - city name incorrect")
                    tested.append(f"T{idx + 2} FAILED - city name incorrect")
                    continue
            if idx == 4:
                if display_data[0] != cities["Tokyo"]["name"]:
                    print(f"T{idx + 2} FAILED - city name incorrect")
                    tested.append(f"T{idx + 2} FAILED - city name incorrect")
                    continue

            print(f"T{idx + 2} PASSED")
            tested.append(f"T{idx + 2} PASSED")


    #tests T7-T11
        for idx, city in enumerate(cities):
            web_data = None
            api_data = None
            city_id = cities[city]["api_id"]
            #accessing the api in html format
            api_url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&mode=html"
            api_driver = launcher(api_url)
            test_case_query(cities[city]["html_id"])
            #scraping webpage data
            web_data = test_case_data_collection()
            #scraping api data
            api_data = api_data_collection()
            #comparing city name, temperature and humidity between webpage and api
            if city != api_data[0]:
                print(f"T{idx + 7} FAILED - city name incorrect")
                tested.append(f"T{idx + 7} FAILED - city name incorrect")
                close_down(api_driver)
                continue
            if abs(float(api_data[1]) - float(web_data[1][0][-6:-3])) > 1:
                print(f"T{idx + 7} FAILED - temperature discrepancy too high")
                tested.append(f"T{idx + 7} FAILED - temperature discrepancy too high")
                close_down(api_driver)
                continue
            #ensuring humidity value doesn't have % at the end
            if abs(int(api_data[2][-3:-2]) - int(web_data[1][1][-3:-2])) > 1:
                print(f"T{idx + 7} FAILED - humidity discrepancy too high")
                tested.append(f"T{idx + 7} FAILED - humidity discrepancy too high")
                close_down(api_driver)
                continue
            print(f"T{idx + 7} PASSED")
            tested.append(f"T{idx + 7} PASSED")
            close_down(api_driver)
            time.sleep(1)
        close_down(driver)
        #separating log from list of completed tests.
        print("""
        \n
        \n
        \n
        """)
        print(*tested, sep = "\n")
    except:
        print("software error prevented from testing being fully complete")
        print(*tested, sep = "\n")

