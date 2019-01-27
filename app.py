#!./env/bin/python3

import os
import re
import time
import requests
import argparse
from dotenv import load_dotenv


def init_arg_parser():
    parser = argparse.ArgumentParser(
        prog="Weather-tool", description="Display weather results in your area")

    # positional arg city. positional means required without a flag
    parser.add_argument(
        "city", help="get weather for spescified city", type=str, nargs="*", default=city)

    # Optional arg. defaults to False
    parser.add_argument(
        "-s", "--save", help="save your city for next time useage by default", action="store_true")

    # nargs == Number of arguments for one action.
    # defaults to none else you pass a --key flag and an api key (--key apikey)
    parser.add_argument(
        "--key", help="save your own openweathermap api key", type=str)

    # parse arguments
    return parser.parse_args()


# local_time = time.localtime(time.time())
# print(local_time.tm_hour)

def getWeather(query, key):
    # units= imeprial for F and units=metric for C and no units will result in kelvins
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={key}"
    r = requests.get(url)
    # parse data to python dict
    json = r.json()
    # Return what's needed from data
    return {
        key: json[key] for key in json if key == "name" or key == "weather" or key == "main" or key == "speed"
    }


def get_location():
    r = requests.get("https://ipinfo.io")
    if r.status_code == 200:
        return r.json()["city"]


def save_to_file(item, value):
    # save item to .env file with key=value formate
    print("saving to file")
    try:
        with open(".env") as f:
            copy = f.read()

        if item in copy:
            copy = re.sub(f"{item}.*", f"{item}={value}", copy)
            with open(".env", "w") as f:
                f.write(copy)
        else:
            with open(".env", "a") as f:
                f.write(f"\n{item}={value}")

    except FileNotFoundError:
        print("making .env file")
        with open(".env", "w") as f:
            pass
        save_to_file(item, value)


def main():
    args = init_arg_parser()
    key = args.key
    save = args.save
    city = "+".join(args.city) if type(args.city) is list else args.city
    print("++++++++++")
#    print(key)
#    print(city)
#    print(save)
    print("++++++++++")

    weather = getWeather(city, _key)
    # save key if key is passed
    if key:
        save_to_file("key", key)
    # save city if city passed
    if city and save:
        save_to_file("city", city)

    # Name of city
    print(weather["name"])
    # State and description of weather
    print(
        f'{weather["weather"][0]["main"]} ,{weather["weather"][0]["description"]}')
    # # Temp and humidity and pressure
    for item in weather["main"]:
        print(f"{item} {weather['main'][item]}")


if __name__ == "__main__":
    load_dotenv()
    _key = os.getenv("key") if os.getenv(
        "key") else "57720d9a6c316db99681b89f9302a6d1"
    print(_key)
    city = os.getenv("city") if os.getenv("city") else get_location()
    main()


"""Todo
1. work on caching http requests
X 2. work on saving city
X 3. work on taking api keys
X 4. make argpars arguments in a function because it runs befor load_dotenv() gets called
"""
