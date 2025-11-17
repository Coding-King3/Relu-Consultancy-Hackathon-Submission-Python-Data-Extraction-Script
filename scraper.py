import os
import time
import random
import csv
import logging

import pandas as pd
from openpyxl.xml.constants import XPROPS_NS
from pandas.core.dtypes.base import register_extension_dtype
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By # Optional, for locating elements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


def load_chromedriver():
    try:
        # Using random user agents so that it avoids bot dection
        list_of_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        ]
        random_user_agent = random.choice(list_of_user_agents)

        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument(f"--user-agent={random_user_agent}")

        working_directory = os.getcwd()
        c_driver_path = working_directory + '\\chromedriver.exe'

        service = Service(executable_path=c_driver_path)
        chrome_driver = webdriver.Chrome(service=service, options=chrome_options)

        return chrome_driver
    except Exception:
        logger.exception("Problem in load_chromedriver function")


def visit_web_page():
    # added explicit wait so that the crawler doesn't stuck
    try:

        driver.get('https://www3.shoalhaven.nsw.gov.au/masterviewUI/modules/ApplicationMaster/Default.aspx')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[value = 'Agree']")))
        driver.find_element(By.CSS_SELECTOR, "[value = 'Agree']").click()
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class = 'rmLink ']//*[contains(text(), 'DA')]")))
        driver.find_element(By.XPATH,"//*[@class = 'rmLink ']//*[contains(text(), 'DA')]").click()
        time.sleep(1)

        "//*[@class = 'rtsTxt'][contains(text(), 'Advanced')]"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class = 'rtsTxt'][contains(text(), 'Advanced')]"
                                            )))

        driver.find_element(By.XPATH, "//*[@class = 'rtsTxt'][contains(text(), 'Advanced')]"
                            ).click()

        time.sleep(2)
        driver.find_element(By.ID, "ctl00_cphContent_ctl00_ctl03_dateInput_text").send_keys('1/09/2025')
        time.sleep(1)
        driver.find_element(By.ID, "ctl00_cphContent_ctl00_ctl05_dateInput_text").send_keys("30/09/2025")
        time.sleep(1)
        driver.find_element(By.ID, "ctl00_cphContent_ctl00_ctl05_dateInput_text").send_keys(Keys.TAB)
        time.sleep(1)
        driver.find_element(By.ID, "ctl00_cphContent_ctl00_btnSearch").click()


        # Below logic actually increases url length available on the page and reduces pages to browse
        # to gather urls, This saves time

        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class = 'RadGrid RadGrid_Default']")))
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "RadComboBox.RadComboBox_Default ").click()
        time.sleep(2)
        # select_object = Select(dropdown_element)
        driver.find_element(By.CSS_SELECTOR, "[class = 'rcbList'] li:last-of-type").click()
        time.sleep(2)
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class = 'RadGrid RadGrid_Default']")))
        time.sleep(3)
    except Exception:
        logger.exception("Problem in visit Web page function")


def scraping_links_handling_pagination():

    # This code basically, scrapes destination url available on each page,

    try:
        find_page_length = driver.find_elements(By.CSS_SELECTOR, "[class = 'rgWrap rgNumPart'] span").__len__()
        find_page_length += 1
        # Purposely reduced zoom to 30% because page loads faster when zoom ratio is minimum

        driver.execute_script("document.body.style.zoom='30%'")
        list_of_urls = []
        selenium_cookies = driver.get_cookies()
        # added scrolling so that for some problem if next page button is not clickable,
        # the bottom scroll can work and find the element properly

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        for next_page in range(1, find_page_length):
            if next_page == 1:
                pass
            else:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"(//*[@class = 'rgWrap rgNumPart']//a)[{next_page}]")))

                driver.find_element(By.XPATH, f"(//*[@class = 'rgWrap rgNumPart']//a)[{next_page}]").click()
                time.sleep(3)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class = 'RadGrid RadGrid_Default']")))

            time.sleep(1)
            get_links = driver.find_elements(By.XPATH, "//*[@class = 'rgRow' or @class = 'rgAltRow']//a")


            for getting_urls in get_links:
                list_of_urls.append(getting_urls.get_attribute('href'))

        return list_of_urls, selenium_cookies

    except Exception:
        logger.exception("Problem in scraping links and handling pagination function")

def scraping_main_data():
    try:
        # used dictionary here, where keys are heading and values are id locators to find text
        # As per me this reduces code.

        csv_headers = {"DA_Number": "ctl00_cphContent_ctl00_lblApplicationHeader","Detail_URL" : None, "Description" : None, "Submitted_Date" : None,"Decision" :'lblDecision', "Categories" : "lblCat", "Property_Address":"lblProp", "Applicant":None, "Progress":"lblProg", "Fees":"lblFees"
            , "Documents":"lblDocs", "Contact Council":"lbl91"}

        file_name = "scraped_data.csv"

        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers.keys())

        # Here I have used cookies of selenium webdriver which we used to find links, page navigation etc
        # This actually makes website server think that a previous user has logged in again and visiting site.
        session = requests.Session()
        request_cookies = {
            cookies['name'] : cookies['value']
            for cookies in cookie_data
        }
        session.cookies.update(request_cookies)
        time.sleep(1)
        driver.quit()

        with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            for accessing_url in url_data[214:216]:
                # Added uniform sleep so that server doesn't get bombard with multiple request
                delay_seconds = random.uniform(2,3)
                time.sleep(delay_seconds)
                print(accessing_url)

                response = session.get(accessing_url)

                soup = BeautifulSoup(response.text, 'html.parser')
                # print(soup.prettify())
                data_append = []

                for key,val in csv_headers.items():

                    if key == 'Detail_URL':
                        data_append.append(accessing_url)

                    elif key == 'Description':
                        find_details = soup.find(id = 'lblDetails')
                        new_text = find_details.text
                        clean_text = new_text.split('Submitted:')[0].replace('Description:', '')
                        data_append.append(clean_text)

                    elif key == 'Submitted_Date':
                        find_details = soup.find(id = 'lblDetails')
                        new_text = find_details.text
                        clean_text = new_text.split('Submitted: ')[1]
                        data_append.append(clean_text)

                    elif key == 'Applicant':
                        find_details = soup.find(id = 'lblPeople')
                        new_text = find_details.text
                        clean_text = new_text.split('Applicant: ')[1]
                        data_append.append(clean_text)

                    else:
                        find_details = soup.find(id=val)

                        if val == 'lblProg' or val == 'lblFees':
                            new_text = find_details.text
                            clean_text = ' '.join(new_text.split())
                        else:
                            clean_text = find_details.text.strip()
                        data_append.append(clean_text)

                writer.writerow(data_append)

        return file_name

    except Exception:
        logger.exception("Problem in scraping main data function")

def clean_data():
    try:

        df = pd.read_csv(csv_file)
        df['Fees'] = df['Fees'].astype(str).str.replace("No fees recorded against this application.", "Not Required", regex=False)
        df['Contact Council'] = df['Contact Council'].astype(str).str.replace("Application Is Not on exhibition, please call Council on 1300 293 111 if you require assistance.", "Not Required", regex=False)
        df.to_csv(csv_file, index=False)

    except Exception:
        logger.exception("Error in clean data function")


if __name__ == '__main__':
    LOG_FILENAME = 'scraper_log.text'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILENAME, mode='a'),
        ]
    )

    logger = logging.getLogger(__name__)

    driver = load_chromedriver()
    visit_web_page()
    url_data, cookie_data = scraping_links_handling_pagination()
    csv_file = scraping_main_data()
    clean_data()

    if driver:
        driver.quit()
    else:
        pass
