%% makefilter_03.m 
% Filter twice for gradual rise time

%%

clc
clear

%% Difference equation
% y(n) = b0 x(n) - a1 y(n-1) - a2 y(n-2)

Fs = 8000;          % sampling frequency (sample/second)
F1 = 400;           % frequency (cycles/second)
f1 = F1/Fs          % normalized fequenccy (cycles/sample)
om1 = 2*pi * f1;    % normalized fequenccy (radians/sample)

Ta = 0.5;           % duration (seconds) [time till 1% amplitude]
r = 0.1^(1/(Ta*Fs))

a = [1 -2*r*cos(om1) r^2]  % recursive part
b = 1;              % non-recursive part
zplane(b,a);

%% Impulse response
% Note that the amplitude profile has the form E(n) = n r^n.

N = Fs;
n = 0:N;

imp = [1 zeros(1, N)]; %impulse signal
h = filter(b, a, imp); %transfer function

figure(1)
clf
plot(n/Fs, h)
title('Impulse response');
xlabel('Time (sec)')
zoom xon