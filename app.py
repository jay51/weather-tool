#!./env/bin/python3

import os
import re
import time
import requests
import argparse
from dotenv import load_dotenv
#load_dotenv()
#value = os.getenv("key")


parser = argparse.ArgumentParser(
    prog="Weather-tool", description="Display weather results in your area")

# positional arg city. positional means required without a flag
parser.add_argument(
    "city", help="get weather for spescified city", type=str, nargs="*", default="San Antonio")

# Optional arg. defaults to False
parser.add_argument(
    "-s", "--save", help="save your city for next time", action="store_true")

# nargs == Number of arguments for one action.
# defaults to none else you pass a --key flag and an api key (--key apikey)
parser.add_argument(
    "--key", help="openweathermap api key", type=str, nargs=1)


# parse arguments
args = parser.parse_args()

city = args.city
save = args.save
# for testing
key = "57720d9a6c316db99681b89f9302a6d1"
local_time = time.localtime(time.time())
# print(local_time.tm_hour)


print(args.key)
print(args.city)
print(args.save)


def getWeather(query, key=key):
    if type(query) is list:
        query = "+".join(city)
    #units= imerial for F and units=metric for C and no units will result in kelvins
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={key}"
    r = requests.get(url)
    # parse data to python dict
    json = r.json()
    # Return what's needed from data
    return {
        key: json[key] for key in json if key == "name" or key == "weather" or key == "main" or key == "speed"
    }



def save_to_file(item, value):
    #save item to .env file with key=value formate
    with open(".env") as f:
       copy =  f.read()
       copy = re.sub(f"{item}.*", f"{item}={value}", copy)
        
    with open(".env", "w") as f:
      f.write(copy) 
        





def main():
    weather = getWeather(city)
    #Name of city
    print(weather["name"])
    #State and description of weather
    print(f'{weather["weather"][0]["main"]} ,{weather["weather"][0]["description"]}')
    #Temp and humidity and pressure
    for item in weather["main"]:
        print(f"{item} {weather['main'][item]}")


if __name__ == "__main__":
    main()


"""Todo
1. work on caching http requests
2. work on saving city
3. work on taking api keys 
"""
