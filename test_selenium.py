import datetime
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from decouple import config
from threading import Thread
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

cipher_key = config('CIPHER_KEY')
project_path = config('PATH_P')
url = "https://giseo.rkomi.ru/about.html"

data = (
        [123456, 'ОплеснинаЯ1', '04072006', 'Городской округ Сыктывкар', 'Сыктывкар, г.',
         'Общеобразовательная',
         'МАОУ "Технологический лицей"', 'theme_1'],

        [123456, 'СухановА2', '290483', 'Городской округ Сыктывкар', 'Сыктывкар, г.',
         'Общеобразовательная',
         'МАОУ "Технологический лицей"', 'theme_1'],
        # [212343, 'Городской округ Сыктывкар', 'Городской округ Сыктывкар', 'Сыктывкар, г.', 'Общеобразовательная',
        #  'МАОУ "Технологический лицей"', 'Криштопа', '04072006', 'theme_1']
        )


def get_page(mass):
    user = Parse(*mass)


class Parse:
    def __init__(self, chat_id, login, password, place, town, type_school, school, theme):
        """
        Class to parsing info
        :param chat_id:
        :param login:
        :param password:
        :param place:
        :param town:
        :param type_school:
        :param school:
        :param theme:
        """

        # Create folder special for user
        # if not os.path.exists(f'{project_path}\\data\\assets\\user_{chat_id}'):
        #     os.makedirs(f'{project_path}\\data\\assets\\user_{chat_id}')

        # User information
        self.chat_id = chat_id
        self.login = login
        self.password = password
        self.place = place
        self.town = town
        self.type_school = type_school
        self.school = school
        self.date_update = datetime.datetime.today()
        self.theme = theme
        self.progress = 0

        # Parameters for execute
        self.TIME_SLEEP = 0.6
        self.DEBUG = False

        self.start_parse()

    def start_parse(self):
        settings = webdriver.ChromeOptions()
        # settings.binary_location = f'{project_path}\\tool_4\\GoogleChromePortable.exe'
        driver = webdriver.Chrome(executable_path=f'{project_path}\\tool_driver\\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get("https://giseo.rkomi.ru/about.html")
        self.progress = 10
        time.sleep(1)
        self.get_page(driver)

    def get_page(self, driver):
        """
        Input information about user and get html
        :param driver: driver selenium
        :return:
        """
        print(f'start: {self.login}')
        # Enter place
        try:
            in_place = Select(driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[3]/div/select'))
            in_place.select_by_visible_text(self.place)
        except Exception as e:
            pass
        self.progress = 13
        # Enter town
        try:
            in_town = Select(driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[4]/div/select'))
            in_town.select_by_visible_text(self.town)
        except:
            pass

        self.progress = 16
        # Enter type of school
        try:
            in_type_school = Select(
                driver.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[5]/div/select'))
            in_type_school.select_by_visible_text(self.type_school)
        except Exception as e:
            pass
        self.progress = 19
        # Enter name of school
        try:
            in_school = Select(driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[6]/div/select'))
            in_school.select_by_visible_text(self.school)
        except Exception as e:
            pass
        self.progress = 23
        # Enter login and password
        in_login = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[8]/input')
        in_login.send_keys(self.login)
        in_password = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[9]/input')

        in_password.send_keys(self.password)

        self.progress = 26
        # Try to login with already entered login and password
        try:
            driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[12]/a/span').click()
        except Exception as e:
            pass

        self.progress = 29
        # Skip warning
        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]/span[2]').click()
        except:
            pass

        # time.sleep(self.TIME_SLEEP)
        # self.parse_final(driver)
        # time.sleep(self.TIME_SLEEP)
        # self.parse_middle_marks_year(driver)
        # time.sleep(self.TIME_SLEEP)
        # self.parse_middle_marks_period(driver)
        print(f'finish: {self.login}')
        time.sleep(4)
        self.quit_giseo(driver)

    def quit_giseo(self, driver):
        """
        Exit from Giseo.rkomi.ru
        :param driver: driver selenium
        :return:
        """

        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul/li[3]/a/span[2]').click()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[3]/div/div/button[1]').click()
        print(f'Successes quit from giseo for user {self.chat_id}')
        driver.quit()


for item in data:
    Thread(target=get_page, args=(item,)).start()
