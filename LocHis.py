import json
import pandas
from datetime import datetime
import csv
import webbrowser

"""
This programm clearns location data downloaded from google location
history.
It converts the database from json to csvfile
Also it computes the average location in a specified year
"""
file_path = '/Users/MEHRA/Documents/Notebooks/Takeout/Location History/Location History.json'
json_file = open(file_path)
gdic_zero = json.load(json_file)
json_file.close()
gdic_one = gdic_zero['locations']

# Cleaning up the records list
records = {}
ymonth = []
for i in range(len(gdic_one)):
    timestamp = gdic_one[i]['timestampMs'][:10]
    gooddate = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    shortdate =datetime.fromtimestamp(int(timestamp)).strftime('%Y') #-%m')
    ymonth.insert(i, shortdate)
    lon = gdic_one[i]['longitudeE7']/1e7
    lat = gdic_one[i]['latitudeE7']/1e7
    records[gooddate] = (lat,lon)

# Printing into csv file
with open('LocOutput.csv', 'w', newline='') as csvfile:
   record_writer = csv.writer(csvfile, delimiter=',',
                               quotechar = '"',
                               quoting=csv.QUOTE_MINIMAL)
   for rtime, rcoords in records.items():
       record_writer.writerow([rtime,rcoords[0], rcoords[1]])

#Finding the average location over the specified year
def average_loc(loc_dic, year):
    lonav, latav, count = 0,0,0
    for t_loc, loc in loc_dic.items():
        if int(t_loc[0:4]) == year:
            latav += float(loc[0])
            lonav += float(loc[1])
            count += 1
    coordav = (latav/count, lonav/count)
    print(coordav)
    print(count)
    return coordav

# Open URL in new window, locating the coords location.
def open_gmaps(coords):
    url = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(coords[0],coords[1])
    webbrowser.open_new(url)

my_av = average_loc(records, 2018)
open_gmaps(my_av)
