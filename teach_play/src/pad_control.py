#!/usr/bin/env python

import rospy

# TODO importare msg

def pad_control():
	pass
	
# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':
	try:
		# init instructions
		rospy.init_node('pad_control', disable_signals=True)
		
		pad_control()

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt pad_control...')
		rospy.signal_shutdown('')
 
