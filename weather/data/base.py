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

from zipfile import ZipFile
import datetime


class DWDDataSourceParser(object):
    """
    base class for parsing DWD sources
    """

    METADATA_CACHE = {}

    def __init__(self, downloaddir):
        self.downloaddir = downloaddir

    def get_metadata(self, station_id):
        return self.METADATA_CACHE.get(station_id)

    def parse_metadata(self, infile):
        with open(infile, 'r') as md_file:
            _header = md_file.readline()
            row = [elem.strip() for elem in md_file.readline().split(";") if elem]
            if row:
                metadata = {
                    "id": row[0],
                    "height": int(row[1]),
                    "lat": float(row[2]),
                    "lon": float(row[3]),
                    "name": unicode(row[6].strip(), "iso8859")
                }
                self.METADATA_CACHE[metadata["id"]] = metadata
                return metadata
            else:
                return {}

    def open_zip(self, infile):
        zip = ZipFile(infile, 'r')
        metadata = None
        data_file = None
        for efile in zip.namelist():
            if efile.startswith('Stationsmetadaten'):
                print("metadata:", efile)
                zip.extract(efile)
                metadata = efile
            if efile.startswith('produkt'):
                print("data:", efile)
                zip.extract(efile)
                data_file = efile
        return metadata, data_file

    def get_date(self, val):
        return datetime.datetime(year=int(val[0:4], 10), month=int(val[4:6], 10), day=int(val[6:8], 10), hour=int(val[8:10], 10))

    def get_name(self):
        return "base"

    def parse(self, station_id):
        raise NotImplementedError()

    def parse_data(self, infile):
        raise NotImplementedError()
