from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import datetime

weekday_dict = {0: "MONDAY", 1: "TUESDAY", 2: "WEDNESDAY", 3: "THURSDAY", 4: "FRIDAY", 5: "SATURDAY", 6: "SUNDAY"}
urls = {"south": 'https://dining.rice.edu/south-servery/full-week-menu',
        "seibel": 'https://dining.rice.edu/seibel-servery/full-week-menu',
        "north": None, "west": None, "baker": None}


def get_raw_text():
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    response = driver.get('https://dining.rice.edu/south-servery/full-week-menu')
    food_results = driver.find_elements_by_class_name('html-scaffold-body')
    return food_results
    # print(results[0].text)
    # print('---------------------')
    # print(results[1].text)


def get_weekday():
    weekd_num = datetime.date.today().weekday()
    weekday = weekday_dict[weekd_num]
    return weekday


def print_food(results, desired_weekday):
    message = ""
    lunchtext = results[0].text.split('\n') # CAN I ASSUME LUNCH COMES FIRST
    message = message + "LUNCH: \n"
    current = False
    for line in lunchtext:
        if current:
            if line in weekday_dict.values():
                current = False
            else:
                message = message + line + '\n'
        else:
            if line == desired_weekday:
                current = True
    dinnertext = results[1].text.split('\n')
    message = message + "DINNER: \n"
    current = False
    for line in dinnertext:
        if current:
            if line in weekday_dict.values():
                current = False
            else:
                message = message + line + "\n"
        else:
            if line == weekday:
                current = True
    print(message)

food_results = get_raw_text()
weekday = get_weekday()
print_food(food_results, weekday)