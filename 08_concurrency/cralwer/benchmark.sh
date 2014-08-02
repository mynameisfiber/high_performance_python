#!/bin/bash

ulimit -n 2048

(python server.py --port=8080 &> /dev/null) &
server_pid=$!
sleep 1 # wait for server to be ready

for i in gevent grequests tornado tornado_callback serial
    do 
        pushd $i
        python crawler.py
        popd
done

pushd asyncio
OLD_PYTHONPATH=$PYTHONPATH
unset PYTHONPATH
python3 crawler.py
export PYTHONPATH=$OLD_PYTHONPATH
popd

curl "localhost:8080/add?flush=True"
kill $server_pid

mkdir images
python visualize.py
