#!/usr/bin/env python

import rospy
from iiwa_msgs import msg
from functions import print_on_csv_wrench

actual_wrench = msg.CartesianWrench().wrench.force

def read_cartesian_wrench(data):
	global actual_wrench
	actual_wrench = data.wrench.force

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('cartesian_wrench', disable_signals=True)

	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)

	try:
		while True:
			print_on_csv_wrench((actual_wrench.x, actual_wrench.y, actual_wrench.z))
			rospy.sleep(0.05)

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt play...')
