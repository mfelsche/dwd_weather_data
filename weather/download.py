from weather import is_dir, FullPaths
import argparse
import re
import sys
import urllib2
import os.path


def parse(infile, output_dir):
    data = infile.read()
    match = re.findall(r'href=[\'"]?([^\'" >]+)', data)
    links = [m for m in match if 'klimadaten/german/download/Stundenwerte' in m and not 'akt' in m]
    print "Found {0} links".format(len(links))
    for link in links:
        filename = os.path.join(output_dir, link.split('/')[-1])
        if not filename.endswith('.zip'):
            filename = filename + '.zip'
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
    parser.add_argument('output', help="The output directory", action=FullPaths, type=is_dir)
    args = parser.parse_args(sys.argv[1:])
    parse(args.infile, args.output)
    args.infile.close()
