
import sys
import traceback
import logging
import argparse
import json
from data import Parsers
from weather import FullPaths, is_dir


def parse(download_dir, station_id=None):
    with open(station_id + ".json", "w") as json_file:
        print("writing to", json_file.name)
        for row in Parsers.parse(station_id, download_dir):
            json_file.write(json.dumps(row))
            json_file.write("\n")
    print("done")


def main():
    parser = argparse.ArgumentParser(description="Parse Weather data")
    parser.add_argument("--download-dir", dest="download_dir", action=FullPaths,
                        type=is_dir, help="the directory the data sources were downloaded into",
                        default=os.path.join(os.path.dirname(__file__), "..", "downloads"))
    parser.add_argument("-s", "--station-id", dest="station_id", type=str)
    parser.add_argument('-d', '--debug', dest="debug", action="store_true")
    args = parser.parse_args(sys.argv[1:])
    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
            format='[%(levelname)s %(asctime)s] %(message)s',
            datefmt='%Y/%m/%d %H:%M:%S',
            stream=sys.stdout,
            level=level)
    try:
        parse(args.download_dir, args.station_id)
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
