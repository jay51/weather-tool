#!./env/bin/python3

import os
import re
import time
import requests
import argparse
from dotenv import load_dotenv


class WeatherTool:
    def __init__(self, greeting="Thank you for using our tool :)"):
        print(greeting)
        parser = argparse.ArgumentParser(
            prog="Weather-tool", description="Display weather results in your area")

        # positional arg city. positional means required without a flag
        parser.add_argument(
            "city", help="get weather for spescified city", type=str, nargs="*")

        # Optional arg. defaults to False
        parser.add_argument(
            "-s", "--save", help="save your city for next time useage by default", action="store_true")

        # nargs == Number of arguments for one action.
        # defaults to none else you pass a --key flag and an api key (--key apikey)
        parser.add_argument(
            "--key", help="save your own openweathermap api key", type=str)

        self.args = parser.parse_args()
        self.key = self.args.key
        self.save = self.args.save
        city = self.args.city
        self.city = "+".join(city) if type(city) is list else city

        if self.city and self.save:
            self.save_to_file("city", self.city)

    def get_weather(self, query, key, func=requests.get):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={key}"
        r = func(url)
        json = r.json()
        return {
            key: json[key] for key in json if key == "name" or key == "weather" or key == "main" or key == "speed"
        }

    def get_location(self, func=requests.get):
        r = func("https://ipinfo.io").json() or {"city": "none"}
        return r["city"]

    def save_to_file(self, item, value):
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
            self.save_to_file(item, value)

    def formate_text(self, results):
        # Name of city
        print(results["name"])
        # State and description of results
        print(
            f'{results["weather"][0]["main"]} ,{results["weather"][0]["description"]}')
        # # Temp and humidity and pressure
        for item in results["main"]:
            print(f"{item} {results['main'][item]}")


def main():
    tool = WeatherTool()
    if tool.city:
        city = tool.city
    elif os.getenv("city"):
        city = os.getenv("city")
    else:
        print("getting location")
        city = tool.get_location()
        tool.save_to_file("city", city)

    if tool.key:
        key = tool.key
        tool.save_to_file("key", key)
    elif os.getenv("key"):
        key = os.getenv("key")
    else:
        key = "57720d9a6c316db99681b89f9302a6d1"

    result = tool.get_weather(city, key)
    tool.formate_text(result)


if __name__ == "__main__":
    load_dotenv()
    main()


"""Todo
1. work on caching http requests
X 2. work on saving city
X 3. work on taking api keys
X 4. make argpars arguments in a function because it runs befor load_dotenv() gets called
"""
