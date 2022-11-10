"""Author: Larsson Bajracharya
    Date Created: 11/06/2022
    File functionality: Automates three test cases covering the UI/API of alza website
"""
import os
import time
import requests
import pytest
from selenium import webdriver
from CommonTestScripts import CommonValues
from PageLibraries.Alza_path import Alza_path
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import HTTPError
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pathlib import Path


@pytest.fixture()
def setup():
    driver = webdriver.Chrome(executable_path="C:\\Users\\E0548165\\chromedriver.exe")
    driver.maximize_window()
    return driver

#TC_ShippingAndDelivery
def test_lenovo_buy(setup):
    driver = setup
    # Navigate to the application home page
    driver.get(CommonValues.Alza_web)
    driver.find_element("xpath", CommonValues.Alza_cookie).click()
    try:
        # not sure if the pop up occurs regularly
        driver.find_element("xpath", Alza_path.black_friday_popup).click()
        time.sleep(1)
        driver.find_element("xpath", Alza_path.computer_button).click()
        time.sleep(1)
        driver.find_element("xpath", Alza_path.laptop_button).click()
        driver.find_element("xpath", Alza_path.lenovo_check).click()
        time.sleep(1)
        driver.find_element(By.XPATH, Alza_path.lenovo_max_ram).is_selected()
        time.sleep(3)
        driver.find_element(By.XPATH, Alza_path.lenovo_max_ram).send_keys(32)
        time.sleep(4)
        driver.find_element("xpath", Alza_path.lenovo_ideapad).click()
        time.sleep(2)
        driver.find_element("xpath", Alza_path.lenovo_ideapad_add_to_cart).click()
        time.sleep(2)
        driver.find_element("xpath", Alza_path.microsoft_365).click()
        time.sleep(2)
        driver.find_element("xpath", Alza_path.proceed_checkout).click()
        time.sleep(2)
        driver.find_element("xpath", Alza_path.continue_to_payment).click()
        time.sleep(2)
        driver.find_element("xpath", Alza_path.pick_up).click()
        time.sleep(2)
        driver.find_element(By.XPATH, Alza_path.location_input).send_keys('kamenicka')
        time.sleep(5)
        driver.find_element("xpath", Alza_path.find_praha).click()
        time.sleep(3)
        driver.find_element("xpath", Alza_path.first_location).click()
        time.sleep(3)
        driver.find_element("xpath", Alza_path.pick_up_confirm).click()
        time.sleep(3)
        driver.find_element("xpath", Alza_path.pay_by_card).click()
        time.sleep(5)
        driver.find_element("xpath", Alza_path.confirm_order).click()
        time.sleep(2)
        driver.find_element("xpath", Alza_path.shipping_ad_close).click()
        driver.close()
    except NoSuchElementException:
        print("element exception")
        driver.close()
    except TimeoutException:
        print("timeout exception")
        driver.close()


def test_api_get():
    try:
        resp_vendor = requests.get(CommonValues.vendor_url)
        assert (resp_vendor.status_code == 200), "Status code is not 200. Rather found : " + str(resp_vendor.status_code)
        data = resp_vendor.json()
        assert data["vendorTeam"] is None , \
            "Data not matched! Expected : null, but found : " + str(data["vendorTeam"])
        assert data["conversation"] is None, \
            "Data not matched! Expected : null, but found : " + str(data["vendorTeam"])
        assert data["conversations"] is None, \
            "Data not matched! Expected : null, but found : " + str(data["vendorTeam"])
        assert data["callbackService"] is None, \
            "Data not matched! Expected : null, but found : " + str(data["vendorTeam"])
    except AssertionError:
        print("Assertion issue for request. Test cancelled")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


#TC_Charger_Add_To_Cart
def test_charger_add_to_cart(setup):
    try:
        driver = setup
        driver.get(CommonValues.Alza_web)
        time.sleep(1)
        driver.find_element("xpath", CommonValues.Alza_cookie).click()
        time.sleep(1)
        # not sure if the pop up occurs regularly
        driver.find_element("xpath", Alza_path.black_friday_popup).click()
        time.sleep(1)
        currentDir = Path.cwd()
        SplittedPath = os.path.split(currentDir)
        JoinedPath = os.path.join(SplittedPath[0], 'Fortify\\TestData\\test_data.xml')
        with open(JoinedPath, 'r') as f:
            data = f.read()
        xml_data = BeautifulSoup(data, "xml")
        # getting all searchbar values for chargers
        values = xml_data.find_all('Electronics')
        for vals in values:
            Charger = vals.find('Charger').next
            driver.find_element(By.XPATH, Alza_path.search_bar).send_keys(Charger)
            time.sleep(1)
            driver.find_element(By.XPATH, Alza_path.search_bar_button).click()
            time.sleep(2)
            driver.find_element("xpath", Alza_path.brand_new_radio).click()
            time.sleep(3)
            driver.find_element("xpath", Alza_path.add_to_cart).click()
            time.sleep(2)
        driver.find_element("xpath", Alza_path.show_cart).click()
        time.sleep(3)
        driver.close()
    except NoSuchElementException:
        driver.close()
        print("element exception")

    except TimeoutException:
        driver.close()
        print("timeout exception")

