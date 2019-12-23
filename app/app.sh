#!/bin/bash

PROJDIR="/data/python/fastor/app"
PIDFILE="$PROJDIR/app.fastor.pid"
ERRORLOG="/data/logs/cms_app_error.log"
OUTLOG="/data/logs/cms_app_std_out.log"
APP_EXEC="/data/python2.7/bin/python manage.py runfcgi method=prefork daemonize=true host=127.0.0.1"
NUM_PROC=16000
NUM_PROCS=8
MIN_SPARE=50
MAX_SPARE=100

cd $PROJDIR


function start_server() {
    cd $PROJDIR
    ulimit -n 65535
    $APP_EXEC port=$NUM_PROC minspare=$MIN_SPARE maxspare=$MAX_SPARE maxchildren=$NUM_PROCS  outlog=$OUTLOG errlog=$ERRORLOG
}

function stop_server() {
    ps aux | grep "$APP_EXEC" | grep "$NUM_PROC" | awk '{print $2}' | xargs kill -9
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
    echo 'Usage: app.sh [start|stop|restart]'
esac



