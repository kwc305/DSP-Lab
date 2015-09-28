def gaincheck(gain,limit):
	limit=limit
	if gain>limit:
		gain=limit
	elif gain<-limit:
			gain=-limit
	else:
		pass
	return gain