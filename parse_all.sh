for f in $`ls downloads/temperature | awk  -F '_' '{sub(/-.*$/, "", $2); print $2}'` 
do 
    bin/parse_data -s $f --temp-download-dir downloads/temperature --sunshine-download-dir downloads/sunshine_duration --wind-download-dir downloads/wind --rainfall-download-dir downloads/rainfall
done
