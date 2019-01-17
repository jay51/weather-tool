#!./env/bin/python3

import sys
import requests
import argparse

#print("arg", sys.argv)

parser = argparse.ArgumentParser(description="Display weather results in your area")
#positional arg city. positional means required without a flag 
parser.add_argument("city", help="get weather for spescified city", type=str)


#Optional arg. By default = None
parser.add_argument("-s", "--save", help="save your city for next time", action="store_true")

#parse arguments
args = parser.parse_args()

#get the arg with the name city
print(args.save)





url = "https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=" 
key = "57720d9a6c316db99681b89f9302a6d1"

def getWeather():
	#Request data from api
	#parse data to python dict
	#Return what's needed from data
