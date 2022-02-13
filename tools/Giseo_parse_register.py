import time
from bs4 import BeautifulSoup as bs
from decouple import config
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pprint import pprint
import json

driver_path = config('DRIVER_PATH')
project_path = config('PATH_P')
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(options=options, executable_path=driver_path)
driver.get('https://giseo.rkomi.ru/about.html')
sleep = 0.5

DATA = {}
provinces = Select(driver.find_element_by_id('provinces'))
for i_provinces in range(1, len(provinces.options)):
    provinces.select_by_index(i_provinces)
    html = driver.page_source
    soup = bs(html, 'html5lib')
    select_provinces = soup.find_all('div', class_='row form-horizontal')[2]
    province = select_provinces.find_all('option')[i_provinces]
    time.sleep(sleep)

    cities = Select(driver.find_element_by_id('cities'))
    data_citi = {}
    for i_cities in range(1, len(cities.options)):
        cities.select_by_index(i_cities)
        html = driver.page_source
        soup = bs(html, 'html5lib')
        select_cities = soup.find_all('div', class_='row form-horizontal')[3]
        citi = select_cities.find_all('option')[i_cities]
        time.sleep(sleep)

        funcs = Select(driver.find_element_by_id('funcs'))
        data_func = {}
        for i_funcs in range(1, len(funcs.options)):
            funcs.select_by_index(i_funcs)
            html = driver.page_source
            soup = bs(html, 'html5lib')
            select_funcs = soup.find_all('div', class_='row form-horizontal')[4]
            func = select_funcs.find_all('option')[i_funcs]
            time.sleep(sleep)

            schools = Select(driver.find_element_by_id('schools'))
            data_school = []
            for i_schools in range(1, len(schools.options)):
                schools.select_by_index(i_schools)
                html = driver.page_source
                soup = bs(html, 'html5lib')
                select_schools = soup.find_all('div', class_='row form-horizontal')[5]
                school = select_schools.find_all('option')[i_schools]
                data_school.append(school.text)
                # DATA.append([province.text, citi.text, func.text, school.text])
                print(f'{province.text}, {citi.text}, {func.text}, {school.text}')

            data_func[func.text] = data_school

        data_citi[citi.text] = data_func

    DATA[province.text] = data_citi


with open(f'{project_path}/data/basic/data_registration_giseo.json', 'w', encoding='UTF-8') as f:
    json.dump(obj=DATA, fp=f, sort_keys=False, indent=4, ensure_ascii=False)


