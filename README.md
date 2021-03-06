# WeatherAPI-Test
Weather API test for Twenty7Tec Junior Automation QA Tester application

## Setup:

1. Ensure Python and Google Chrome is installed your machine.
2. Clone this repository onto the machine.
3. I recommend using a virtual environment when running the app and tests.
4. Type "pip install -r requirements.txt" into the command line when you are located in the repository's main directory.
5. To run the app on local host type "python app.py" and enter the api key as an argument.

## Testing:

To run the tests, you will have to open an additional terminal instance to keep the app going. On the new terminal change directory to ./tests/ and launch tests.py with the api key as an argument. Test results will be output onto the command line as the testing continues and will be summarised at the end in a list.

## Tools used:

1. Flask (Python library) for webhosting.
2. Selenium (Python library) for test automation and web scraping.
3. VSCode Thunderclient for manually calling APIs.

Future implementation of unittest framework should made test output more user-friendly.
