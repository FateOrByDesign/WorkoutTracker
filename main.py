import os
import requests_cache
from dotenv import load_dotenv

load_dotenv()

NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY")
NUTRITION_APP_ID = os.getenv("NUTRITION_APP_ID")

if NUTRITION_APP_ID is None : raise ValueError("NUTRITION_APP_ID didn't load properly.")
if NUTRITION_API_KEY is None : raise ValueError("NUTRITION_API_KEY didn't load properly.")

# create a cache for API
session = requests_cache.CachedSession("API_cache", expire_after=360*10)

# NUTRITION_API_CONSTANTS
NUTRITION_API_ENDPOINT = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
NUTRITION_API_HEADERS = {
    "x-app-id": NUTRITION_APP_ID,
    "x-app-key": NUTRITION_API_KEY,
}
NUTRITION_API_QUERY_PARMS = {
    "weight_kg": 86.5,
    "height_cm": 170,
    "age": 21,
    "gender": "male",
}

def main():
    # get the user to type the workouts
    workout_input = input("Tell me which exercises you did followed by a comma (ex: ran 2k, rode bike 1 hour): ").split(",")
    exercises = []
    # for each workout the user entered call the API to get the info
    for workout in workout_input:
        exercise = recognize_workout_from_api(workout)
        exercises.append(exercise)
    print(exercises)


def recognize_workout_from_api(workout_text: str)->tuple:
    """From the given text extract the workout name, duration and calories"""
    nutrition_api_parms = NUTRITION_API_QUERY_PARMS.copy()
    nutrition_api_parms["query"] = workout_text
    response = session.post(NUTRITION_API_ENDPOINT, json=nutrition_api_parms, headers=NUTRITION_API_HEADERS)
    response.raise_for_status()
    workout_data = response.json()["exercises"][0]
    return workout_data["name"], workout_data["duration_min"], workout_data["nf_calories"]

main()