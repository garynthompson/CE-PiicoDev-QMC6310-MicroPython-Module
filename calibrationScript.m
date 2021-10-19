clear all
data = dlmread("calibration.log");
data = data(1:1000,:)
xOffset = (min(data(:,1)) + max(data(:,1)))/2;
yOffset = (min(data(:,2)) + max(data(:,2)))/2;
zOffset = (min(data(:,3)) + max(data(:,3)))/2;

xCal = data(:,1) - xOffset;
yCal = data(:,2) - yOffset;
zCal = data(:,3) - zOffset;

figure(1)

%plot(sqrt(xCal.^2 + yCal.^2 + zCal.^2), "linewidth", 2.0)

%plot(sqrt(x(:,1).^2 + x(:,2).^2 + x(:,3).^2), "linewidth", 2.0)
hold off
plot(xCal, "linewidth", 2.0)
hold on
plot(yCal, "linewidth", 2.0)
title("calibrated Magnetometer Data")
set(gca, "linewidth", 2, "fontsize", 22)
grid on
figure(3)
hold off
plot(data(:,1), "linewidth", 2.0, '-.')
hold on
plot(data(:,2), "linewidth", 2.0, '-.')
set(gca, "linewidth", 2, "fontsize", 22)
title("Raw Magnetometer Data")
grid on

figure(2)
hold off
plot(180/pi*(atan2(yCal, xCal)),'g', "linewidth", 2.0)
hold on
plot(180/pi*(atan2(data(:,2), data(:,1))),'r',  "linewidth", 2)
set(gca, "linewidth", 2, "fontsize", 22)
title("Calibrated and Uncalibrated Heading")
ylabel("Heading (degrees)")
grid on