#!/usr/bin/env python

'''
Video Stream Processing

Processing the aerial stream from camera

Usage:
    stream_process.py  [source0] [source1] ...'

    sourceN is an
     - integer number for camera capture
     - leave none will treat the source as cam 1

Keys:
    ESC    - exit
    SPACE  - save current frame to <shot path> directory
    ENTER  - start image processing

'''
# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
from numpy import pi, sin, cos

import cv2, sys
from shutil import copyfile
# built-in modules
from time import clock

# local modules
from tst_scene_render import TestSceneRender
import common


presets = dict(
    chess = 'synth:class=chess:bg=../data/lena.jpg:noise=0.1:size=1920x1080',
)
#*****************************Parameter Setting***************************#
#Critial Setting
##Size Setting, in Pixels
CritialSizeMax=20
CritialSizeMin=2
CritialNum=10

ThreshRed=0.35
ThreshBlue=0.45

#Processing Parameters
FrameJumpNumber=20
SkipFlag=1
VideoRecordFlag=1
#*********************************Setting End*****************************#
#
save_img_quality = 100

## save image path
##   this path MUST EXIST before using!!! otherwise images cannot be saved
img_path = "./frame_with_target/"
GotTargetPath='./IGotTarget/'
exit_flag=0

## counting frames with target
max_target_digit = 8 # max  frames
target_frame_cnt = 0
frame_cnt = 0
SkipCount=1
SizeMax=CritialSizeMax*CritialSizeMax*3
SizeMin=CritialSizeMin*CritialSizeMin*3
if (VideoRecordFlag):
	video_name = "try.avi"
	fps = 24
	size = (1920,1080)
	videoWriter = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('P','I','M','1'), fps, size)
#
def create_capture(source = 1, fallback = presets['chess']):
    '''source: <int> or '<int>|<filename>|synth [:<param_name>=<value> [:...]]'
    '''
    source = str(source).strip()
    if source == None:
    	source = 1
    print('*****[Status:] Connecting Camera',source,'...*****'),
    chunks = source.split(':')
  
    source = chunks[0]
    try: source = int(source)
    except ValueError: pass
    params = dict( s.split('=') for s in chunks[1:] )
    
    cap = None
    if source == 'synth':
        Class = classes.get(params.get('class', None), VideoSynthBase)
        try: cap = Class(**params)
        except: pass
    else:
        cap = cv2.VideoCapture(source)
        if 'size' in params:
            w, h = map(int, params['size'].split('x'))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,h)
        else:
        	print('*****[Status:] Setting Camera Resolution...*****\r'),
        	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
        if fallback is not None:
            return create_capture(fallback, None)
    return cap

