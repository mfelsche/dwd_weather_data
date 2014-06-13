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
from __future__ import print_function
from .base import DWDDataSourceParser
import csv
import time


class EarthGroundParser(DWDDataSourceParser):
    NAME = "earth_ground"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def parse_data(self, infile, metadata):
        with open(infile, 'r') as data:
            reader = csv.reader(data, delimiter=',')
            _header = reader.next()
            i = 0
            for row in reader:
                i += 1
                try:
                     if len(row) > 12 and filter(None, row):
                        date = self.get_date(row[1])
                        ground_temp = [
                            float(row[3]),  # 2cm depth
                            float(row[5]),  # 5 cm depth
                            float(row[7]),  # 10 cm depth
                            float(row[9]),  # 20 cm depth
                            float(row[11])  # 50 cm depth
                        ]
                        yield {
                            "date": int(1000*time.mktime(date.timetuple())),
                            "station_id": metadata['id'],
                            "station_name": metadata['name'],
                            "station_lat": metadata["lat"],
                            "station_lon": metadata["lon"],
                            "station_height": metadata["height"],
                            "ground_temp": ground_temp  # temperatures in °C
                        }
                except Exception as e:
                    print("row %d: %s" % (i, row))
                    print(e)
