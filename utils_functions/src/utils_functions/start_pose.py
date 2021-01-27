#!/usr/bin/env python

import rospy
from iiwa_msgs import msg


# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':

	# init instructions
	rospy.init_node('start_pose', disable_signals=True)

	try:
		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt start_pose ...')
