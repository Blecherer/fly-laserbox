% fly.x
% fly.y
% fly.a     % angle
% fly.va    % stochastic angular velocity (rad per sec)
% fly.v     % speed (mm per second)
% fly.time  % last update
function [fly] = updateFly (fly, arena)
    currentTime = clock;
    elapsedTime = etime(clock,fly.time); % sec
    
    
    fly.a = fly.a + fly.va* sqrt(elapsedTime) * randn;
    
    fly.x_prev = fly.x;
    fly.y_prev = fly.y;
    
    fly.x = fly.x + fly.v * cos(fly.a) * elapsedTime;
    fly.y = fly.y + fly.v * sin(fly.a) * elapsedTime;
    
    fly.time_prev = fly.time;
    fly.time = currentTime;
    
    % Arena
    if nargin == 1
       return;
    end
    
    d = pdist([fly.x, fly.y; arena.x, arena.y],'euclidean');
    if d > arena.r
        %a = GetAngle([fly.x, fly.y], [arena.x, arena.y]);
        %fly.x = arena.x + (arena.r-1) * cos(a);
        %fly.y = arena.y + (arena.r-1) * sin(a);
        
        %a = GetAngle([fly.x, fly.y], [arena.x, arena.y]);
        %dr = d - (arena.r + 10);
        %fly.x = fly.x + dr * cos(a);
        %fly.y = fly.y + dr * sin(a);
        
        fly.a = -fly.a;
        fly.x = fly.x_prev;
        fly.y = fly.y_prev;
       
    end
end