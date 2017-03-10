#!/bin/sh

while true
do
 node /home/pi/Downloads/polly_poc/getNewClips.js >> /home/pi/logs/clips.log
 sleep 5
done
