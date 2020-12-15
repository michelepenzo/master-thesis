#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, TwistStamped
from sensor_msgs.msg import Joy


def read_joy_datas(data):
	pass


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller_node', disable_signals=True)
	#pub = rospy.Publisher("/iiwa/command/CartesianVelocity", TwistStamped, queue_size=100)
	#rospy.Subscriber("/joy", Joy, read_joy_datas)

	try:
		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt controller ...')