if __name__ == '__main__':
    import sys
    import getopt

    print(__doc__)

    args, sources = getopt.getopt(sys.argv[1:], '', 'shotdir=')
    args = dict(args)
    shotdir = args.get('--shotdir', '.')
    if len(sources) == 0:
        sources = [ 1 ]

    line='-'*80
    caps = list(map(create_capture, sources))
    shot_idx = 0
    ProcessFlag =0
    WaitFlag = 1
    StopTagetCopyCnt = 4
    cv2.namedWindow('frame',cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('frame',900,600)
    print('*****[Status:] Previewing the Stream... *****')
    while WaitFlag:
        imgs = []
        for i, cap in enumerate(caps):
            ret, img = cap.read()
            imgs.append(img)
            cv2.imshow('frame', img)
        ch = cv2.waitKey(1)
        if ch == 27:
            break
        if ch == 13:
        	ProcessFlag=1
        	WaitFlag =0
        	TargetFlag=0
        	print(line)
        	print('*****[Status:] Started Targets Detecting!*****')
        	

    #starting image processing	
	while (ProcessFlag):		
		found_red = 0
		found_blue = 0
		target_text = ""
	  	contour_red = []
	  	contour_blue = []

	  	ret,img1 =cap.read()

	  	ch = cv2.waitKey(1)
	  	if ch == 27:
	  		break
	  	if ch == ord(' '):
	  		TargetFlag=1
	  		StopTagetCopyCnt=1
	  		CopyIndex=str(target_frame_cnt).zfill(max_target_digit)
	  		dst=GotTargetPath+"target_frame_" + CopyIndex + ".jpg"
	  		cv2.imwrite(dst,img1)	
	  		print('\r',dst, 'saved')

	  	if (SkipFlag) and (SkipCount<FrameJumpNumber):
	  	 	SkipCount=SkipCount+1
	  	 	continue

	  	SkipCount=1;

	  	img1[550:600,260:320]=0
	  	img1[390:450,1560:1660]=0
	  	img=img1[150:930,230:1690]

	  	#img=img1[160:950,325:1560]

	 	if (VideoRecordFlag):
	 		videoWriter.write(img1)

	  	if not(ret):
	  	 	time.sleep(1)
	  	 	continue
  
	  	## convert to YCrCb, extract Y channel
	  	img_crcrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
	  	img_cr = img_crcrcb[:,:,1]

	  	## Y-axis max, min, mean
	  	cr_max = img_cr.max()
	  	cr_min = img_cr.min()
	  	cr_avg = img_cr.mean()

	  	## red
	 	if (cr_max - cr_avg)>30:
	  		thresh = cr_max - (cr_max - cr_avg)*ThreshRed
	  		img_cr_thresh_red = cv2.inRange(img_cr, thresh, 255)
	  		im2,contour_red, hier = cv2.findContours(img_cr_thresh_red.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	  		if len(contour_red)>0 and len(contour_red) < CritialNum:
	  			## reject contour if they are too large or too small
	  			for cnt in contour_red:
	  				area = cv2.contourArea(cnt)
	  				if area < SizeMax and area > SizeMin:
	  					found_red = 1
	  					M = cv2.moments(cnt)
	  					cx = int(M['m10']/M['m00'])
	  					cy = int(M['m01']/M['m00'])
	  					center = (cx, cy)
	  					radius = int(25)
	  					cv2.circle(img,center,radius,(0,0,255),2)

	  ## blue		
	  	if (cr_avg - cr_min)>30:
	  		thresh = (cr_avg-cr_min)*ThreshBlue + cr_min
	  		img_cr_thresh_blue = cv2.inRange(img_cr, thresh, 255)
	  		## contour
	  		im3, contour_blue, hier = cv2.findContours(img_cr_thresh_blue.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	  		if len(contour_blue)>0 and len(contour_blue) < CritialNum:
	  			## reject contour if they are too large or too small
	  			for cnt in contour_blue:
	  				area = cv2.contourArea(cnt)
	  				if area < SizeMax and area > SizeMin:
	  					found_blue = 1
	  					M = cv2.moments(cnt)
	  					cx = int(M['m10']/M['m00'])
	  					cy = int(M['m01']/M['m00'])
	  					center = (cx, cy)
	  					radius = int(25)
	  					cv2.circle(img,center,radius,(255,0,0),2)
	  	# open and close live video
	  	cv2.imshow('frame',img)
	  	## if too many target, then reject
	  	if len(contour_blue) + len(contour_red) >15:
	  		continue
	  	## save everything if targets are identified
	  	if found_red == 1 or found_blue == 1:
	  		## save img
	  		index = str(frame_cnt).zfill(max_target_digit)
	  		img_name = img_path + "target_frame_" + index + ".jpg"
	  		cv2.imwrite(img_name, img1)
	  		frame_cnt = frame_cnt + 1
	  		target_frame_cnt = target_frame_cnt + 1
	  		outstr='\r*****[Status:]     '+ str(target_frame_cnt).zfill(4)+ ' Targets Detected!*****'
	  		sys.stdout.write(outstr)
	  		sys.stdout.flush()
	  	if TargetFlag:
	  		index=str(target_frame_cnt).zfill(max_target_digit)
	  		target_img_name= GotTargetPath+'target_frame_'+index+".jpg"
	  		cv2.imwrite(target_img_name,img1)
	  		target_frame_cnt=target_frame_cnt+1
	  		StopTagetCopyCnt=StopTagetCopyCnt+1
	  	if StopTagetCopyCnt >= 3:
	  		TargetFlag=0

	  		#print('*****[Status:]     ', target_frame_cnt, ' Targets Detected!*****', end='\r')
print('\r',line)
print('\r******************Done***************************')
cap.release()
cv2.destroyAllWindows()