[cr,cc]=size(CAM);
for m=1:cr
    if m<10
       a(m,:)=strcat('000',num2str(m),'r.jpg');
    end
    if m>=10 && m<100
       a(m,:)=strcat('00',num2str(m),'r.jpg');
    end
    if m>=100 && m<1000
       a(m,:)=strcat('0',num2str(m),'r.jpg');
    end
    if m>=1000
        a(m,:)=strcat(num2str(m),'r.jpg');
    end
    m
end