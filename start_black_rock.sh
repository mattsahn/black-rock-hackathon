#!/bin/sh

cd /home/pi/dev/black-rock
sudo python rock.py > /home/pi/logs/rock.log 2>&1


#while true
#do
# node /home/pi/Downloads/polly_poc/getNewClips.js >> /home/pi/logs/clips.log
# node /home/pi/Downloads/polly_poc/playClipFromWeb.js >> /home/pi/logs/clips2.log
# sleep 15
#done
