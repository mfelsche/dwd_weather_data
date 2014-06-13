from weather import is_dir, FullPaths
import argparse
import sys
import os
import os.path
import traceback
import urllib3
import logging
from six.moves.urllib import parse as urlparse

logger = logging.getLogger(__name__)

TYPES = ["rainfall", "ground", "temperature", "wind", "sunshine"]

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "etc"))


def download(types, output_dir):
    if "all" in types:
        download_all(output_dir)
    elif types:
        for source_type in types:
            logger.info("downloading {0} sources...".format(source_type))
            source_download_dir = os.path.join(output_dir, source_type)
            if not os.path.exists(source_download_dir):
                os.makedirs(source_download_dir)
            source_link_list_file = os.path.join(CONFIG_DIR, "{0}.txt".format(source_type))
            if not os.path.exists(source_link_list_file):
                raise FileNotFoundError(source_link_list_file)
            download_from_file(source_link_list_file, source_download_dir)
            logger.info("done.")
    else:
        logger.info("nothing to download")


def download_all(output_dir):
    for source_type in TYPES:
        logger.info("downloading {0} sources...".format(source_type))
        source_download_dir = os.path.join(output_dir, source_type)
        source_link_list_file = os.path.join(CONFIG_DIR,
                                             "{0}.txt".format(source_type))
        if not os.path.exists(source_link_list_file):
            raise FileNotFoundError(source_link_list_file)
        else:
            download_from_file(source_link_list_file, source_download_dir)
        logger.info("done.")


def download_from_file(link_list_file, output_dir):
    conn = None
    with open(link_list_file, 'r') as links_file:
        for link_line in links_file.readlines():
            link = link_line.strip()
            filename = os.path.join(output_dir, link.split('/')[-1])
            if not filename.endswith('.zip'):
                filename += '.zip'

            if not os.path.isfile(filename):
                if conn is None:
                    conn = urllib3.connection_from_url(link)
                path = urlparse.urlparse(link).path
                response = conn.request('GET', path,
                                        headers={'Accept': '*/*',
                                                 'Accept-Encoding': 'gzip, deflate',
                                                 'User-Agent': 'crate-weather/0.0.1'},
                                        timeout=10)
                if response.status >= 400:
                    logger.error("error accessing {0}: {1}".format(link, response.data))
                else:
                    with open(filename, 'wb') as output:
                        for data in response.stream():
                            output.write(data)
                    response.release_conn()
                    logger.info("downloaded {0}".format(os.path.basename(filename)))
            else:
                logger.info("{0} already downloaded".format(os.path.basename(filename)))


def main():
    parser = argparse.ArgumentParser(description="Download data")
    parser.add_argument('types', type=str, action='append', help="""The type of data sources to download.

options are:

 * rainfall
 * ground
 * temperature
 * wind
 * sunshine
 * all (all of the above)
""", choices=TYPES + ["all"])
    parser.add_argument('--download-dir', dest="download_dir", action=FullPaths,
                        type=is_dir, help="the directory to download the data sources into",
                        default=os.path.join(os.path.dirname(__file__), "..", "downloads"))
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
            level=logging.DEBUG)
    try:
        download(args.types, args.download_dir)
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

