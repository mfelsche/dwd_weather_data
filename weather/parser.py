from data import Parsers
import sys
import argparse
import json


def parse(temp_download_dir, station_id):

    download_dirs = {
        "temp": temp_download_dir
    }
    with open(station_id + ".json", "w") as json_file:
        print("writing to", json_file.name)
        for row in Parsers.parse(station_id, download_dirs):
            json_file.write(json.dumps(row))
            json_file.write("\n")
    print("done")


def main():
    parser = argparse.ArgumentParser(description="Parse Weather data")
    parser.add_argument("--temp-download-dir", dest="temp_dir", type=str, default="downloads/temp")
    parser.add_argument("-s", "--station-id", dest="station_id", type=str)
    args = parser.parse_args(sys.argv[1:])
    parse(args.temp_dir, args.station_id)
