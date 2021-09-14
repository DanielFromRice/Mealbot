import json
import jsonpickle
from mealdata_seleniumless import MealDataScraper, SOUTH, SEIBEL


def test_scraping_South_Servery():
    print("TESTING SCRAPE OF SOUTH")
    print("---------------------------")
    try:
        servery_scraper = MealDataScraper(SEIBEL)
        servery_scraper.start()
        servery_info = servery_scraper.get_food_information()

        for info in servery_info.meals:
            print(str(info))

    except Exception as e:
        print("Test Failed")
        print(e)
        return
    print("----------------------------")
    print("TEST SUCCESSFUL")

def main():
    test_scraping_South_Servery()

main()

