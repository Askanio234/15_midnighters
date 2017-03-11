from datetime import datetime
import requests
from pytz import timezone
import pytz

DEVMAN_API = "https://devman.org/api/challenges/solution_attempts/"

MIN_TIME = 0

MAX_TIME = 6


def get_number_of_pages(api):
    request = requests.get(api)
    request.encoding = "utf-8"
    result = request.json()
    return result["number_of_pages"]


def load_attempts(api, number_of_pages):
    attempts = []
    for page in range(1, number_of_pages+1):
        parameters = {"page": page}
        request = requests.get(api, params=parameters)
        request.encoding = "utf-8"
        result = request.json()
        attempts.extend(result["records"])
    return attempts


def convert_to_local_time(attempts):
    attempts_in_local_time = []
    for record in attempts:
        if record["timestamp"] is not None:
            user_time_zone = timezone(record["timezone"])
            user_local_time = user_time_zone.localize(datetime.fromtimestamp(
                                                        record["timestamp"]))
            attempts_in_local_time.append({"username": record["username"],
                                            "time": user_local_time})
    return attempts_in_local_time


def get_midnighters(attempts_in_local_time):
    midnighters = set()
    for record in attempts_in_local_time:
        if MIN_TIME <= record["time"].time().hour <= MAX_TIME:
            midnighters.add(record["username"])
    return midnighters


def print_midnighters(midnighters):
    print("Совы на девмане:\n")
    for midnighter in midnighters:
        print("{}".format(midnighter))


if __name__ == '__main__':
    number_of_pages = get_number_of_pages(DEVMAN_API)
    attempts = load_attempts(DEVMAN_API, number_of_pages)
    local_time_attempts = convert_to_local_time(attempts)
    midnighters = get_midnighters(local_time_attempts)
    print_midnighters(midnighters)
