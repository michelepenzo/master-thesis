#!/usr/bin/env python

import rospy
from iiwa_msgs import msg

if __name__ == '__main__':
	rospy.init_node('init', disable_signals=True)
	pub = rospy.Publisher('/iiwa/command/CartesianVelcoity', msg.CartesianVelocity)

	rospy.Rate(100)

	while not rospy.is_shutdown():
		pass

