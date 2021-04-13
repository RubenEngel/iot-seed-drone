#!/usr/bin/env python2

def test():
	x = 5
	if x > 3:
		suitable = True
		position = 'left'
	else:
		suitable = False
		position = 'right'
	return suitable, position

[suitable, _] = test()



