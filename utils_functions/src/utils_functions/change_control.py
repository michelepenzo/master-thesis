#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from create_msgs import *
from services import configure_control_mode

def change_control():

	configure_control_mode(control_mode_srv, create_msg_cartesian_impedance_safety())

	#rospy.sleep(5)

	#configure_control_mode(control_mode_srv, create_msg_position_control())

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('change_control', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	try:
		change_control()

		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		configure_control_mode(control_mode_srv, create_msg_position_control())
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt change_control...')
