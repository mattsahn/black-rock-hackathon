#!/bin/sh

cd /home/pi/Downloads/polly_poc/
while true
do
 /home/pi/.nvm/versions/node/v6.10.0/bin/node /home/pi/Downloads/polly_poc/getNewClips.js >> /home/pi/logs/clips.log
 sleep 5
done
