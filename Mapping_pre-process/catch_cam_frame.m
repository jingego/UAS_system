clear
clc
tic
%************************请输入文件名！**********************************
%*************************请输入参数：**********************************
tic
fileName = 'auto.MP4'; 
load('targets_info.mat')%读取log数据
obj = VideoReader(fileName);
re_GPS_time=CAM(1,3);
[cr,cc]=size(CAM);
for m=2:cr
    TS=CAM(m,3)-re_GPS_time;
    TN=fix(TS/40);
    k=re_frame_no+TN;
    frame = read(obj,k);
    if m<10
       imwrite(frame,strcat('00',num2str(m),'r.jpg'),'jpg');
    end
    if m>=10 && m<100
       imwrite(frame,strcat('0',num2str(m),'r.jpg'),'jpg');
    end
    if m>=100
        imwrite(frame,strcat(num2str(m),'r.jpg'),'jpg');
    end
end