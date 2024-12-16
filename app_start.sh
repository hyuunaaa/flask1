#!/bin/bash

APP_NAME="Flask App"
APP_SCRIPT="./src/app.py"
LOG_FILE="flask_app.log"
PID_FILE="flask_app.pid"

# Check if the app is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "$APP_NAME is already running with PID $PID"
        exit 1
    else
        echo "Stale PID file found. Removing it..."
        rm -f "$PID_FILE"
    fi
fi

# Start the app
echo "Starting $APP_NAME..."
nohup python $APP_SCRIPT > $LOG_FILE 2>&1 & echo $! > $PID_FILE
echo "$APP_NAME started with PID $(cat $PID_FILE)"
