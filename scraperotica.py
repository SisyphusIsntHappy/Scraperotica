#!/bin/python
import sys
from story import *
from author import *
from get_story import *

url_sample = "https://www.literotica.com/s/"

if ( url_sample in sys.argv[1]):
    get_story(sys.argv[1])

elif (int(sys.argv[1])):
    get_everything(sys.argv[1])

else:
    print("Give a valid input - author uid or the stoy link")
