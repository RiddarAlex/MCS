%Floor painter algorithm
%Written by Alex Szorkovszky for UU Modelling Complex Systems course

%INPUTS
%rules: 54-cell array with one of three actions: 0(do nothing) 1(turn left) 2(turn right) 3(random)
%room: MxN matrix defining a rectangular room with each square either 0(empty) or 1(furniture).

%OUTPUTS
%score: percentage of empty space painted
%xpos: x positions over time
%ypos: y positions over time

function [score,xpos,ypos] = painter_play(rules,room)


[M,N] = size(room);
t = length(room(:)) - sum(room(:));

xpos = nan(t+1,1);
ypos = nan(t+1,1);


%add walls
env = ones(M+2,N+2);
env(2:(M+1),2:(N+1)) = room;

M = M+2;
N = N+2;

%random initial location
while 1
  xpos(1) = ceil(M*rand);
  ypos(1) = ceil(N*rand);
  if env(xpos(1),ypos(1))==0
      break;
  end
end

%random orientation (up=0,left=-1,right=+1,down=-2)
dir = floor(4*rand) - 2;

%initial score
score = 0;

for i=1:t
    

    
  dx = rem(dir,2);
  dy = rem(dir+1,2);
  
  dxr = rem(dir+1,2);
  dyr = -rem(dir,2);
  
  %evaluate surroundings (forward,left,right)
  local = [env(xpos(i)+dx,ypos(i)+dy),env(xpos(i)-dxr,ypos(i)-dyr),env(xpos(i)+dxr,ypos(i)+dyr)];
  
  localnum = 2*(sum((3.^(2:-1:0)) .* local)) + 1; % 1,3,5...53
  if env(xpos(i),ypos(i)) == 2 % entering painted square: 2,4,6...54
      localnum = localnum + 1;
  end
  
  %use turning rule
  
  if rules(localnum) == 3
      dirchange = round(rand) + 1;
  else
      dirchange = rules(localnum);
  end
  
  if dirchange == 1
    dir = rem(dir-2,4) + 1;   
  elseif dirchange == 2
    dir = rem(dir+3,4) - 2;
  end
  
  dx = rem(dir,2);
  dy = rem(dir+1,2);
  
  %paint square
  if env(xpos(i),ypos(i))==0
     env(xpos(i),ypos(i)) = 2;
     score = score + 1;
  end
  
  %go forward if possible
  
  if env(xpos(i)+dx,ypos(i)+dy) == 1
     xpos(i+1) = xpos(i);
     ypos(i+1) = ypos(i);
  else
     xpos(i+1) = xpos(i)+dx;
     ypos(i+1) = ypos(i)+dy;      
  end
  
  
end

%subtract external walls from position
xpos = xpos - 1;
ypos = ypos - 1;

%normalise score by time
score = score/t;

end