import os
import requests_cache
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY")
NUTRITION_APP_ID = os.getenv("NUTRITION_APP_ID")
SHEETY_AUTHORIZATION = os.getenv("SHEETY_AUTHORIZATION")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")

if not NUTRITION_APP_ID: raise ValueError("NUTRITION_APP_ID didn't load properly.")
if not NUTRITION_API_KEY: raise ValueError("NUTRITION_API_KEY didn't load properly.")
if not SHEETY_AUTHORIZATION: raise ValueError("SHEETY_AUTHORIZATION didn't load properly.")
if not SHEETY_ENDPOINT: raise ValueError("SHEETY_ENDPOINT didn't load properly")

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

# SHEETY_API_CONSTANTS
SHEETY_API_ENDPOINT = SHEETY_ENDPOINT
SHEETY_HEADER = {"Authorization" : f"Bearer {SHEETY_AUTHORIZATION}"}

def main():
    # get the user to type the workouts
    workout_input = input("Tell me which exercises you did followed by a comma (ex: ran 2k, rode bike 1 hour): ").split(",")
    # for each workout the user entered call the API to get the info and log it
    for workout in workout_input:
        exercise = recognize_workout_from_api(workout)
        logging_workouts_to_sheets(exercise[0].capitalize(), exercise[1], exercise[2])



def recognize_workout_from_api(workout_text: str)->tuple:
    """From the given text extract the workout name, duration and calories"""
    nutrition_api_parms = NUTRITION_API_QUERY_PARMS.copy()
    nutrition_api_parms["query"] = workout_text
    response = session.post(NUTRITION_API_ENDPOINT, json=nutrition_api_parms, headers=NUTRITION_API_HEADERS)
    response.raise_for_status()
    workout_data = response.json()["exercises"][0]
    return workout_data["name"], workout_data["duration_min"], workout_data["nf_calories"]

def logging_workouts_to_sheets(exercise, duration, calories):
    """Add each workout to the sheet"""
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%X")
    payload_for_sheety = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories, }
    }
    response = session.post(SHEETY_API_ENDPOINT, headers=SHEETY_HEADER, json=payload_for_sheety)
    response.raise_for_status()
    print(response.json())
main()