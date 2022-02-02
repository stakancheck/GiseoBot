import os
import time
import logging
import datetime
from decouple import config
from bs4 import BeautifulSoup
from selenium import webdriver
from cryptography.fernet import Fernet
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from tools import DbTools, base_model, ImageConstructor

cipher_key = config('CIPHER_KEY')
project_path = config('PATH_P')

logging.basicConfig(filename=f'{project_path}\\data\\basic\\giseo_parser.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s: %(levelname)s -> %(message)s')


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
        logging.info(f'Create user {chat_id}')

        # Create folder special for user
        if not os.path.exists(f'{project_path}\\data\\assets\\user_{chat_id}'):
            os.makedirs(f'{project_path}\\data\\assets\\user_{chat_id}')

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

        if not DbTools.check_user_exists(self.chat_id):
            self.login_user()
        else:
            self.progress = 5
            logging.info(f'User {self.chat_id} already added to DB')

        try:
            self.start_parse()
        except Exception as e:
            logging.error(e)

    def login_user(self):
        base_model.User.create_table()
        new_user = base_model.User.create(chat_id=self.chat_id, login=self.login, password=self.password,
                                          place=self.place, town=self.town, type_school=self.type_school,
                                          school=self.school, theme=self.theme, date_update=self.date_update)
        new_user.save()
        # data = (self.chat_id, self.login, self.password, self.place,
        #         self.town, self.type_school, self.school, self.theme, self.date_update)
        # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
        #     cur = conn.cursor()
        #     cur.execute(
        #         "CREATE TABLE IF NOT EXISTS users(chat_id INT, login TEXT, password TEXT, place TEXT, town TEXT, "
        #         "type_school TEXT, school TEXT, theme TEXT, time_update DATETIME);")
        #     conn.commit()
        #     cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
        #     conn.commit()
        #     cur.close()
        logging.info(f'Add user to data.db message_id {self.chat_id}')
        self.progress = 5

    def start_parse(self):
        logging.info('Start get page')
        settings = webdriver.ChromeOptions()
        # settings.binary_location = f'{project_path}\\tool_4\\GoogleChromePortable.exe'
        if not self.DEBUG:
            settings.add_argument('headless')  # аргумент отвечает за запуск окна в скрытом режиме
        driver = webdriver.Chrome(options=settings, executable_path=f'{project_path}\\tool_driver\\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get("https://giseo.rkomi.ru/about.html")
        logging.info('Complete get page')
        self.progress = 10
        time.sleep(0.7)
        self.get_page(driver)

    def get_page(self, driver):
        """
        Input information about user and get html
        :param driver: driver selenium
        :return:
        """

        # Enter place
        try:
            in_place = Select(driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[3]/div/select'))
            in_place.select_by_visible_text(self.place)
        except Exception as e:
            logging.error(f"Place '{self.place}' is not defined in list, except: {e}, user: {self.chat_id}")

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
            logging.error(f"Type_school '{self.type_school}' is not defined in list, except: {e}, user: {self.chat_id}")

        self.progress = 19
        # Enter name of school
        try:
            in_school = Select(driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[6]/div/select'))
            in_school.select_by_visible_text(self.school)
        except Exception as e:
            logging.error(f"Name of school '{self.school}' is not defined in list, except: {e}, user: {self.chat_id}")

        self.progress = 23
        # Enter login and password
        in_login = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[8]/input')
        in_login.send_keys(self.login)
        in_password = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[9]/input')
        cipher = Fernet(cipher_key)
        password_not_crypt = cipher.decrypt(self.password.encode()).decode()
        in_password.send_keys(password_not_crypt)
        self.progress = 26
        # Try to login with already entered login and password
        try:
            driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/div[12]/a/span').click()
        except Exception as e:
            logging.error(f'Not all info is entered!')
        logging.info(f'Successful login, user: {self.chat_id}')

        self.progress = 29
        # Skip warning
        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div/div[4]/div/div/div/div/button[2]/span[2]').click()
        except:
            logging.error(f'Skip warning error!')

        try:
            time.sleep(self.TIME_SLEEP)
            # self.parse_final(driver)
            # time.sleep(self.TIME_SLEEP)
            # self.parse_middle_marks_year(driver)
            # time.sleep(self.TIME_SLEEP)
            # self.parse_middle_marks_period(driver)
            # time.sleep(self.TIME_SLEEP)
            self.parse_schedule(driver)
            time.sleep(self.TIME_SLEEP)
            self.parse_duty(driver)
            self.quit_giseo(driver)
        except Exception as e:
            logging.error(e)

    def parse_schedule(self, driver):
        logging.info(f'Start parse schedule for user {self.chat_id}')
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('/html/body/div[1]/div[4]'
                                                                          '/nav/ul/li[4]/a')).perform()
        driver.find_element_by_xpath('/html/body/div[1]/div[4]/nav/ul/li[4]/ul/li[1]/a').click()
        time.sleep(1)
        html = driver.page_source
        # print(html)
        soup = BeautifulSoup(html, 'html5lib')
        days = soup.find_all('div', class_='day_table')
        # pprint(days)
        data = []

        for y in range(len(days)):
            date = days[y].find('span', class_='ng-binding').text
            work = days[y].find_all('tr', class_='ng-scope')
            year = date[-7:-3]
            day_ = date[4:6].replace(' ', '')
            if len(day_) == 1:
                day_ = "0" + day_
            month = self.date_reformat(date)
            date_fin = f'{year}-{month}-{day_}'
            for i in range(len(work)):
                les = work[i].find_all('td')[1]
                name_les = les.find('a')

                if name_les is not None:
                    hw = work[i].find('a', class_='ng-binding ng-scope')
                    if hw is not None:
                        hw = hw.text
                    else:
                        hw = ''
                    if len(name_les.text) > 30:
                        name_les = name_les.text[:29] + '...'
                    else:
                        name_les = name_les.text
                    time_start = str(les.find('div').text[:5]) + ':00'
                    time_finish = str(les.find('div').text[8:13]) + ':00'
                    data_local = {'date': date_fin, 'affair': name_les, 'homework': hw, 'time_end': time_finish,
                                  'time_start': time_start}
                    data.append(data_local)

        # pprint(data)

        data_local_tb = data
        # for item in data:
        #     # print(item['date'])
        #     # 2021-10-04
        #     # 2021-10-05
        #
        #     # print(f"{item['date']} ----- {datetime.date.today()}")
        #     # item['date'] == str(datetime.date.today()) - datetime.timedelta(days=1) условие для вчера
        #     date = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
        #     if datetime.date.today().weekday() != 6:
        #         if item['date'] == str(datetime.date.today()) or \
        #                 item['date'] == str(datetime.date.today() + datetime.timedelta(days=1)):
        #             data_local_tb.append(item)
        #     else:
        #         if item['date'] == str(datetime.date.today() + datetime.timedelta(days=1)) or \
        #                 item['date'] == str(datetime.date.today() + datetime.timedelta(days=2)):
        #             data_local_tb.append(item)

        # pprint(data_local_tb)
        # print(str(datetime.date.today() - datetime.timedelta(days=1)))

        # Очистка базы от старых записей
        model = base_model.Schedule.delete().where(base_model.Schedule.chat_id == self.chat_id)
        model.execute()

        text = {
            '0': [],
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': []
        }

        if data_local_tb:
            # print(f"now: {datetime.datetime.today().weekday()}")
            for item in data_local_tb:
                date = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
                # print(date.weekday())
                # weekday 0 monday 6 sunday
                mass = text[str(date.weekday())]
                homework_text = item['homework']

                mass.append([f"{item['time_start'][:-3]} - {item['time_end'][:-3]}", item['affair']])
                text[str(date.weekday())] = mass

                # Создание записи в базе данных
                d = base_model.Schedule.create(chat_id=self.chat_id,
                                               time=f"{item['time_start'][:-3]} - {item['time_end'][:-3]}",
                                               subject=item['affair'],
                                               day=date.weekday(),
                                               homework=homework_text)
                d.save()

        labels = ('Время', 'Урок')

        for i in range(6):
            if os.path.exists(f'{project_path}\\data\\assets\\user_{self.chat_id}\\parse_schedule_{i}.png'):
                os.remove(f'{project_path}\\data\\assets\\user_{self.chat_id}\\parse_schedule_{i}.png')

        for key in text.keys():
            if text[str(key)]:
                ImageConstructor.creation_image(text[str(key)], labels, self.theme, self.chat_id,
                                                f'parse_schedule_{key}.png')
                logging.info(f'Successes save schedule {key} for user {self.chat_id}')

    def parse_duty(self, driver):
        """
        Parsing Duty from schedule window
        :param driver: driver selenium
        :return:
        """

        logging.info(f'Start parse duty for user {self.chat_id}')

        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div/'
                                     'div[2]/div/div/div[2]/div[1]/div[2]/div[3]/i').click()
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div/div[2]'
                                         '/div/div/div[1]/past-mandatory/div/div[1]/i[1]').click()
        except Exception as e:
            logging.error(e)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find('table', class_='hidden-mobile')
        rows = table.find_all('tr', class_='ng-scope')

        for item in rows:
            subject = item.find('td', class_='subject_data').find('a').text
            task = item.find('td', class_='theme_data').find('a').text
            date = item.find('td', class_='date_data').find('a').text
            # print(f'{subject} - {task} - {date}')
            d = base_model.Duty.create(chat_id=self.chat_id, subject=subject, task=task, date=date)
            d.save()

        logging.info(f'Successes save duty for user {self.chat_id}')

    def parse_final(self, driver):
        """
        Parse final marks
        :param driver: driver selenium
        :return:
        """

        # Path to table marks

        driver.find_element_by_xpath('/html/body/div[1]/div[4]/nav/ul/li[3]/a').click()
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div/div[2]/div/table/tbody/tr[2]/td[2]/a').click()
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div/div[3]/div/div/div[1]/button[1]/span[2]').click()
        time.sleep(self.TIME_SLEEP)
        html = driver.page_source

        # Очистка базы от старых записей
        model = base_model.FinalMarks.delete().where(base_model.FinalMarks.chat_id == self.chat_id)
        model.execute()

        # Find elements of table
        soup = BeautifulSoup(html, 'html5lib')
        data = []

        if soup.find('table', class_='table-print-num'):
            rows = soup.find('table', class_='table-print-num').find_all('tr')
            rows.pop(0)  # delete waste info
            rows.pop(0)  # delete waste info

            # Add info in list
            for i in range(len(rows)):
                t = rows[i].find_all('td')
                if len(t[1].text) > 30:
                    name = t[1].text[:29] + '...'
                else:
                    name = t[1].text

                for z in range(2, 6):
                    if t[z].text == u'\xa0':
                        t[z] = 0
                    else:
                        t[z] = int(t[z].text)

                data.append([name, t[2], t[3], t[4], t[5], t[6].text])

                base_model.FinalMarks.create(chat_id=self.chat_id,
                                             subject=name,
                                             quarter_1=t[2],
                                             quarter_2=t[3],
                                             quarter_3=t[4],
                                             quarter_4=t[5],
                                             final_mark=t[6].text)

        labels = ('Предмет', ' 1 ', ' 2 ', ' 3 ', ' 4 ', 'Итог')

        if data:
            ImageConstructor.creation_image(data, labels, self.theme, self.chat_id, 'parse_final_marks.png')
        else:
            if os.path.exists(f'{project_path}\\data\\assets\\user_{self.chat_id}\\parse_final_marks.png'):
                os.remove(f'{project_path}\\data\\assets\\user_{self.chat_id}\\parse_final_marks.png')

        logging.info(f'Successes save final_marks for user {self.chat_id}')

    def parse_middle_marks_year(self, driver):
        """
        Parsing middle marks of all year
        :param driver: driver selenium
        :return:
        """
        # Path to table marks

        driver.find_element_by_xpath('/html/body/div[1]/div[4]/nav/ul/li[3]/a').click()
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div/div[2]/div/table/tbody/tr[3]/td[2]/a').click()
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div/div/div[3]/div/div/div[1]/button[1]/span[2]').click()
        time.sleep(self.TIME_SLEEP)
        html = driver.page_source

        # Очистка базы от старых записей
        model = base_model.MiddleMarksYear.delete().where(base_model.MiddleMarksYear.chat_id == self.chat_id)
        model.execute()

        # Find elements of table
        soup = BeautifulSoup(html, 'html5lib')
        data = []

        if soup.find('tr', class_='chart-labels-row'):
            names = soup.find('tr', class_='chart-labels-row').find_all('th')
            names.pop(0)  # delete waste info
            marks = soup.find('tr', class_='text-nowrap chart-data-row').find_all('td')
            marks.pop(0)  # delete waste info

            # Add info in list
            for i in range(len(names)):
                data.append([names[i].text, marks[i].text])
                base_model.MiddleMarksYear.create(chat_id=self.chat_id,
                                                  subject=names[i].text,
                                                  marks=marks[i].text)
        labels = ('Предмет', 'Балл')

        if data:
            ImageConstructor.creation_image(data, labels, self.theme, self.chat_id, 'parse_middle_marks_year.png')
        else:
            if os.path.exists(f'{project_path}\\data\\assets\\user_{self.chat_id}\\parse_middle_marks_year.png'):
                os.remove(f'{project_path}\\data\\assets\\user_{self.chat_id}\\parse_middle_marks_year.png')

        logging.info(f'Successes save middle_marks_year for user {self.chat_id}')

    def parse_middle_marks_period(self, driver):
        """
        Parsing middle marks of one period
        :param driver: driver selenium
        :return:
        """

        try:
            # Path to certain period
            driver.find_element_by_xpath('/html/body/div[1]/div[4]/nav/ul/li[3]/a').click()
            driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div/div/div/div[2]/div/table/tbody/tr[10]/td[2]/a').click()
        except Exception as e:
            logging.error(e)

        # Очистка базы от старых записей
        model = base_model.MiddleMarksPeriod.delete().where(base_model.MiddleMarksPeriod.chat_id == self.chat_id)
        model.execute()

        for period in range(1, 5):
            # driver.find_element_by_xpath(
            #     '/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/form/div/div/div/div[3]/div/select').click()
            if period == 1:
                Select(driver.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/form/div/div/div/div[3]/div/select')).select_by_index(
                    0)
                # driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div['
                #                              '1]/form/div/div/div/div[3]/div/select/option[1]').click()
            elif period == 2:
                Select(driver.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/form/div/div/div/div[3]/div/select')).select_by_index(
                    1)

                # driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div['
                #                              '1]/form/div/div/div/div[3]/div/select/option[2]').click()
            elif period == 3:
                Select(driver.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/form/div/div/div/div[3]/div/select')).select_by_index(
                    2)

                # driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div['
                #                              '1]/form/div/div/div/div[3]/div/select/option[3]').click()
            elif period == 4:
                Select(driver.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/div/div/div/div[2]/div[1]/form/div/div/div/div[3]/div/select')).select_by_index(
                    3)

                # driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div['
                #                              '1]/form/div/div/div/div[3]/div/select/option[4]').click()
            time.sleep(0.5)

            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div/div[3]/div/div/div[1]/button[1]').click()

            time.sleep(1)
            html = driver.page_source

            # Find elements of table
            soup = BeautifulSoup(html, 'html5lib')
            data = {}
            elements = soup.find('table', class_='table-print').find_all('tr')
            elements.pop(len(elements) - 1)
            elements.pop(0)  # delete waste info
            elements.pop(0)  # delete waste info
            for item in elements:
                if item.find_all('td')[5].text != '\xa0':
                    data[item.find_all('td')[0].text] = item.find_all('td')[5].text
            text = []
            labels = ('Предмет', 'Балл')

            # Add info in list
            for i in data:
                if len(i) > 30:
                    name = i[:29] + '...'
                else:
                    name = i
                text.append([name, data[i]])

                base_model.MiddleMarksPeriod.create(chat_id=self.chat_id,
                                                    subject=name,
                                                    period=period,
                                                    marks=data[i])

            if data:
                ImageConstructor.creation_image(text, labels, self.theme, self.chat_id,
                                                f'parse_middle_marks_period_{period}.png')
            else:
                if os.path.exists(f'{project_path}\\data\\assets\\user_{self.chat_id}\\'
                                  f'parse_middle_marks_period_{period}.png'):
                    os.remove(f'{project_path}\\data\\assets\\user_{self.chat_id}\\'
                              f'parse_middle_marks_period_{period}.png')

            logging.info(f'Successes save middle_marks_period for period {period} user {self.chat_id}')

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
        logging.info(f'Successes quit from giseo for user {self.chat_id}')
        driver.quit()

    @staticmethod
    def date_reformat(date_old):
        """
        Reformat date
        :param date_old: old format
        :return: new format date: string
        """
        month = ''
        if date_old.find('янв') > 0:
            month = '01'
        elif date_old.find('февр') > 0:
            month = '02'
        elif date_old.find('мар') > 0:
            month = '03'
        elif date_old.find('апр') > 0:
            month = '04'
        elif date_old.find('мая') > 0:
            month = '05'
        elif date_old.find('июня') > 0:
            month = '06'
        elif date_old.find('июля') > 0:
            month = '07'
        elif date_old.find('авг') > 0:
            month = '08'
        elif date_old.find('сент') > 0:
            month = '09'
        elif date_old.find('окт') > 0:
            month = '10'
        elif date_old.find('нояб') > 0:
            month = '11'
        elif date_old.find('дек') > 0:
            month = '12'
        return month


if __name__ == "__main__":
    then = datetime.datetime.now()
    user = Parse(chat_id=12324, place='Городской округ Сыктывкар', town='Сыктывкар, г.',
                 type_school='Общеобразовательная',
                 school='МАОУ "Технологический лицей"',
                 login='СухановА2',
                 password='gAAAAABg4xihX5qenJQewYVg7YyDf4GhPf0mAjj4iWJib49quBYItFSNObW8y'
                          'NrSUUkRM1EFS3KjqkjvP9MN66Wb3y3CmzglBA==', theme='theme_1')
    logging.shutdown()
    now = datetime.datetime.now()
    duration = now - then
    print(f'finished: {duration.total_seconds()} sec')
