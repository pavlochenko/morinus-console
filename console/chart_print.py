#!/usr/bin/env python
import sys, os
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/usr/local/lib/python3.11/site-packages')

import astrology
import chart
import csv
import houses
import pickle
import planets
import pprint
import options
import transits
import pickle
import util
import time
import transits
from inspect import getmembers
from pprint import pprint
from printr import printr
from sys import exit
import pandas as pd
import swisseph

swisseph.set_ephe_path('F:/fintwit/ephe')

def printPlanetsData(chrt):
    out = []
    print(chrt.name)
    print("%d-%d-%d %d:%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day, chrt.time.hour, chrt.time.minute))
    outList = {}

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        decl = chrt.planets.planets[j].dataEqu[1]
        #riseset = chrt.riseset.planetRiseSet(j)
        outList[ chrt.planets.planets[j].name]  =  [lon, lat, speed, decl]

    # ASC / MC positions
    ASC = chrt.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON], chrt.houses.ascmc2[houses.Houses.ASC][houses.Houses.LAT], chrt.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]
    outList['ASC'] =  [ ASC[0], ASC[1],ASC[2],0]
    out.append("%.2f\t%.2f\t%.2f\t%.3f\t" % (ASC[0], ASC[1], ASC[2], 0))
    MC = chrt.houses.ascmc2[houses.Houses.MC][houses.Houses.LON], chrt.houses.ascmc2[houses.Houses.MC][houses.Houses.LAT], chrt.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]
    outList['MC'] =  [ MC[0], MC[1],  MC[2], 0]
    print (pd.DataFrame.from_dict(outList, orient='index', columns=['lon', 'lat', 'speed', 'decl']))

opts = options.Options()
opts.def_hsys = opts.hsys = 'S'
opts.def_ayanamsha = opts.ayanamsha = 1

# Headers
print ("""Symbol\tDate\t \
    "SULON\tSULAT\tSUDEC\tSUSP\t" \
    "MOLON\tMOLAT\tMODEC\tMOSP\t" \
    "MELON\tMELAT\tMEDEC\tMESP\t" \
    "VELON\tVELAT\tVEDEC\tVESP\t" \
    "MALON\tMALAT\tMADEC\tMASP\t" \
    "JULON\tJULAT\tJUDEC\tJUSP\t" \
    "SALON\tSALAT\tSADEC\tSASP\t" \
    "URLON\tURLAT\tURDEC\tURSP\t" \
    "NELON\tNELAT\tNEDEC\tNESP\t" \
    "PLLON\tPLLAT\tPLDEC\tPLSP\t" \
    "NNLON\tNNLAT\tNNDEC\tNNSP\t" \
    "SNLON\tSNLAT\tSNDEC\tSNSP\t" \
    "ASLON\tASLAT\tASDEC\tASSP\t" \
    "MCLON\tMCLAT\tMCDEC\tMCSP\t""")


with open('F:/morinus-console/Hors/birthdates.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, )
    for row in reader:
        # Need to import for each iteration or it brokes
        import time
        if row['Symbol'] == 'NIKHIL':    
            dt = time.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
            # place, time and chart generation
            ny_place = chart.Place('New York', 74, 0, 21, False, 40, 42, 51, True, 10)
            jaipur_place = chart.Place('Jaipur', 75, 48, 0 , True, 26, 54, 0, True, 10)
            year, month, day, hour, minute, second = dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec
            zone_hour, zone_minute, zone_second = util.decToDeg(float(row['ZH']))
            symbol = row['Symbol']
            time = chart.event.DateTime(year, month, day, hour, minute, second, False, astrology.SE_JUL_CAL, chart.event.DateTime.ZONE, False, zone_hour, 0, False, ny_place)
            chrt = chart.Chart(symbol, False, time, jaipur_place, opts.hsys, 'notes', opts)
            # Print chart positions
            printPlanetsData(chrt)
            print("#"*10 , sep="\n")
