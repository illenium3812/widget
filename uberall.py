from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json


class Uberall:

    def get_results(self, results):
        search_results = {}
        for i in range(len(results)):
            Directory = results[i].find_elements_by_class_name(
                'ubsc_results-table-cell')[0].text
            directory_logo = results[i].find_elements_by_css_selector('img')[
                0].get_attribute('src')
            Business_Info = results[i].find_elements_by_class_name(
                'ubsc_results-table-cell')[1].text
            try:
                hours = results[i].find_elements_by_css_selector(
                    'img')[1].get_attribute('src')
            except:
                hours = ''
            try:
                photos = results[i].find_elements_by_css_selector(
                    'img')[2].get_attribute('src')
            except:
                photos = ''
            search_results[i] = {'Directory': Directory, 'Business Info': Business_Info,
                                 'Hours': hours, 'Photos': photos, 'logo': directory_logo}
        return search_results

    def make_call(self, query):
        # Setting up Dowloading Directory and Chrome Options
        chromedriver = "C:\\Users\\c\\anaconda3\\chromedriver.exe"
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chromedriver, chrome_options=options)
        try:
            # parsing the query into variables
            lst = query.split('-')
            Country = lst[0]
            Company_name = lst[1]
            Street_Number = lst[2]
            ZIP = lst[3]
        except:
            return "There is an issue with the query"

        # Opening up the website
        BaseUrl = "https://uberall.com/en/developers/statusCheckWidget"
        browser.get(BaseUrl)
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Select-control')))
        browser.find_element_by_xpath(
            "//div[@class='Select-control']").find_element_by_css_selector('input').send_keys(Country)
        browser.find_element_by_class_name('Select-menu-outer').click()
        browser.find_element_by_xpath(
            '//*[@id="widget-preview-box"]/div/div/div[1]/span/div/div/form/div[2]/input').send_keys(Company_name)
        browser.find_element_by_xpath(
            '//*[@id="widget-preview-box"]/div/div/div[1]/span/div/div/form/div[3]/input').send_keys(Street_Number)
        browser.find_element_by_xpath(
            '//*[@id="widget-preview-box"]/div/div/div[1]/span/div/div/form/div[4]/input').send_keys(ZIP)
        browser.find_element_by_xpath('//input[@value="CHECK NOW"]').click()
        try:
            time.sleep(3)
            map_inputs = browser.find_elements_by_class_name(
                'normalization-map-input')
            map_inputs[0].clear()
            map_inputs[0].send_keys(Street_Number)
            map_inputs[1].clear()
            map_inputs[1].send_keys(Street_Number)
            browser.find_element_by_class_name(
                'normalization-map-button').click()
        except Exception as e:
            pass
        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'ubsc_results-table-wrapper')))
        time.sleep(3)
        results = browser.find_elements_by_class_name(
            "ubsc_result-listing-row")
        search_results = self.get_results(results)
        return search_results
#         with open("results.json", "w") as write_file:
#             json.dump(search_results, write_file, indent=4)
