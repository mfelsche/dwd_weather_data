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

from temp_humility import TemperatureHumilityParser
from sunshine_duration import SunshineParser
from rainfall import RainFallParser
from wind import WindParser


class Parsers(object):
    parsers = [
        TemperatureHumilityParser,
        RainFallParser,
        WindParser,
        SunshineParser
    ]

    @classmethod
    def parse(cls, station_id, download_dirs):
        data = {}
        for parser_class in cls.parsers:
            parser = parser_class(download_dirs[parser_class.get_name()])
            for datum in parser.parse(station_id):
                value = data.setdefault(datum["date"], {})
                value.update(datum)

        for value in data.values():
            yield value

