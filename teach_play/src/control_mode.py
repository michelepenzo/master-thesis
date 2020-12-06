#!/usr/bin/env python

from create_msgs import *
from services import change_control_mode

# changing control mode in real time
def check_control_mode():
	# TEACH (senza premere)
	#	1- cambio il controllore in position joint
	# 	2- cambio il controllore in cartesian impedance (come se fosse hand guide) --> OCCHIO CHE CADE
	# 	3- rimetto in position joint
	# FINE TEACH
	# 	4- runno il play

	'''
	control_mode, joint_impedance, cartesian_impedance, desired_force, sine_pattern, limits = create_msg_joint_impedance()
	change_control_mode_position_control(control_mode, joint_impedance, cartesian_impedance,
										 desired_force, sine_pattern, limits)
	'''

	# TODO controllare se questa cosa funziona
	change_control_mode(control_mode_srv, create_msg_joint_impedance())

	rospy.sleep(5)

	change_control_mode(control_mode_srv, create_msg_position_control())

	'''
	control_mode, joint_impedance, cartesian_impedance, desired_force, sine_pattern, limits = create_msg_position_control()
	change_control_mode_position_control(control_mode, joint_impedance, cartesian_impedance,
										 desired_force, sine_pattern, limits)
	'''

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('check_control_mode', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	try:
		check_control_mode()
	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt check_control_mode ...')
		rospy.signal_shutdown('')
