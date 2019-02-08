#!./env/bin/python3

import os
import re
#import requests
from urllib.request import urlopen
from urllib.parse import urlencode 
import json
import argparse
from dotenv import load_dotenv


def main():
    tool = WeatherTool()

    # if user provide a city
    if tool.city:
        city = tool.city
    elif os.getenv("city"):
        city = os.getenv("city")
    else:
        print("getting location")
        city = tool.get_location()
        tool.save_to_file("city", city)

    # if user provide his own apikey
    if tool.key:
        key = tool.key
        tool.save_to_file("key", key)
    elif os.getenv("key"):
        key = os.getenv("key")
    else:
        #free api key for general use
        key = "57720d9a6c316db99681b89f9302a6d1"

    result = tool.get_weather(city, key)
    tool.format_text(result)


class WeatherTool:
    def __init__(self, greeting="Thank you for using our tool :)"):
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

        self.args = parser.parse_args()
        self.key = self.args.key
        self.save = self.args.save
        city = self.args.city
        # if user enter Multi-Word city
        self.city = "+".join(city) if type(city) is list else city

        if self.city and self.save:
            self.save_to_file("city", self.city)

    def get_weather(self, query, key, func=urlopen):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={key}"
        with func(url) as res:
            json_data = json.loads(res.read())
        properties_from_api = ("name", "weather", "main", "speed")
        return {
            key: json_data[key] for key in json_data if key in properties_from_api
        }
    
    # find out why this function gets called first or is just compile time
    #def get_location(self, func=requests.get):
        #r = func("https://ipinfo.io").json() or {"city": "none"}
        #return r["city"]
    def get_location(self, func=urlopen):
        with func("https://ipinfo.io") as res:
            return json.loads(res.read())["city"] or {"city": "none"}

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

    def format_text(self, results):
        # Name of city
        print(results["name"])
        # State and description of results
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
X 2. work on saving city
X 3. work on taking api keys
X 4. fix function  order bug 
"""
