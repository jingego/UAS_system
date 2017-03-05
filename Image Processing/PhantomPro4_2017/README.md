#Stream Processing Program for DJI Phantom 4 Pro with Litchi
This program is developed for Taiwan UAV competition and used to process the live video stream from video transimitter and detect targets. 

##Requirement:
Python
openCv 3.1.0

##Useage
Terminal on Linux/Ubuntu, run

```sh
python stream_process.py [source0]
'''
sourceN is an
     - integer number for camera capture
     - leave none will treat the source as cam 1

For example:

```sh
python stream_process.py 0
```
Keys:
    ESC    - exit
    SPACE  - save current frame to <shot path> directory
    ENTER  - start image processing