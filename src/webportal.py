import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
import constants as C


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
    driver.get(C.PLATFORM_URL)

    # log in
    print("Performing login...")
    login_field = driver.find_element(By.ID, 'val_loginAccount')
    login_field.clear()
    login_field.send_keys(C.USERNAME)

    passw_field = driver.find_element(By.ID, 'val_loginPwd')
    passw_field.clear()
    passw_field.send_keys(C.PASSWORD)

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
