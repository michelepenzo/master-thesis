#!/usr/bin/env python

# control Kuka iiwa with ps4 pad
def controller():
	pass

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller', disable_signals=True)

	try:
		controller()
	except KeyboardInterrupt:
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt controller ...')
