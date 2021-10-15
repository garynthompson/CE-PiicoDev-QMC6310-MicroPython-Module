clear all
x = dlmread("calibration.log");
xOffset = (min(x(:,1)) + max(x(:,1)))/2
yOffset = (min(x(:,2)) + max(x(:,2)))/2
zOffset = (min(x(:,3)) + max(x(:,3)))/2

xCal = x(:,1) - xOffset;
yCal = x(:,2) - yOffset;
zCal = x(:,3) - zOffset;

figure(1)
hold off
plot(sqrt(xCal.^2 + yCal.^2 + zCal.^2))
hold on
plot(sqrt(x(:,1).^2 + x(:,2).^2 + x(:,3).^2))
plot(xCal)
plot(yCal)

figure(2)
hold off
plot((atan2(yCal, xCal)),'g')
hold on
plot((atan2(x(:,2), x(:,1))),'r')