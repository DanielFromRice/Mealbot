from requests_html import HTMLSession
from bs4 import BeautifulSoup
from FoodInfo import MealTimeInfo, DailyFoodInfo, FoodItemInfo, ServeryDiningInfo
from jsonpickle import encode


SOUTH = "SOUTH"
NORTH = "NORTH"
WEST = "WEST"
BAKER = "BAKER"
SEIBEL = "SEIBEL"

_SOUTH_URL = "https://dining.rice.edu/south-servery/full-week-menu"
_NORTH_URL = "https://dining.rice.edu/north-servery/full-week-menu"
_WEST_URL = "https://dining.rice.edu/west-servery/full-week-menu"
_BAKER_URL = "https://dining.rice.edu/baker-servery/full-week-menu"
_SEIBEL_URL = "https://dining.rice.edu/seibel-servery/full-week-menu"

SERVERY_LIST = {SOUTH: _SOUTH_URL, NORTH: _NORTH_URL, WEST: _WEST_URL, BAKER: _BAKER_URL, SEIBEL: _SEIBEL_URL}

class MealDataScraper():
    """
    Class to abstract away extraction of food information from the servery.
    Simply instantiate an instance of the class and call the start method. Results will then be available using the
    get_food_information method, returning a list of MealTimeInfo objects
    """
    def __init__(self, servery):
        self.page = SERVERY_LIST[servery]
        self.session = HTMLSession()
        self.response = None
        self.hasBeenStarted = False
        self.servery_information = ServeryDiningInfo(servery)

    def start(self):
        """
        Starts the Data Scraper. Must be called to begin extraction
        :return:
        """
        self.hasBeenStarted = True
        self.response = self.session.get(self.page)
        self.response.html.render()
        self._parse_food_from_webpage()

        self.write_json()

    def _parse_food_from_webpage(self):
        """
        Entry level function to begin food extraction from the webpage specified
        :return:
        """
        raw_food_items = self._get_raw_food_information_html()
        self._process_raw_food_information(raw_food_items)

    def _get_raw_food_information_html(self):
        """
        Pulls raw html data fro the dining page
        :return: A mapping from the string meal time to a list of html tags containing food information
        """
        #Renders the Javascript
        soup = BeautifulSoup(self.response.html.raw_html, 'html.parser')
        meal_times = soup.find_all("div", {"class": "menu-scaffold"})

        rawInformation = {}

        for meal_time in meal_times:
            #Extract meal time
            meal_time_name_candidate = meal_time.find_all('span', class_ = 'meal-time')
            if meal_time_name_candidate:
                #Breakfast, lunch or dinner
                meal_time_name = meal_time_name_candidate[0].text

                #Map meal time to associated meal items
                rawInformation[meal_time_name] = meal_time.find_all('div', class_="item")

        return rawInformation

    def _process_raw_food_information(self, raw_food_items):
        """
        Processes the raw food information mapping into usable MealTimeInfo data
        :param raw_food_items:
        :return:
        """
        processed_food = []
        for meal_time, raw_daily_food_items in raw_food_items.items():
            meal_info = MealTimeInfo()
            meal_info.time_of_day = meal_time
            for raw_daily_food_item in raw_daily_food_items:
                daily_food_info = self._process_raw_food_item(raw_daily_food_item)
                if daily_food_info:
                    meal_info.daily_food_data.append(daily_food_info)

            self.servery_information.meals.append(meal_info)



    def _process_raw_food_item(self, raw_food):
        """
        Processes a tag containing information about food for a particular day of the week into a structured
        FoodInfo object
        :param raw_food: Tag containing food data
        :return: A FoodInfo object or None if errors
        """
        daily_food_info = DailyFoodInfo()
        day_candidates = raw_food.find_all('div', class_="title")

        #If no day exists return None
        if not day_candidates:
            return None
        daily_food_info.day = day_candidates[0].text

        #Extract the food information
        for food_tag in raw_food.find_all('div', class_="mitem"):
            if food_tag.text != "" and food_tag.text != "\n":
                item = FoodItemInfo(food_tag.text)
                daily_food_info.food_items.append(item)

        return daily_food_info

    def get_food_information(self):
        if not self.hasBeenStarted:
            print("ERROR: Attempting to obtain food info without starting the parser")
            return []
        return self.servery_information

    def write_json(self):
        results = encode(self.get_food_information())
        print(results)


