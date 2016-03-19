function GM1=fungry1(x0) %输入原始数据x0
T=input('T=');%从键盘输入从最后一个历史数据算起的第T时点
x1=zeros(1,length(x0));B=zeros(length(x0)-1,2);
yn=zeros(length(x0)-1,1);Hatx0=zeros(1,length(x0)+T);
Hatx00=zeros(1,length(x0));Hatx1=zeros(1,length(x0)+T);
epsilon=zeros(length(x0),1);omega=zeros(length(x0),1);
for i=1:length(x0)
    for j=1:i
        x1(i)=x1(i)+x0(j);
    end
end
for i=1:length(x0)-1
    B(i,1)=(-1/2)*(x1(i)+x1(i+1));
    B(i,2)=1;
    yn(i)=x0(i+1);
end
HatA=(inv(B'*B))*B'*yn % GM(1,1)模型参数估计
for k=1:length(x0)+T
    Hatx1(k)=(x0(1)-HatA(2)/HatA(1))*exp(-HatA(1)*(k-1))+HatA(2)/HatA(1);
end
Hatx0(1)=Hatx1(1);
for k=2:length(x0)+T
    Hatx0(k)=Hatx1(k)-Hatx1(k-1);%累计还原得到历史数据的模拟值
end
for i=1:length(x0) %开始模型检验
    epsilon(i)=x0(i)-Hatx0(i);
    omega(i)=(epsilon(i)/x0(i))*100;
end
% x0;Hatx0;epsilon;omega;  %必要时去掉％得到各种数据
c=std(epsilon)/std(x0);p=0;
for i=1:length(x0)
    if abs(epsilon(i)-mean(epsilon))<0.6745*std(x0)
        p=p+1;
    end
end
p=p/length(x0)
if p>0.95 & c<0.35
    disp('The model is good,and the forecast is:'),
    disp(Hatx0(length(x0)+T))
elseif p>0.85 & c<0.5
    disp('The model is eligibility,and the forecast is:'),
    disp(Hatx0(length(x0)+T))
elseif p>0.7 & c>0.65
    disp('The model is not good,and the forecast is:'),
    disp(Hatx0(length(x0)+T))
else p<=0.7 & c>0.65
    disp('The model is bad and try again')
end
for i=1:length(x0)
    Hatx00(i)=Hatx0(i);
end
z=1:length(x0);
plot(z,x0,'-',z,Hatx00,':') %将原始数据和模拟值画在一个图上帮助观察
text(2,x0(2),'History data: real line')
text(length(x0)/2,Hatx00(length(x0))/2,'Simulation data:broken line')
end

    
    
    
   


