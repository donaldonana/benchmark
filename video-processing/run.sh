#!/bin/bash
 
VIDEO="1Mb.avi"
IPV4="172.20.20.78"
LIBRARY=("moviepy" "ffmpeg" "imageio" "opencv")
 
mkdir -p "result/energy/energy/$VIDEO"

for LIB in "${LIBRARY[@]}"; do

  echo -e "$LIB"
  ENERGY_FILE="result/energy/energy/$VIDEO/$LIB$VIDEO.txt"  

  for (( i = 1; i <= 100; i++ )); do

    # Launch cpu-energy-meter in background and save its PID
    cpu-energy-meter -r >> "$ENERGY_FILE" &
    METER_PID=$!

    wsk action invoke proc -r \
        --param bib  "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$VIDEO" >> result/energy/result.txt

    kill -SIGINT "$METER_PID"

    echo -e "$i"

    sleep 2
      
  done

done
