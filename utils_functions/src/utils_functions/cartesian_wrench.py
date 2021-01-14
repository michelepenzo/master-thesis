#!/usr/bin/env python

import rospy
from iiwa_msgs import msg
from functions import print_on_csv_wrench, clean_file_wrench


actual_wrench = msg.CartesianWrench().wrench.force
sample_rate = 0.05

def read_cartesian_wrench(data):
	global actual_wrench
	actual_wrench = data.wrench.force

# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':

	# init instructions
	rospy.init_node('cartesian_wrench', disable_signals=True)
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)
	clean_file_wrench()

	try:
		print_on_csv_wrench(('wrench_x', 'wrench_y', 'wrench_z'))

		while True:
			rospy.sleep(sample_rate)
			print_on_csv_wrench((actual_wrench.x, actual_wrench.y, actual_wrench.z))

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt wrench...')
