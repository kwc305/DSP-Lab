%% makefilter_03.m 
% Filter twice for gradual rise time

%%

clc
clear

%% Difference equation
% y(n) = b0 x(n) - a1 y(n-1) - a2 y(n-2)

Fs = 8000;          % sampling frequency (sample/second)
F1 = 400; % frequency (cycles/second)

f1 = F1/Fs          % normalized fequenccy (cycles/sample)
om1 = 2*pi * f1;    % normalized fequenccy (radians/sample)

Ta1 = 0.5; % duration (seconds) [time till 1% amplitude]
Ta2 = 0.8
r1 = 0.01^(1/(Ta1*Fs))
r2 = 0.01^(1/(Ta2*Fs))
peak = log((1-r1)/(1-r2))/log(r2/r1)/8000
a11 = [1 -2*r1*cos(om1) r1^2]  % recursive part
a22 = [1 -2*r2*cos(om1) r2^2]
 a = [1 1.89995 0.9]
b = 1;              % non-recursive part
% change b, just change b0, twice the impulse response?

%% Impulse response
% Note that the amplitude profile has the form E(n) = n r^n.

N = Fs;
n = 0:N;

imp = [2 zeros(1, N)];
h = filter(b, a, imp);

figure(1)
clf
plot(n/Fs, h)
title('Impulse response');
xlabel('Time (sec)')
zoom xon

%% Listen

soundsc(h, Fs)

%% Twice the filter

% a2 = conv(a, a)
a2 = conv(a11, a22)
b2 = 0.5;

h2 = filter(b2, a2, imp);

plot(n/Fs, h2)
title('Impulse response');
xlabel('Time (sec)')

% What is the peak amplitude in terms of f1 and r?


%% Listen

soundsc(h2, Fs)

%% Pole-zero plot
% Note that the poles double poles

zplane(b2, a2)
title('Pole-zero Plot')

%% Frequency response
% The frequency response has a peak at f1

[H2, om] = freqz(b2, a2);
f = om / (2*pi) * Fs;
plot(f, abs(H2))
title('Frequency response')
xlabel('Frequency (cycles/second)')
xlim([0 1000])
grid


%%

H2dB = 20*log10(abs(H2));

plot(f, H2dB)
title('Frequency response')
xlabel('Frequency (cycles/second)')
xlim([0 1000])
grid








