#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from create_msgs import create_msg_cartesian_impedance, create_msg_position_control
from services import configure_control_mode

def move_in_impedance():

	configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('move_in_impedance', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	try:
		move_in_impedance()

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt play...')
