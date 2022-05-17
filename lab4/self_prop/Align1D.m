% Self-propelled particle model of aggregation in one dimension.
% Written by David Sumpter

clear
close all

%Number of individuals
N=100;
%Size of world
L=200;
%Time steps of simulation
T=400;

%Average distance travelled in a single step.
v0=1; 

%Interaction zone
delta=1;      
%Size of stochastic term
nu=2.5;         

%Directional persistence
alpha=0.3;

%Stores histogram of positions of individuals
hx=zeros(T,N);
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
     xlocal = (abs(x(i)-x)<delta & abs(x(i)-x)~=0) | ((abs(x(i)-x)>L-delta) & abs(x(i)-x)~=0);
     
    if sum(xlocal)>0
        ulocal = sum(u.*xlocal)/sum(xlocal);
    else
        ulocal = 0;
    end

    if ulocal>0 
        pu(i)=(ulocal+1)/2;
    elseif ulocal<0
        pu(i)=(ulocal-1)/2;
    else
        pu(i)=0;
    end
 end

 %Add stochastic effect
 epsilon  = (rand(N,1)-0.5)*nu;
 u(1:N) = alpha*u+(1-alpha)*pu+epsilon';
 
 %Individuals move on a ring.
 x=mod(x,L);
 
 %Store positions of all
 hx(t,:)=x;
 h(t,:)=hist(x,[0:1:L]);
 a(t)=mean(u);
 
% %Plot time and position figure
% figure(1)
% colormap([1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0]]')
% plot(hx'*251.3/36,[1:1:T]/60,'k.');
% axis([0 251.3 0 10])
% hlx=ylabel('Time');
% hly=xlabel('Position');
% set(hlx,'FontSize',12);
% set(hly,'FontSize',12);

figure(3)
colormap([1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0]]')
imagesc([0:1:L],[1:1:T],h);
axis([0 L 0 T]);
hlx=ylabel('Time steps');
hly=xlabel('Position');
set(hlx,'FontSize',12);
set(hly,'FontSize',12);


M(t)=getframe;


end

figure(2)
plot([1:1:T],a,'k')
hlx=xlabel('Time steps')
hly=ylabel('Alignment')
set(hlx,'FontSize',16);
set(hly,'FontSize',16);

