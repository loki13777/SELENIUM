import json
from constants import *
from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path='chromedriver')

with driver:
    # открываем страницу
    driver.get(url)
    # находим и нажимаем кнопку принять (найстроки coocies)
    driver.find_element('css selector', css_accept).click()
    time.sleep(1)
    # находим и нажимаем кнопку каталог
    driver.find_element('xpath', xpath_catalog).click()
    time.sleep(1)
    # находим все стартовые категории
    start_categories = driver.find_elements('css selector', css_start_categories)
    # записываем названия категорий в список
    list_start_categories = [el.text for el in start_categories]
    # создаём словарь для записи результата
    dict_results = {}
    # проходимя списком по именам категорий
    for str_start_category in list_start_categories:
        # создаём словарь для подкатегорий
        dict_subcategories = {}
        time.sleep(3)
        # находим и нажимаем кнопку категории подставляя её имя в xpath
        driver.find_element('xpath', f"// span[text() = '{str_start_category}']").click()
        time.sleep(3)
        # находим все подкатегории на странице категории
        subcategories = driver.find_elements('css selector', css_subcategories)
        for subcategory in subcategories:
            # записываем в словарь ключём название подкатегории а значением ссылку на эту подкатегорию
            dict_subcategories[subcategory.text] = subcategory.get_attribute('href')
        # добавляем в результирующий словарь ключём название категории а значением словарь с подкатегориями
        dict_results[str_start_category] = dict_subcategories
        # перезаписываем результирующий словарь в файл
        with open("catalog_dict.json", "w", encoding='UTF-8') as file:
            json.dump(dict_results, file, indent=1, ensure_ascii=False)
        # нажимаем кнопку каталог перед следующей итерацией цикла
        driver.find_element('xpath', xpath_catalog).click()
        time.sleep(3)
