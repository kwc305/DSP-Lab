def gain_range(gain):
	gain_max = 10173.843
	if  gain >= gain_max:
		gain = gain_max
	if  gain <= -gain_max:
		gain = -gain_max
	return gain