# -*- coding: utf-8; -*-
#
# Licensed to CRATE Technology GmbH ("Crate") under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  Crate licenses
# this file to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
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

from .base import DWDDataSourceParser


class SolarRadiationParser(DWDDataSourceParser):
    NAME = "solar"

    def get_name(cls):
        return cls.NAME

    def extract_data(self, row):
        return {
            "sunshine_duration": self.get_float(row[3]),  # Stundensumme der Sonnenscheindauer in minutes
            "diffuse_sky_radiation": self.get_float(row[4]),  # Stundensumme der kurzwelligen diffusen Himmelsstrahlung in J/cm²
            "global_radiation": self.get_float(row[5]),  # Stundensumme der kurzwelligen Globalstrahlung in J/cm²,
            "sun_zenith": self.get_float(row[7])  # Sonnenzenit
        }

    def expected_columns(self):
        return 8
