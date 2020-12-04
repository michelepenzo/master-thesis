#!/usr/bin/env python

from utils_check import * 

# test flag
TEST_CONTROL = 1

# change control mode in position control
def change_control_mode_position_control(msg):
	control_mode_request = srv.ConfigureControlModeRequest(msg)		
	
	try:
		control_mode_response = gripper(control_mode_request) 
	except rospy.service.ServiceException as e:
		rospy.logerr('Control mode service Exception' + str(control_mode_response))


# stessa cosa del teach + play
def check_control_mode(control_mode):

	# vedo che controllore e' attivo (?)
	# TEACH (senza premere)
	#	1- cambio il controllore in position joint
	# 	2- cambio il controllore in cartesian impedance (come se fosse hand guide) --> OCCHIO CHE CADE
	# 	3- rimetto in position joint
	# FINE TEACH
	# 	4- runno il play

	# TUTTI FLOAT !
	msg_position_control = create_msg_position_control()
	msg_joint_impendance = create_msg_position_control()
	#change_control_mode_position_control(msg_position_control)
	change_control_mode_position_control(msg_joint_impendance)

	pass



# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	rospy.init_node('check_control_mode', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	control_mode = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode',srv.ConfigureControlMode)

	try:
		if TEST_CONTROL:
			check_control_mode(control_mode)
		else:
			play()

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt check_control_mode ...')
		rospy.signal_shutdown('')
