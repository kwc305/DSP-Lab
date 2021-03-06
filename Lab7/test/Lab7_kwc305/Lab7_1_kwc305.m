function filter_gui_example_ver1

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + randn(1, N);        % Input signal

figure(1)
subplot(2,1,1)
line_handle1 = plot(n, x);
title('Noisy data', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])



subplot(2, 1, 2)

Nfft=1024;
X = fft(x, Nfft);
fs = 16000;
xlim([0,fs]);
ylim([0,300]);
f = (0:Nfft-1)/Nfft * fs;
line_handle2 = plot(f, abs(X));
xlabel('Frequency (Hz)')
title('|X(f)|   [SPECTRUM]')


drawnow;

slider_handle = uicontrol('Style', 'slider', ...
    'Min', 0, 'Max', 1,...
    'Value', 1, ...
    'SliderStep', [0.02 0.05], ...
    'Position', [5 200 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle1,line_handle2, x}    );



end


function fun1(hObject, eventdata, line_handle1,line_handle2, x)

fc = get(hObject, 'Value');  % fc : cut-off frequency

fc = max(0.01, fc);         % minimum value
fc = min(0.95, fc);         % maximum value

[b, a] = butter(2, fc);     % Order-2 Butterworth filter
y = filtfilt(b, a, x);
Nfft=1024;
X =fft(y,Nfft);



set(line_handle1, 'ydata',  y);        % Update data in figure
set(line_handle2, 'ydata',  abs(X));        % Update data in figure


title( sprintf('Output of Frequency Response. Cut-off frequency = %.3f', fc), 'fontsize', 12 )

end


