#!/bin/bash

APP_NAME="Flask App"
PID_FILE="flask_app.pid"

# Check if the app is running
if [ ! -f "$PID_FILE" ]; then
    echo "$APP_NAME is not running (no PID file found)."
    exit 1
fi

PID=$(cat "$PID_FILE")
if ps -p $PID > /dev/null; then
    echo "Stopping $APP_NAME with PID $PID..."
    kill $PID
    rm -f "$PID_FILE"
    echo "$APP_NAME stopped."
else
    echo "PID $PID not found. Cleaning up..."
    rm -f "$PID_FILE"
fi
