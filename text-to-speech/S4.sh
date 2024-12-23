
#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1
UPDATE=$2
PREWARM=$3
RUN=$4

# docker pull  $IMAGE
if [ "$UPDATE" == "1" ]; then
  ./S2.sh $IPV4 1 0 0 
  wsk action update validation  validation/__main__.py  
  wsk action update S4 --sequence validation,demo/text2speech,demo/conversion
fi

if [ "$PREWARM" == "1" ]; then
  wsk action invoke S4 -r \
    --param ipv4 $IPV4 \
    --param text "1Ko.txt" \
    --param schema "S4"
fi

if [ "$RUN" == "1" ]; then

  TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt")
  mkdir -p "result/energy/S4/" 

  for TEXT in "${TEXTES[@]}"; do

    echo -e "$TEXT" 

    for (( i = 1; i <= 2; i++ )); do

      cpu-energy-meter -r >> "result/energy/S4/$TEXT" &
      METER_PID=$!
      wsk action invoke S4 -r \
        --param ipv4 "$IPV4" \
        --param schema "S4" \
        --param text "$TEXT" >> "result/result.txt" 
      kill -SIGINT $METER_PID

      echo -e "$i"
      sleep 6
    done
  done
fi
    
