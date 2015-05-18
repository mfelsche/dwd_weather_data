# -*- coding: utf-8; -*-
#
# Licensed to CRATE Technology GmbH ("Crate") under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  Crate licenses
# this file to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
# However, if you have executed another commercial license agreement
# with Crate these terms will supersede the license and you may use the
# software solely pursuant to the terms of the relevant commercial agreement.

from zipfile import ZipFile, BadZipfile
import datetime
import time
import os
import glob
import csv
import logging
logger = logging.getLogger(__name__)


class DWDDataSourceParser(object):
    """
    base class for parsing DWD sources
    """
    RECENT = "recent"
    HISTORICAL = "historical"

    METADATA_CACHE = {}

    def __init__(self, download_dir, work_dir, include_metadata=True):
        self.download_dir = download_dir
        self.workdir = os.path.join(work_dir, self.get_name())
        self.include_metadata = include_metadata

    def get_metadata(self, station_id):
        return self.METADATA_CACHE.get(station_id)

    def parse_metadata(self, infile):
        with open(infile, 'r', encoding='iso8859') as md_file:
            _header = md_file.readline()
            row = [elem.strip() for elem in md_file.readline().split(";") if elem]
            if row:
                metadata = {
                    "id": row[0],
                    "height": int(row[1] or 0),
                    "lat": float(row[2]),
                    "lon": float(row[3]),
                    "name": row[6].strip()
                }
                self.METADATA_CACHE[metadata["id"]] = metadata
                return metadata
            else:
                return {}

    def parse(self, station_id):
        f = None
        glob_matches = glob.glob(os.path.join(
            self.download_dir,
            self.get_name(),
            "stundenwerte_*_{}*.zip".format(station_id))
        )
        if not glob_matches:
            logger.debug("could not find file for station %s in dir '%s'" % (station_id, os.path.join(self.download_dir, self.get_name())))
            return []

        metadata_file, data_files = self.open_zip(glob_matches)
        metadata = self.get_metadata(station_id)
        if metadata is None:
            try:
                metadata = self.parse_metadata(metadata_file)
            finally:
                os.unlink(metadata_file)
        return self.parse_data(data_files, metadata)

    def open_zip(self, infiles):
        metadata_extracted = False
        metadata = None
        data_files = []
        for infile in infiles:
            try:
                zip = ZipFile(infile, 'r')
                for efile in zip.namelist():
                    if not metadata_extracted and efile.startswith('Stationsmetadaten'):

                        zip.extract(efile, path=self.workdir)
                        metadata = os.path.join(self.workdir, efile)
                        metadata_extracted = True
                        logger.debug("metadata: %s", metadata)
                    if efile.startswith('produkt'):

                        zip.extract(efile, path=self.workdir)
                        data_files.append(
                            os.path.join(self.workdir, efile)
                        )
                        logger.debug("data: %s", os.path.join(self.workdir, efile))
            except BadZipfile as e:
                logger.error("could not open: {}".format(infile))
                raise e
        return metadata, data_files

    @staticmethod
    def get_date(val):
        return datetime.datetime(year=int(val[0:4], 10), month=int(val[4:6], 10), day=int(val[6:8], 10), hour=int(val[8:10], 10))

    @staticmethod
    def get_float(val):
        fval = float(val)
        if fval == -999:
            return None
        return fval

    @staticmethod
    def get_int(val):
        ival = int(val)
        if ival == -999:
            return None
        return ival

    @classmethod
    def get_name(cls):
        return "base"

    def parse_data(self, infiles, metadata):
        for infile in infiles:
            try:
                with open(infile, 'r') as data:
                    reader = csv.reader(data, delimiter=';')
                    i = 0
                    header_skipped = False
                    for row in reader:
                        if not header_skipped:
                            header_skipped = True
                            continue
                        i += 1
                        try:
                            if len(row) >= self.expected_columns() and filter(None, row):
                                date = self.get_date(row[1])
                                data = self.extract_data(row)
                                data["date"] = int(1000*time.mktime(date.timetuple()))
                                if self.include_metadata:
                                    data.update({
                                        "station_id": metadata['id'],
                                        "station_name": metadata['name'],
                                        "position": [metadata["lon"], metadata["lat"]],
                                        "station_height": metadata["height"],
                                    })
                                yield data
                        except Exception as e:
                            logger.error("Error during {}, row {}: {}".format(self.get_name(), i, row))
                            logger.error(e)
                            yield {}
            finally:
                os.unlink(infile)

    def extract_data(self, row):
        raise NotImplementedError()

    def expected_columns(self):
        return 1000
