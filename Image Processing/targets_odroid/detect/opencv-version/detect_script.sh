
#!/bin/bash


EXE_PATH="/home/odroid/detect/opencv-version"
SD_PATH="/dev/mmcblk1"
SD_MOUNT_PATH=$EXE_PATH/sdcard

## back-up previous results locally run before starting
#BK_DIR_NAME="`date +"%Y-%m-%d-%H:%M:%S"`_frame_with_target"
#cp -r ${EXE_PATH}/frame_with_target  ${EXE_PATH}/${BK_DIR_NAME}
#mv ${EXE_PATH}/try.avi ${EXE_PATH}/${BK_DIR_NAME}
#rm ${EXE_PATH}/frame_with_target/*


## upload a txt file to dropbox to let user know we are ready
#echo "detection ready" | tee "/home/odroid/detect/opencv-version/frame_with_target/ready.txt"
#python /home/odroid/detect/dropbox/py-script/dropbox_sync.py ready.txt 

## start detection program
## absolute path is used, change accordingly!!
python ${EXE_PATH}/detect_stream.py

## if fail, loop forever
while [ 0 ]
do
  echo "failed"
  sleep 3
done
