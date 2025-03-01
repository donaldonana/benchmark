#!/bin/bash

IPV4="172.20.20.77"
IMAGES=("100Kb.JPEG" "500b.JPEG" "1Mb.JPEG" "15Mb.JPEG" "256Kb.JPEG")
LIBRARY=("pillow" "wand" "pygame" "opencv")


for IMAGE in "${IMAGES[@]}"; do
  echo -e "$IMAGE"
  mkdir -p "result/results/energy/$IMAGE" 

  for LIB in "${LIBRARY[@]}"; do
    echo -e "$LIB"
    ENERGY_FILE="result/results/energy/$IMAGE/$LIB$IMAGE.txt"  

    for (( i = 1; i <= 100; i++ )); do
      # Launch cpu-energy-meter in background and save its PID
      cpu-energy-meter -r >> "$ENERGY_FILE" &
      METER_PID=$!
        
      wsk action invoke thumb -r \
        --param bib  "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$IMAGE" >> result/results/result.txt

      kill -SIGINT "$METER_PID"

      echo -e "$i"

      sleep 4
    done

    sleep 4

  done

done

 

