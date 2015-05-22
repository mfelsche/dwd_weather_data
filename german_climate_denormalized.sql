CREATE TABLE german_climate_denormalized (
  date timestamp,
  station_id string,
  station_name string,
  position geo_point, -- position of the weather station
  station_height int, -- height of the weather station
  temp float, -- temperature in °C
  humility double, -- relative humulity in percent
  cloudiness int,  -- 0 (cloudless)
                   -- 1 or less (nearly cloudless)
                   -- 2 (less cloudy)
                   -- 3
                   -- 4 (cloudy)
                   -- 5
                   -- 6 (more cloudy)
                   -- 7 or more (nearly overcast)
                   -- 8 (overcast)
                   -- -1 not availavle
  rainfall_fallen boolean, -- if some precipitation happened this hour
  rainfall_height double,  -- precipitation height in mm
  rainfall_form int, -- 0 - no precipiation
                     -- 1 - only "distinct" (german: "abgesetzte") precipitation
                     -- 2 - only liquid "distinct" precipitation
                     -- 3 - only solud "distinct" precipitation
                     -- 6 - liquid
                     -- 7 - solid
                     -- 8 - solid and liquid
                     -- 9 - no measurement
  air_pressure double,  -- air pressure (Pa)
  air_pressure_station_height double, -- air pressure at station height (Pa)
  ground_temp array(float), -- soil temperature in °C at 2cm, 5cm, 10cm, 20cm and 50cm depth
  sunshine_duration double, -- sum of sunshine duration in that hour in minutes
  diffuse_sky_radiation double, -- sum of diffuse short-wave sky-radiation in J/cm² for that hour
  global_radiation double, -- sum of global short-wave radiation in J/cm² for that hour
  sun_zenith float, -- sun zenith in degree
  wind_speed double, -- wind speed in m/sec
  wind_direction int -- wind direction given in 36-part land-spout
) clustered by (station_id) with (number_of_replicas=0, refresh_interval=0);
