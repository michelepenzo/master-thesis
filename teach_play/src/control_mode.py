#!/usr/bin/env python

from create_msgs import *
from services import *


# changing control mode in real time
def check_control_mode():
	rospy.logwarn('to joint impedance')
	# configure_control_mode(control_mode_srv, create_msg_joint_impedance())
	configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())

	rospy.sleep(3)

	rospy.logwarn('to position control')
	configure_control_mode(control_mode_srv, create_msg_position_control())


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('check_control_mode', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	try:
		check_control_mode()
	except KeyboardInterrupt:
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt check_control_mode ...')
