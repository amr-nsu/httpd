#!/bin/sh

cd ${0%/*}

python3 ../stream/stream.py &

../stream/video0.sh &

#python3 -m http.server --cgi 8000
python fhttpd.py > /tmp/fhttpd.log
