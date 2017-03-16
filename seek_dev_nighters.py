from datetime import datetime
import requests
from pytz import timezone
import pytz

DEVMAN_API = "https://devman.org/api/challenges/solution_attempts/"

MIN_TIME = 0

MAX_TIME = 6


def send_request(api, parameters):
    request = requests.get(api, params=parameters)
    request.encoding = "utf-8"
    return request.json()


def load_attempts(api):
    attempts = []
    result = send_request(api, None)
    attempts.extend(result["records"])
    number_of_pages = result["number_of_pages"]
    for page in range(1, number_of_pages+1):
        parameters = {"page": page}
        result = send_request(api, parameters)
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


def is_midnighter(MIN_TIME, MAX_TIME, record):
    return bool(MIN_TIME <= record["time"].time().hour <= MAX_TIME)


def get_midnighters(attempts_in_local_time):
    midnighters = [record["username"]
                    for record in attempts_in_local_time
                    if is_midnighter]
    return set(midnighters)


def print_midnighters(midnighters):
    print("Совы на девмане:\n")
    for midnighter in midnighters:
        print("{}".format(midnighter))


if __name__ == '__main__':
    attempts = load_attempts(DEVMAN_API)
    local_time_attempts = convert_to_local_time(attempts)
    midnighters = get_midnighters(local_time_attempts)
    print_midnighters(midnighters)
