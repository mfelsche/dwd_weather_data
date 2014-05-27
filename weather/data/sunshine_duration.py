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

from base import DWDDataSourceParser
import csv
import time


class SunshineParser(DWDDataSourceParser):

    NAME = "sun"

    @classmethod
    def get_name(cls):
        return cls.NAME

    def parse_data(self, data_file, metadata):
        data = open(data_file, 'r')
        try:
            reader = csv.reader(data, delimiter=',')
            _header = reader.next()
            i = 0
            for row in reader:
                i+=1
                try:
                    if len(row) > 6 and filter(None, row):
                        date = self.get_date(row[1])
                        sunshine_hours = float(row[5])
                        yield {
                            "date": int(1000*time.mktime(date.timetuple())),
                            "station_id": metadata['id'],
                            "station_name": metadata['name'],
                            "station_lat": metadata["lat"],
                            "station_lon": metadata["lon"],
                            "station_height": metadata["height"],
                            "sunshine_hours": sunshine_hours
                        }
                except Exception as e:
                    print "row %d: %s" % (i, row)
                    print e
        finally:
            data.close()
