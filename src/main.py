import os
import re
from datetime import datetime
from dotenv import load_dotenv
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import shutil

# setup
load_dotenv()
EXCEL_FILES_LOCATION = r"C:\Users\jorrit\drive\finance\nutsvoorzieningen\zonnepanelen\growatt_data\data_download\maandrapport"
MAXIMUM_GO_BACK_UNTIL_YEAR = 2017
MAXIMUM_GO_BACK_UNTIL_MONTH = 1
PLATFORM_URL = "https://server.growatt.com/login"
USERNAME = os.getenv("growatt-username")
PASSWORD = os.getenv("growatt-password")
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
        return {'year': most_recent_date.year, 'month': most_recent_date.month}
    else:
        return MAXIMUM_GO_BACK_UNTIL_YEAR, MAXIMUM_GO_BACK_UNTIL_MONTH


def download_files_from_online_portal(halt_at):
    # create a temp directory for the data file download
    temp_directory = tempfile.mkdtemp()
    print(f"Temp directory for downloads: {temp_directory}")

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": temp_directory}
    options.add_experimental_option("prefs", prefs)

    # create the driver with these options
    driver = webdriver.Chrome(options=options)

    print("Navigating to portal using selenium...")
    # go to website
    driver.get(PLATFORM_URL)

    # log in
    print("Performing login...")
    login_field = driver.find_element(By.ID, 'val_loginAccount')
    login_field.clear()
    login_field.send_keys(USERNAME)

    passw_field = driver.find_element(By.ID, 'val_loginPwd')
    passw_field.clear()
    passw_field.send_keys(PASSWORD)

    signin_btn = driver.find_element(By.CLASS_NAME, "loginB")
    signin_btn.click()

    # go to the energy - monthly menu
    print("Navigating to Energy dashboard...")
    time.sleep(2)
    energy_div_button = driver.find_element(By.CLASS_NAME, "div_menu_energy")
    energy_div_button.click()
    time.sleep(2)

    # find all tabs and look for the one with data-val="1" => DAY TAB
    i_elements = driver.find_elements(By.CSS_SELECTOR, "i.btn-pan.btn_energy_compare_timeType")
    for i_element in i_elements:
        if i_element.get_attribute("data-val") == "1":
            i_element.click()
            time.sleep(1)
            break

    while True:
        # get the year-month for this page
        date_selector = driver.find_element(By.ID, 'val_energy_compare_Time')
        current_page_year_month = date_selector.get_attribute("value")
        y, m = map(int, current_page_year_month.split('-'))
        current_page = {'year': y, 'month': m}

        print(f"Downloading {current_page}...")

        # export + download button
        export_btn = driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/input')
        export_btn.click()
        time.sleep(1)

        download_btn = driver.find_element(By.XPATH,
                                           '//*[@id="div_pageContent"]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/dl/dd[2]')
        download_btn.click()
        time.sleep(2)

        # go back one month
        prev_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div/i[1]')
        prev_btn.click()
        time.sleep(2)

        # break if we have arrived at the latest existing file
        # (which we have downloaded again to guarantee completeness)
        if current_page == halt_at:
            break

    driver.close()
    return temp_directory


def copy_back_monthly_excel_reports(source_folder, target_folder):
    # List all files in the source folder
    files = os.listdir(source_folder)

    for file in files:
        source_path = os.path.join(source_folder, file)
        target_path = os.path.join(target_folder, file)

        # Copy the file from source to target, overwriting if exists
        print(f"Writing {target_path}")
        shutil.copy2(source_path, target_path)

def main():
    # step 1: find the most recent file where we have to restart downloading
    halt_at = find_starting_point_for_download()

    # step 2: fetch from web portal using selenium
    temp_dir = download_files_from_online_portal(halt_at)
    print("step 2 done, folder: " + temp_dir)

    # step 3: copy temp files to excel folder
    copy_back_monthly_excel_reports(temp_dir, EXCEL_FILES_LOCATION)

if __name__ == "__main__":
    main()

