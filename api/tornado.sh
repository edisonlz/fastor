#!/bin/bash

APP_DIR=/data/python/fastor/api

APP_EXEC="/data/python2.7/bin/python main.py"

LOG_DIR=/data/logs/tornado/
LOG_LEVEL=error

WORKER_NUM=5
PORTS=(10000 10001 10002 10003)


function start_server() {
    cd $APP_DIR
    chmod +x main.py
    ulimit -n 65535
    for port in "${PORTS[@]}";
    do
        echo $port
        $APP_EXEC -port=$port -doc=Ture -worker=$WORKER_NUM -logging=$LOG_LEVEL -log_file_prefix=$LOG_DIR/$port.log &
    done
}

function stop_server() {
    for port in "${PORTS[@]}";
    do
        ps aux | grep "$APP_EXEC" | grep "$port" | awk '{print $2}' | xargs kill -9
    done
}


case "$1" in
start)
    start_server
;;
stop)
    stop_server
;;
restart)
    stop_server
    start_server
;;
*)
    echo 'Usage: bin/tornado.sh [start|stop|restart]'
esac


