%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Company name: VaryWave%%
%%Author: Jieming%%
%%Project: UAVtargeting%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [ output ] = uavtarget( input,f_n )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%this part should be performed on the rabbit unit%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CmosInput=input;
CmosCapture=rgb2ycbcr(CmosInput);
InputGray=CmosCapture(:,:,3);%y layer
%done by camera configuration
InputEqu=InputGray;
%image motion detection
%put code here
%end motion detection
%image compression
%put code here
%end compression

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%this part should be performed on the piggy unit%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%image de-compression
%put code here
ReceivedImg=InputEqu;
%end de-compression
%gray scale transform
%Calculate hist sum
%     figure
%     imshow(ReceivedImg);
% ReceivedImg(find(ReceivedImg > 235))=0;

%gaussian blur
% w=fspecial('gaussian',[5 5],3);%% 2 or 3
% ReceivedImg=imfilter(ReceivedImg,w);
%end gaussian blur
%ostu bin
maxva=max(max(ReceivedImg));
minva=min(min(ReceivedImg));
meanva=mean2(ReceivedImg);
%end ostu bin
%sobel
% ReceivedImg=double(ReceivedImg);
% ReceivedImg = edge(ReceivedImg,'sobel','vertical');
% ReceivedImg = uint8(ReceivedImg);
%end sobel
% disp('max');
% disp(maxva-meanva);

% ********************************红色判别************************

if (maxva-meanva)>30
    threadl=maxva-(maxva-meanva)*0.1;
    newim=ReceivedImg;    
    newim(find(newim>threadl))=255;
    newim(find(newim<threadl))=0;
    a_1=sum(newim(:));
    %if a_1> 100000 & a_1 < 110000
    if a_1> 36720 & a_1 < 449820
        imwrite(CmosInput,strcat(num2str(f_n),'.jpg'),'jpg');% 保存帧
        imwrite(newim,strcat(num2str(f_n),'c.jpg'),'jpg');% 保存计算结果
        length(find(newim~=0));
        %output=newim;
    end
end

%***********************************************************************

% disp('min')
% disp(meanva-minva)
if (meanva-minva)>30
    threadl=(meanva-minva)*0.45+minva;
    newim=ReceivedImg;
    newim(find(newim>threadl))=255;
    newim(find(newim<threadl))=0;
    a_2=sum(newim(:));
    %if a_2> 528700000 & a_2 < 528750000
    %if a_2> 528318180 & a_2 < 528750280
    if a_2> 528518180 & a_2 < 528750280
        imwrite(CmosInput,strcat(num2str(f_n),'s.jpg'),'jpg');% 保存帧
        imwrite(newim,strcat(num2str(f_n),'sc.jpg'),'jpg');% 保存计算结果
        length(find(newim~=255));
        %output=newim;
    end
end
% [m,n]=size(ReceivedImg);
% figure
% plot(ReceivedImg,m:-1:1);
end
