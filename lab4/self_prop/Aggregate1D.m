% Self-propelled particle model of aggregation in one dimension.
% Written by David Sumpter

clear
clf

%Number of individuals
N=50;
%Size of world
L=200;
%Time steps of simulation
T=100;

%Average distance travelled in a single step.
v0=1; 

%Interaction zone
delta=12;      
%Size of stochastic term
nu=0.5;         

%Directional persistence
alpha=0.5;

%Stores histogram of positions of individuals
h=zeros(T,L+1);

%Initial positions
x(1:N)=rand(N,1)*L-L/2;
%Initial velocities
u(1:N)=rand(N,1)*2-1;

%For T time steps
for t=1:1:T
 
 
 %For N individuals
 for i=1:1:N
    x(i)= x(i) + v0*u(i);
     
    xlocal1 = (abs(x(i)-x)<delta & abs(x(i)-x)~=0);
    xlocal2 = ((abs(x(i)-x)>L-delta) & abs(x(i)-x)~=0);

    if sum(xlocal1+xlocal2)>0
        pu(i) = sum(sign(x-x(i)).*xlocal1+sign(x(i)-x).*xlocal2)/sum(xlocal1+xlocal2);
    else
        pu(i) = 0;
    end

 end

 %Add stochastic effect
 epsilon  = (rand(N,1)-0.5)*nu;
 u(1:N) = alpha*u+(1-alpha)*pu+epsilon';
 
 %Individuals move on a ring.
 x=mod(x,L);
 
 %Store positions of all
 h(t,:)=hist(x,[0:1:L]);

%Plot time and position figure
%     figure(2)
%     plot(x,(T-t)*ones(length(x),1),'.');
%     hold on
%     axis([0 L 0 T])
%     hlx=ylabel('Time')
%     hly=xlabel('Position')
%     set(hlx,'FontSize',12);
%     set(hly,'FontSize',12);
end

%Plot time and position figure
figure(1)
colormap([1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0]]')
imagesc(h);
hlx=ylabel('Time')
hly=xlabel('Position')
set(hlx,'FontSize',16);
set(hly,'FontSize',16);


