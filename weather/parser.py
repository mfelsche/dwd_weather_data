from data import Parsers
import sys
import argparse
import json
from data import TemperatureHumilityParser, RainFallParser, WindParser, SunshineParser, EarthGroundParser


def parse(download_dirs, station_id):
    with open(station_id + ".json", "w") as json_file:
        print("writing to", json_file.name)
        for row in Parsers.parse(station_id, download_dirs):
            json_file.write(json.dumps(row))
            json_file.write("\n")
    print("done")


def main():
    parser = argparse.ArgumentParser(description="Parse Weather data")
    parser.add_argument("--temp-download-dir", dest="temp_dir", type=str, default="downloads/temp")
    parser.add_argument("--sunshine-download-dir", dest="sun_dir", type=str, default="downloads/sunshine")
    parser.add_argument("--rainfall-download-dir", dest="rain_dir", type=str, default="downloads/rainfall")
    parser.add_argument("--wind-download-dir", dest="wind_dir", type=str, default="downloads/wind")
    parser.add_argument("--earth-download-dir", dest="earth_dir", type=str, default="downloads/earth_ground")
    parser.add_argument("-s", "--station-id", dest="station_id", type=str)
    args = parser.parse_args(sys.argv[1:])
    parse({
        TemperatureHumilityParser.NAME: args.temp_dir,
        RainFallParser.NAME: args.rain_dir,
        WindParser.NAME: args.wind_dir,
        SunshineParser.NAME: args.sun_dir,
        EarthGroundParser.NAME: args.earth_dir
    }, args.station_id)
