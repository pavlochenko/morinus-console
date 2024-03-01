#!/usr/bin/env python3

GCHART_DESTINATION_PATH = '/tmp'

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append('/usr/local/lib/python3.11/site-packages')

import os
import swisseph
import astrology
import chart
import csv
import houses
import mtexts
import options
import options
import pickle
import planets
import sys
import time
import transits
import util
# from inspect import getmembers
# import pprint
# from sys import exit

swisseph.set_ephe_path('F:/fintwit/ephe')

def printPlanetsData(chrt):
    out = []
    out.append("%s\t" % (chrt.name))
    out.append("%d-%d-%d %d:%d\t" % (chrt.time.year, chrt.time.month, chrt.time.day, chrt.time.hour, chrt.time.minute))

    for j in range (planets.Planets.PLANETS_NUM):
        lon = chrt.planets.planets[j].data[planets.Planet.LONG]
        lat = chrt.planets.planets[j].data[planets.Planet.LAT]
        speed = chrt.planets.planets[j].data[planets.Planet.SPLON]
        decl = chrt.planets.planets[j].dataEqu[1]
        #riseset = chrt.riseset.planetRiseSet(j)
        out.append("%.2f\t%.2f\t%.2f\t%.3f\t" % (lon, lat, decl, speed))

    # ASC / MC positions
    # Houses positions
    for j in range (0, 12):
        lon = chrt.houses.cusps[j]
        #out.append("%.2f\t" % (lon))

    sys.stdout.write(''.join(out))

opts = options.Options()
mtexts.setLang(opts.langid)
opts.def_hsys = opts.hsys = 'S'

# Headers
print("Name\tDate\t" \
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
    "H1\tH2\tH3\tH4\tH5\tH6\tH7\tH8\tH9\tH10\tH11\tH12\tFILE")

# Need to import for each iteration or it brokes
import time
chart_name = sys.argv[1]
bdate = sys.argv[2]
btime = sys.argv[3]
lat = sys.argv[4]
lon = sys.argv[5]
tz = sys.argv[6]
dt = time.strptime(bdate + ' ' + btime, '%Y-%m-%d %H:%M')
north = True
east = True
altitude = 0

#long
idx = lon.find(u'E')#
if idx == -1:
  idx = lon.find(u'W')#
  east = False

if idx == -1:
  print("Invalid lon string provided")
  sys.exit()
else:
  deglon = int(lon[0:idx])
  idx += 1
  degmin = int(lon[idx:])

#lat
idx = lat.find(u'N')#
if idx == -1:
  idx = lat.find(u'S')#
  north = False

if idx == -1:
  print("Invalid lat string provided")
  sys.exit()
else:
  latdeg = int(lat[0:idx])
  idx += 1
  latmin = int(lat[idx:])

# place, time and chart generation
place = chart.Place('Place Name', deglon, degmin, 0, east, latdeg, latmin, 0, north, altitude)
year, month, day, hour, minute, second = dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec
#place.tz
tzh, tzm, tzs = util.decToDeg(float(tz))
if tz[0] == '-':
  tzplus = False
else:
  tzplus = True

time = chart.event.DateTime(year, month, day, hour, minute, second, False, astrology.SE_JUL_CAL, chart.event.DateTime.ZONE, tzplus, tzh, tzm, False, place)
chrt = chart.Chart(chart_name, False, time, place, opts.hsys, 'notes', opts)
# Print chart positions
print(printPlanetsData(chrt))
