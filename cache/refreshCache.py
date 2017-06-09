#coding=utf-8

# Download the google spreadsheet as a CSV using CURL
# Convert the CSV file to a JSON variable, which I can call using <script>

# requires CURL and Python
import csv
import json
import os
import string
import subprocess
import datetime

onlyFutureResults = False


# set the URL that we want to update from
remoteURL = "https://docs.google.com/spreadsheets/d/1E78Wo-wL9RtJcoc-8Cuwy7wVN_FJVRAf_GlxKkVifJk/export?gid=0&format=csv"
# set the paths for the local files
base = os.path.split(__file__)[0]
csvPath = os.path.join(base, 'cache.csv')
jsonPath = os.path.join(base, 'cache.json')

# if we already aren't in the working directory, let's go there
if base:
    os.chdir(base)

# use the subprocess module to run CURL from the command line
proc = subprocess.Popen(['curl', remoteURL, '-o', 'cache.csv'], stdout=subprocess.PIPE)
out = proc.communicate()[0]

# get two file objects, one to read from and one to write to
csvfile = open(csvPath, 'r')
jsonfile = open(jsonPath, 'w')

# determine the field names by reading the first line of csv and splitting it by a comma
# we need the fieldnames in order to read the CSV
#fieldnames = tuple(string.strip(csvfile.readlines()[0]).split(','))

# recreate the CSV file, I don't know why
csvfile = open(os.path.join(base, 'cache.csv'), 'r')

fieldnames = ('Name', 'Category', 'Organization', 'Date', 'End Date', 'Time', 'Location', 'Description', 'URL', 'Emily: \xf0\x9f\x91\x8d')

# read the CSV, loop through it, and dump the JSON for each row
reader = csv.DictReader(csvfile, fieldnames)

# we are actually not making a json file, but a javascript variable
# it's a little hacky but it's easy, it works, and doesn't require jquery, so...

jsonfile.write('var data = [')
i = 0

now = datetime.datetime.now() - datetime.timedelta(days=1)

skipped = 0
for row in reader:
    # don't write the first row because it is just the table headers
    i += 1
    if i == 1:
        continue

    d = datetime.datetime.strptime(row['Date'], "%a, %b %d, %Y")    
    #print d <= now, d, now, row['Name'][:10]
    if d <= now and onlyFutureResults:
        skipped += 1
        continue
    
    json.dump(row, jsonfile)
    jsonfile.write(',\n')

jsonfile.write('];')

print 'Updated cache for ' + str(i) + ' rows, and skipped ' + str(skipped) + ' past events.'