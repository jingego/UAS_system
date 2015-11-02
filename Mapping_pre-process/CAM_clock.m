clear
clc
tic
%************************请输入文件名！**********************************
%*************************请输入参数：**********************************
tic
fileName = 'arup.MP4'; 
cam_ori=imread('G0010005.JPG');%第一张trigger照片
load('32.log-359302.mat')%读取log数据
% start_time=1; %起始时间,min
%***********************************************************************
% st=start_time*60*25; %起始处理帧
fprintf('Loading the video...')
fprintf('\n');
obj = VideoReader(fileName);
numFrames = obj.NumberOfFrames;% 帧的总数
cam=imresize(cam_ori,[1080 1920]);
sum_cam=sum(cam(:));
for k = 311: 1 :1000 % 读取数据
    frame = read(obj,k);
    m=cam-frame;
    allk(k)=std2(m(:))%/sum_cam;    
    if allk(k)<=10
      imwrite(frame,strcat(num2str(k),'r.jpg'),'jpg');
%       break
    end
    fprintf('Processing... %5d%',k)%进程报告
    fprintf('\n');
end
re_frame_no=k    %参考帧
save('targets_info.mat','re_frame_no','CAM','GPS','ATT');
% re_Line_no=CAM(1,1);
% re_yaw=CAM(1,10);
% [y,Fs]=audioread('0165.wav');
% sound(y,Fs);
toc