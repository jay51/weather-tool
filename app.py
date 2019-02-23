#!env/bin/python3

import os
import re
from urllib.request import urlopen, URLError
import json
import argparse
from dotenv import load_dotenv


def main():
    if(not check_internet()):
        print("No Internet connection detected")
        return 

    args = init_argparse()
    city = args.city
    key = args.key

    # if user provide a city
    if city:
        city = "+".join(city) if type(city) is list else city
        # if user pass save flag
        if args.save:
            save_to_file("city", city)

    elif os.getenv("city"):
        city = os.getenv("city")
    else:
        print("getting location")
        city = get_location()
        save_to_file("city", city)

    # if user provide his own apikey
    if key:
        save_to_file("key", key)
    elif os.getenv("key"):
        key = os.getenv("key")
    else:
        #free api key for general use
        key = "57720d9a6c316db99681b89f9302a6d1"

    result = get_weather(city, key)
    format_text(result)




def init_argparse(greeting="Thank you for using our tool :)"):
    print(greeting)
    parser = argparse.ArgumentParser(
        prog="Weather-tool", description="Display weather results in your area")

    # positional arg city. positional means required without a flag
    parser.add_argument(
        "city", help="get weather for spescified city", type=str, nargs="*")

    # optional arg. defaults to False
    parser.add_argument(
        "-s", "--save", help="save your city for next time useage by default", action="store_true")

    # defaults to none else you pass a --key flag and an api key (--key apikey)
    parser.add_argument(
        "--key", help="save your own openweathermap api key", type=str)

    return parser.parse_args()


def check_internet():
    try:
        urlopen("https://google.com", timeout=5)
        return True
    except URLError as err:
        return False


def get_weather(query, key, func=urlopen):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={key}"
    with func(url) as res:
        json_data = json.loads(res.read())
    properties_from_api = ("name", "weather", "main")
    return {
        key: json_data[key] for key in json_data if key in properties_from_api
    }

    
def get_location(func=urlopen):
    with func("https://ipinfo.io") as res:
        return json.loads(res.read())["city"] or {"city": "none"}


def save_to_file(item, value):
    print("saving to File")
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

def format_text(results):
    # Name of city
    print(results["name"])
    # State and description 
    print(
        f'{results["weather"][0]["main"]} ,{results["weather"][0]["description"]}')
    # Temp and humidity and pressure
    for item in results["main"]:
        print(f"{item} {results['main'][item]}")


if __name__ == "__main__":
    load_dotenv()
    main()


"""Todo
1. work on caching http requests
"""
