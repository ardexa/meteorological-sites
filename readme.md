

# Purpose
The purpose of this project is to collect data from Meteorologial sites, and send it in real time to your cloud.

## How to use the script
On a raspberry Pi, or other Linux machines (arm, intel, mips or whetever), make sure Python is installed (which it should be). Then install the `BeautifulSoup4` dependancy as follows:
```
sudo pip install BeautifulSoup4
```

Then install and run it as follows:
```
cd
git clone https://github.com/ardexa/meteorological-sites.git
cd meteorological-sites
python meteoclimatic.py {STATION ID} {STATION NAME} {log directory} {debug type}  .... example: sudo python meteoclimatic.py ESAND1800000018110A spain-albolote /opt/data 0
```

## Meteorological Sites
The following sites are handled by these scripts:
```
meteoclimatic.net ... example: https://www.meteoclimatic.net/perfil/ESAND1800000018220A
```

## Collecting to the Ardexa cloud
Collecting to the Ardexa cloud is free for up to 3 Raspberry Pis (or equivalent). Ardexa provides free agents for ARM, Intel x86 and MIPS based processors. To collect the data to the Ardexa cloud do the following:
a. Create a `RUN` scenario to schedule the Ardexa Kaco script to run at regular intervals (say every 300 seconds/5 minutes).
b. Then use a `CAPTURE` scenario to collect the csv (comma separated) data from the filename `/opt/data/logs/`. This file contains a header entry (as the first line) that describes the CSV elements of the file.

## Help
Contact Ardexa at support@ardexa.com, and we'll do our best efforts to help.



