% Seraching Reference frame no
% Written by Jingxuan
% 2016 Mar 10
clear
clc
%**************************** Inputs **********************************

fileName = 'FlightVideo.MP4';             % Video File Name
cam_ori  = imread('TriggerPic.JPG');      % File Name of the first Phorographic
load('FlightLog.mat')                     % Load the Mat File of Flight Log
start_time = 40;                          % Take-off time in Video, secs
end_time  = 120;                          % Auto Mission start within 2 min;

%***********************************************************************
st = start_time*25;                       % Frame No.to start search
ed = end_time*25;                         % Frame No.to end search
fprintf('Loading the video...')
fprintf('\n');
obj = VideoReader(fileName);
cam=imresize(cam_ori,[1080 1920]);        % Resize the Photo
n=1;
for k = st: 1 : ed 
    frame = read(obj,k);                  % Read Each Frame
    m=cam-frame;                          % Calculate Difference between 2 Pics;
    e(n,1)=k;                             % Record Current Frame No.
    e(n,2)=std2(m(:));                    % Record Mean-Square Deviation  
    n=n+1;
    fprintf('Processing... %5d%',k)       % Show Progress
    fprintf('\n');
end
min_e=min(e(:,2);                         % Find the Minimum Value of Mean-Square Deviation
[row,column]=find(e==mina);               % Locate the Minimum Value
re_frame_no=e(row,1)                      % Reference Frame No.
re_GPS_time=CAM(1,3);                     % GPS Time of the Photo
%************************** Save the Results *****************************
frame = read(obj,re_frame_no);
imshow(frame);
imwrite(frame,strcat(num2str(re_frame_no),'r.jpg'),'jpg');
save('targets_info.mat','re_GPS_time','re_frame_no','CAM','GPS','ATT'); 
[y,Fs]=audioread('0165.wav');
sound(y,Fs);                              % Indicating End