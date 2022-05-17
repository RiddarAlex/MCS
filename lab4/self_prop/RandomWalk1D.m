% Self-propelled particle model of aggregation in one dimension.
% Written by David Sumpter


clear
close all

%Number of individuals
N=1;
%Size of world
L=80;
%Time steps of simulation
T=200;

%Average distance travelled in a single step.
v0=1.5; 
    
%Size of stochastic term
nu=1;         

%Directional persistence
alpha=0;

%Stores histogram of positions of individuals
h=zeros(T,L+1);

%Initial positions
x(1:N)=L/2;
%Initial velocities
u=zeros(1,N);

%For T time steps
for t=1:1:T
 
 
 %Add stochastic effect
 epsilon  = (rand(N,1)-0.5)*nu;
 u(1:N) = alpha*u+epsilon';
 x = x + v0*u;
 
 %Individuals move on a ring.
 x=mod(x,L);
 
 %Store positions of all
 h(t,:)=hist(x,[0:1:L]);
 end

 
 
%Plot time and position figure
    figure(1)
colormap([1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0]]')
imagesc(h);
hlx=ylabel('Time');
hly=xlabel('Position');
set(hlx,'FontSize',12);
set(hly,'FontSize',12);
    axis([0 L 0 T])
    hlx=ylabel('Time');
    hly=xlabel('Position');
    set(hlx,'FontSize',12);
    set(hly,'FontSize',12);


%Plot time and position figure
figure(1)
colormap([1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0] ; 1 [0.9:-1/63:0]]')
imagesc(h);
hlx=ylabel('Time');
hly=xlabel('Position');
set(hlx,'FontSize',12);
set(hly,'FontSize',12);


figure(2)
bar([0:1:L],h(t,:))


figure(3)
%plot([0:1:L],h(t,:))
bar([0:1:L],h(t,:),'r')
hold on

%sd - standard devidation
sd=sqrt(v0*nu^2/12);
plot([0:1:L],normpdf([0:1:L],L/2,sd*sqrt(T))*N,'b')





