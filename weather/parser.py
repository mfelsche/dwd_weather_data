import argparse

def parse(infile):


def main():
    parser = argparse.ArgumentParser(description="Parse Weather data")
    parser.add_argument('infile', type=file('r'))
    args = parser.parse_args(sys.argv[1:])
    parse(args.infile)
    args.infile.close()
