#!/bin/sh

sleep 30 
kill -9 $(ps -ef | grep -i streaming.py | awk '{print $2}')
