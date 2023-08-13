import os
import re
from datetime import datetime

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# import tempfile

# setup
EXCEL_FILES_LOCATION = r"C:\Users\jorrit\drive\finance\nutsvoorzieningen\zonnepanelen\growatt_data\data_download\maandrapport"
MAXIMUM_GO_BACK_UNTIL_YEAR = 2017
MAXIMUM_GO_BACK_UNTIL_MONTH = 1
PLATFORM_URL = "https://server.growatt.com/login"
USERNAME =
PASSWORD =
DATABASE_LOCATION = r"C:\Users\jorrit\drive\finance\nutsvoorzieningen\zonnepanelen\growatt_data\data_download\growatt.db"

def find_starting_point_for_download():
    def extract_year_month(filename):
        # Extracts year and month using regex
        match = re.search(r'(\d{4}-\d{1,2})', filename)
        if match:
            year_month = match.group(1)
            year, month = map(int, year_month.split('-'))
            return year, month
        else:
            return None

    def get_most_recent_date(folder_path):
        excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xls')]

        if not excel_files:
            return None

        most_recent_date = None

        for excel_file in excel_files:
            year, month = extract_year_month(excel_file)
            date = datetime(year, month, 1)  # Assuming day 1 of the month
            if most_recent_date is None or date > most_recent_date:
                most_recent_date = date

        return most_recent_date

    most_recent_date = get_most_recent_date(EXCEL_FILES_LOCATION)
    if most_recent_date:
        return most_recent_date.year, most_recent_date.month
    else:
        return MAXIMUM_GO_BACK_UNTIL_YEAR, MAXIMUM_GO_BACK_UNTIL_MONTH

# step 1: find the most recent file where we have to restart downloading
y, m = find_starting_point_for_download()
print(f"{y}-{m}")

# # create a temp directory for the data file download
# temp_directory = tempfile.mkdtemp()
#
# # set the download folder
# options = webdriver.ChromeOptions()
# prefs = {"download.default_directory": temp_directory}
# options.add_experimental_option("prefs", prefs)
#
# # create the driver with these options
# driver = webdriver.Chrome(options=options)
#
#
# try:
#     driver.get('https://www.browserstack.com/test-on-the-right-mobile-devices')
#     # accept cookie
#     gotit = driver.find_element("id", 'accept-cookie-notification')
#     gotit.click()
#
#     # click download
#     downloadcsv = driver.find_element(By.CSS_SELECTOR, '.icon-csv')
#     downloadcsv.click()
#     time.sleep(5)
#     driver.close()
#
# except:
#      print("Invalid URL")