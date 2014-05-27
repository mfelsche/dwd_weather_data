for f in $`ls downloads/temperature | awk  -F '_' '{sub(/-.*$/, "", $2); print $2}'` 
do 
    bin/parse_data -s $f --temp-download-dir downloads/temperature
done
