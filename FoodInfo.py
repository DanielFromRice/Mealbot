
class MealTimeInfo():
    def __init__(self):
        self.daily_food_data = []
        self.time_of_day = None
        self.servery_name = None

    def __str__(self):
        return "Meal information for {0}".format(self.time_of_day)

class DailyFoodInfo():
    def __init__(self):
        self.day = None
        self.food_items = []
    def __str__(self):
        result = "Food info for Day: {0}\n".format(self.day)
        for item in self.food_items:
            result += str(item)
            result += "\n"
        return result

class FoodItemInfo():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
