%http://www.mathworks.co.uk/products/imaq/examples.html?file=/products/demos/shipping/imaq/demoimaq_LaserTracking.html
%function [col, row, laser, properties] = util_findlaser(frame)
function [col, row, boundingBox, area] = util_findlaser(frame)
%UTIL_FINDLASER Return laser coordinates in an image frame. 
%
%    [X, Y, LASER] = UTIL_FINDLASER(FRAME) processes the image FRAME 
%    and returns the X and Y pixel coorindate that corresponds to the centroid 
%    of the laser point in the image. If no laser point is detected, NaN will 
%    be returned for these values instead. LASER is a binary matrix indicating
%    where the laser might be located.
%
%    The algorithm used performs the following 4 steps:
%       1) Inspects the red plane of the image and finds the highest intensity 
%          value present.
%       2) Searches for all locations in the image where this maximum value 
%          occurs, creating a binary image of potential laser locations. 
%       3) Performs a blob analysis to find the largest connected component
%          in the binary image. The centroid of this component is considered to 
%          be the location of the laser, given in pixel coordinates.
%       4) A final check is made to ensure that the number of pixels in the 
%          blob of interest is larger than a threshold so that random noise can be 
%          rejected and not considered a false positive sighting of a laser.  
%

%    DH 2-16-03
%    Copyright 2001-2009 The MathWorks, Inc.
%    $Revision: 1.1.6.3 $  $Date: 2009/05/14 17:02:29 $

% If rgb, take the red plane.  If gray scale, do nothing.
red = frame(:, :, 1);
%white = (frame(:, :, 1) + frame(1, :, :) + frame(:, 1, :))/3;

% Binary matrix of where laser is.
laser = (red >= (0.90 * double(max(red(:)))));
%laser = (red >= (0.80 * double(max(red(:)))));
%laser = (white>= (0.80 * double(max(red(:)))));
props = regionprops(bwlabel(laser), 'Area', 'Centroid', 'BoundingBox');
area = [props.Area];
[num_pixels, index] = max(area);

threshold = 5;
if (num_pixels > threshold)
    % Area of laser is big enough, get region info.
    row = props(index).Centroid(2);
    col = props(index).Centroid(1);
    
    %properties.Area        = props(index).Area       ;
    %properties.Centroid    = props(index).Centroid   ;
    %properties.BoundingBox = props(index).BoundingBox;
    
    boundingBox = props(index).BoundingBox;
    area        = props(index).Area       ;
else 
    % Area of laser is too small to get past the threshold.
    row = NaN;
    col = NaN;
    
    %properties = Nan;
    area = NaN;
    boundingBox = NaN;
end