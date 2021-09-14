from json import JSONEncoder

class ServeryDiningInfo(JSONEncoder):
    """
    Top level object holding structured information regarding information scraped from the servery
    """
    def __init__(self, servery):
        self.servery = servery
        self.meals = []

class MealTimeInfo(JSONEncoder):
    def __init__(self):
        self.daily_food_data = []
        self.time_of_day = None

    def __str__(self):
        header = "Meal information for {0}".format(self.time_of_day)
        details = ""

        for food_data in self.daily_food_data:
            details += str(food_data)
        return header + "\n" + details

class DailyFoodInfo(JSONEncoder):
    def __init__(self):
        self.day = None
        self.food_items = []
    def __str__(self):
        result = "Food info for Day: {0}\n".format(self.day)
        for item in self.food_items:
            result += str(item)
            result += "\n"
        return result

class FoodItemInfo(JSONEncoder):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
