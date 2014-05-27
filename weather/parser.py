import csv
import sys
import argparse


def parse(infile):
    reader = csv.reader(infile, delimiter=',')
    header = reader.next()


def main():
    parser = argparse.ArgumentParser(description="Parse Weather data")
    parser.add_argument('infile', type=file)
    args = parser.parse_args(sys.argv[1:])
    parse(args.infile)
    args.infile.close()
