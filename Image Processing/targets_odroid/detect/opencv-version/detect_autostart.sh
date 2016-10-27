#!/bin/bash

CAM_ID="04b4:00f9"

## back up old data in SD card before running 
EXE_PATH="/home/odroid/detect/opencv-version"
SD_PATH="/media/odroid/4EAB-16EF"

## back-up previous results locally run before starting
BK_FILE_NAME="`date +"%Y-%m-%d-%H%M%S"`_frame_with_target.tar"
#mv ${EXE_PATH}/try.avi ${EXE_PATH}/frame_with_target
tar czf ${SD_PATH}/frame_with_target/${BK_FILE_NAME} ${EXE_PATH}/frame_with_target/* --remove-files


## find GPS port
echo "[`date`]looking for GPS module" | tee -a /home/odroid/video_detect.log
while [ 0 ]
do
  if [ -e /dev/ttyACM0 ]
  then
    echo "[`date`]   found GPS module"  | tee -a /home/odroid/video_detect.log
    break
  else
    echo "[`date`]    waiting..."
    sleep 1
  fi
done

## find camera
echo "[`date`]looking for camera module"  | tee -a /home/odroid/video_detect.log
while [ 0 ]
do
  CAM_FIND=$(lsusb | grep -c ${CAM_ID})
  if [ ${CAM_FIND} -eq 1 ]
  then
    echo "[`date`]   found GPS module"  | tee -a /home/odroid/video_detect.log
    break
  else
    echo "[`date`]    waiting..."
    sleep 1
  fi
done

## find internet connection
echo "[`date`]waiting for internet connection"  | tee -a /home/odroid/video_detect.log
while [ 0 ]
do
  /usr/bin/wget -q --spider http://google.com
  if [ $? -eq 0 ]
  then
    echo "[`date`]    Connected...!"   | tee -a /home/odroid/video_detect.log
    break
  else
    echo "[`date`]    Not connected..."   | tee -a /home/odroid/video_detect.log
  fi
  sleep 3
done


## start program
echo "[`date`]starting GPS daemon"  | tee -a /home/odroid/video_detect.log
/usr/sbin/gpsd /dev/ttyACM0
echo "[`date`]starting video stream detection program"  | tee -a /home/odroid/video_detect.log
screen -m -d -S screen_detect '/home/odroid/detect/opencv-version/detect_script.sh' > /home/odroid/video.log 2>&1

