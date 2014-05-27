import argparse
import re
import sys
import urllib2
import os.path


def parse(infile):
    data = infile.read()
    match = re.findall(r'href=[\'"]?([^\'" >]+)', data)
    links = [m for m in match if 'klimadaten/german/download/Stundenwerte' in m]
    print "Found {0} links".format(len(links))
    for link in links:
        filename = 'downloads/rainfall/' + link.split('/')[-1] + '.zip'
        if not os.path.isfile(filename):
            print "Downloading {0}".format(link)
            data = urllib2.urlopen(link)
            with open(filename, 'wb') as output:
                output.write(data.read())
        else:
            print "File already downloaded"


def main():
    parser = argparse.ArgumentParser(description="Download data")
    parser.add_argument('infile', type=file)
    args = parser.parse_args(sys.argv[1:])
    parse(args.infile)
    args.infile.close()
