#!./env/bin/python3

import sys
import requests
import argparse

parser = argparse.ArgumentParser(
    prog="Weather-tool", description="Display weather results in your area")

# positional arg city. positional means required without a flag
parser.add_argument("city", help="get weather for spescified city", type=str)

# Optional arg. if not passed, By default = False
parser.add_argument(
    "-s", "--save", help="save your city for next time", action="store_true")

# parse arguments
args = parser.parse_args()

city = args.city
save = args.save
# for testing
key = "57720d9a6c316db99681b89f9302a6d1"


def getWeather(city, key=key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    r = requests.get(url)
    json = r.json()
    # print(json)
    # parse data to python dict
    for item in json:
        print(f"{item} =>{json[item]}")
    # Return what's needed from data


def main():
    getWeather(city)


if __name__ == "__main__":
    main()
