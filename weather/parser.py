import csv
import sys
import argparse
import datetime
from zipfile import ZipFile
from metadata import get_metadata
import json
import os

def get_date(val):
    return datetime.datetime(year=int(val[0:4], 10), month=int(val[4:6], 10), day=int(val[6:8], 10), hour=int(val[8:10], 10))

def parse(infile):
    metadata_file, data = open_zip(infile)

    with open(os.path.basename(infile.name) + ".json", "w") as json_file:
        print("writing to", json_file.name)
        with open(data, 'rb') as datafile:
            for row in parse_csv(metadata_file, datafile):
                json_file.write(json.dumps(row))
                json_file.write("\n")
        os.unlink(data) # deleting extracted datafile
    print("done")

def open_zip(infile):
    zip = ZipFile(infile, 'r')
    metadata = None
    data_file = None
    for efile in zip.namelist():
        if efile.startswith('Stationsmetadaten'):
            print("metadata:", efile)
            metadata = zip.open(efile, 'r')
        if efile.startswith('produkt'):
            print("data:", efile)
            zip.extract(efile)
            data_file = efile
    return metadata, data_file

def parse_csv(meta_infile, datafile):
    metadata = parse_metadata(meta_infile)
    return parse_data(datafile, metadata)


def parse_metadata(infile):
    infile.readline()
    header = infile.readline()
    row = [ row.strip() for row in infile.readline().split(";") ]
    return {
        "id": row[0],
        "height": int(row[1]),
        "lat": float(row[2]),
        "lon": float(row[3]),
        "name": unicode(row[6].strip(), "iso8859")
    }

def parse_data(infile, metadata):
    reader = csv.reader(infile, delimiter=',')
    header = reader.next()
    i = 0
    for row in reader:
        i+=1
        try:
            if row:
                id = row[0].strip()
                date = get_date(row[1])
                temp = float(row[5])
                rel_feuchte = float(row[6])
                yield {
                    "date": date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "station_id": metadata['id'],
                    "station_name": metadata['name'],
                    "station_location": [metadata["lat"], metadata["lon"]],
                    "station_height": metadata["height"],
                    "temp": temp,
                    "humility": rel_feuchte
                }
        except Exception as e:
            break
def main():
    parser = argparse.ArgumentParser(description="Parse Weather data")
    parser.add_argument('infile', type=file)
    args = parser.parse_args(sys.argv[1:])
    parse(args.infile)
    args.infile.close()
