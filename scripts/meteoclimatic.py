#! /usr/bin/python

# Copyright (c) 2013-2017 Ardexa Pty Ltd
#
# This code is licensed under the MIT License (MIT).
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# Make sure that you install the module: 'sudo pip install BeautifulSoup4'
#

import urllib2
import sys
import time
import os
from Supporting import *
from bs4 import BeautifulSoup

PIDFILE = 'ardexa-meteoclimatic'
WEBSITE = "meteoclimatic.net"

# COnvert symbols to numbers for wind direction
def convert_wind_dir(value):
	if (value == 'N'):
		return "0"
	elif (value == 'NNE'):
		return "23"
	elif (value == 'NE'):
		return "45"
	elif (value == 'ENE'):
		return "67"
	elif (value == 'E'):
		return "90"
	elif (value == 'ESE'):
		return "113"
	elif (value == 'SE'):
		return "135"
	elif (value == 'SSE'):
		return "158"
	elif (value == 'S'):
		return "180"
	elif (value == 'SSO'):
		return "203"
	elif (value == 'SO'):
		return "225"
	elif (value == 'OSO'):
		return "248"
	elif (value == 'O'):
		return "270"
	elif (value == 'ONO'):
		return "293"
	elif (value == 'NO'):
		return "315"
	elif (value == 'NNO'):
		return "338"
		

# Convert meteoclimatic.net values
def convert_values(raw_dict, station_id, station_name):
	radiation = ""
	temperature = ""
	humidity= ""
	pressure = ""
	rainfall = ""
	wind_speed = ""
	wind_direction = ""
	
	for key,value in raw_dict.iteritems():
		if (key.find("Radiac") != -1):
			radiation,rest = value.split()
		elif (key.find("Temperatura") != -1):
			temperature, rest = value.split()
		elif (key.find("Humedad") != -1):
			humidity ,rest = value.split()
		elif (key.find("Presi") != -1):
			pressure, rest = value.split()
		elif (key.find("Precip.") != -1):
			rainfall, rest = value.split()
		elif (key.find("Viento") != -1):
			wind_direction, wind_speed, rest = value.split()
			wind_direction = convert_wind_dir(wind_direction)	

	header = " #datetime, website, station ID, station name, temperature (C), humidity (%), Wind Speed (km/h), Wind Direction (degs mag), Pressure (hPa),Solar (W/m^2), Daily Precipitation (mm)\n"
	line = get_datetime() + "," + WEBSITE + "," + station_id + "," + station_name + "," + temperature + "," + humidity + "," + wind_speed + "," + wind_direction \
			  + "," + pressure + "," + radiation + "," + rainfall + "\n"

	return header, line



#~~~~~~~~~~~~~~~~~~  End Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Check script is run as root
if os.geteuid() != 0:
	print "You need to have root privileges to run this script, or as \'sudo\'. Exiting."
	sys.exit(2)

# Check the arguments
arguments = check_args(4)
if (len(arguments) < 4):
	print "The arguments cannot be empty. Usage: ", USAGE
	sys.exit(3)

station_id = arguments[1]
station_name = arguments[2]
log_directory = arguments[3]
debug_str = arguments[4]

# Convert debug
retval, debug = convert_to_int(debug_str)
if (not retval):
	print "Debug needs to be an integer number. Value entered: ",debug_str
	sys.exit(3)

# If the logging directory doesn't exist, create it
if (not os.path.exists(log_directory)):
	os.makedirs(log_directory)

# Check that no other scripts are running
pidfile = os.path.join(log_directory, PIDFILE) + station_id + ".pid"
if check_pidfile(pidfile, debug):
	print "This script is already running"
	sys.exit(7)

# if any args are empty, exit with error
if ((not station_id) or (not station_name)):
	print "The arguments cannot be empty. Usage: ", USAGE
	sys.exit(8)

start_time = time.time()

# Open the URL
url = "https://www.meteoclimatic.net/perfil/" + station_id 
html = urllib2.urlopen(url)

# Parse the html using beautiful soap
page = BeautifulSoup(html, 'html.parser')


# Find the values
titles = page.findAll('td', attrs={'class': 'titolet'})
data = page.findAll('td', attrs={'class': 'dadesactuals'})

# Make sure both arrays are equal in size  
if (len(titles) != len(data)):
	exit(1)

raw_dict = {}
idx = 0
for title_raw in titles:	
	title = title_raw.text.strip()
	item = data[idx].text.strip()
	raw_dict[title] = item
	idx += 1

header, line = convert_values(raw_dict, station_id, station_name)

if (debug > 0):
	print "Header: ", header, " Line: ", line

# Write the log entry, as a date entry in the log directory
date_str = (time.strftime("%d-%b-%Y"))
log_filename = date_str + ".csv"
log_directory = os.path.join(log_directory, station_id)
write_log(log_directory, log_filename, header, line, debug, True, log_directory, "latest.csv")


elapsed_time = time.time() - start_time
if (debug > 0):
	print "This request took: ",elapsed_time, " seconds."

# Remove the PID file	
if os.path.isfile(pidfile):
	os.unlink(pidfile)

exit(0)






