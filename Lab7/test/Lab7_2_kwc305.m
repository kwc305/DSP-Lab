function kwc305_lab2

G = 0.2;
Gsqrt = sqrt(G);
Q = 0.9;
fc = 0.15;  % w = 2*pi*f
wc = 2*pi*fc;
B = wc/Q

a = [Gsqrt+G*tan(B/2) -2*Gsqrt*cos(wc)   Gsqrt-G*tan(B/2)]
b = [Gsqrt+tan(B/2)   -2*Gsqrt*cos(wc)   Gsqrt-tan(B/2)] 

[H, om] = freqz(b,a,10000);

f1 = figure(1)
plot(om/pi, abs(H))
clf

line_handle = line(om/pi,abs(H),'linewidth',3,'color','blue');
ylim([0 5]);

drawnow;

slider_handle = uicontrol(f1, ...
    'Style', 'slider', ...
    'Tag','sliderfc', ...
    'Min', 0, 'Max', 0.3, ...
    'UserData', struct('fc',fc,'G',G,'Q',Q), ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.05 0.6 0.03], ...
    'Callback',  {@fun1, line_handle}  );

slider_handle2 = uicontrol(f1, ...
    'Style', 'slider', ...
    'Tag','sliderG', ...
    'Min', 0, 'Max', 0.99, ...
    'UserData', struct('fc',fc,'G',G,'Q',Q), ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.15 0.6 0.03], ...
    'Callback',  {@fun2, line_handle}  );

slider_handle3 = uicontrol(f1, ...
    'Style', 'slider', ...
    'Tag','sliderQ', ...
    'Min', 0, 'Max', 2.999, ...
    'UserData', struct('fc',fc,'G',G,'Q',Q), ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.2 0.25 0.6 0.03], ...
    'Callback',  {@fun3, line_handle}  );
end

function fun1(hObject,eventdata,line_handle)
h1 = findobj('Tag','sliderG');
h2 = findobj('Tag','sliderQ');
hObject.UserData.G = h1.UserData.G
hObject.UserData.Q = h2.UserData.Q

fc = hObject.Value;
G = hObject.UserData.G %hObject is to store GUI data
Q = hObject.UserData.Q

wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);

a = [Gsq+G*tan(B/2) -2*Gsq*cos(wc) Gsq-G*tan(B/2)];
b = [Gsq+tan(B/2) -2*Gsq*cos(wc) Gsq-tan(B/2)];
[H,om] = freqz(b,a,10000);

set(line_handle, 'ydata', abs(H));


end

function fun2(hObject,eventdata,line_handle)

h1 = findobj('Tag','sliderfc');
h2 = findobj('Tag','sliderQ');
hObject.UserData.fc = h1.UserData.fc;
hObject.UserData.Q = h2.UserData.Q;

G = hObject.Value
hObject.UserData.G = G;

fc = hObject.UserData.fc;
Q = hObject.UserData.Q;

wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);

a = [Gsq+G*tan(B/2) -2*Gsq*cos(wc) Gsq-G*tan(B/2)];
b = [Gsq+tan(B/2) -2*Gsq*cos(wc) Gsq-tan(B/2)];
[H,om] = freqz(b,a,10000);

set(line_handle,'ydata',abs(H));

end

function fun3(hObject,eventdata,line_handle)
h1 = findobj('Tag','sliderfc');
h2 = findobj('Tag','sliderG');
hObject.UserData.fc = h1.UserData.fc;
hObject.UserData.G = h2.UserData.G;

Q = hObject.Value
hObject.UserData.Q = Q;

fc = hObject.UserData.fc;
G = hObject.UserData.G;


wc = 2*pi*fc;
B = wc/Q;
Gsq = sqrt(G);

a = [Gsq+G*tan(B/2) -2*Gsq*cos(wc) Gsq-G*tan(B/2)];
b = [Gsq+tan(B/2) -2*Gsq*cos(wc) Gsq-tan(B/2)];
[H,om] = freqz(b,a,10000);

set(line_handle,'ydata',abs(H));


end



