#!./env/bin/python3

import sys
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







