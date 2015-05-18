CREATE TABLE german_weather_denormed (
  station_id string,
  station_name string,
  position geo_point, -- position of the weather station
  station_height int, -- height of the weather station
  temp double, -- temperature in °C
  humility double, -- relative humulity in percent
  cloudiness int, -- 0 -- 0 (wolkenlos)
                       -- 1 oder weniger (fast wolkenlos)
                       -- 2 (leicht bewölkt)
                       -- 3
                       -- 4 (wolkig)
                       -- 5
                       -- 6 (stark bewölkt)
                       -- 7 oder mehr (fast bedeckt)
                       -- 8 (bedeckt)
                       -- 9 Himmel nicht erkennbar
  rainfall_fallen boolean, -- if some precipitation happened this hour
  rainfall_height double,  -- precipitation height in mm
  rainfall_form int, -- TODO: find out coding with http://www.met.fu-berlin.de/~stefan/fm12.html
  air_pressure double,  -- air pressure (Pa)
  air_pressure_station_height double, -- air pressure at station height (Pa)
  ground_temp array(double), -- soil temperature in °C at 2cm, 5cm, 10cm, 20cm and 50cm depth
  sunshine_duration double, -- sum of sunshine duration in that hour in minutes
  diffuse_sky_radiation double, -- sum of diffuse short-wave sky-radiation in J/cm² for that hour
  global_radiation double, -- sum of global short-wave radiation in J/cm² for that hour
  sun_zenith float, -- sun zenith in TODO
  wind_speed double, -- wind speec in m/sec
  wind_direction int -- wind direction given in 36-part land-spout
) clustered by (station_id) with (number_of_replicas=0, refresh_interval=0)
