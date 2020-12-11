#!/usr/bin/env python

import rospy

from src.play import *
from src.teach import *
from src.control_mode import *

from src.teach import finish

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('main', disable_signals=True)

	# wait for services
	rospy.wait_for_service('/iiwa/configuration/configureLed')
	rospy.wait_for_service('/iiwa/configuration/openGripper')

	# open service
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.configureLed)
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	# startup operations
	configure_led(led_srv, False, 1, False)
	configure_gripper(gripper_srv, 1)
	clean_file()

	# listeners
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, read_MF_button)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	try:
		# change control mode to joint impedance
		configure_led(True, 1, True)
		rospy.sleep(5)
<<<<<<< HEAD
		configure_control_mode(control_mode_srv, create_msg_joint_impedance())
=======
		change_control_mode(control_mode_srv, create_msg_joint_impedance())
>>>>>>> 3247ae8d06419c770416ca3aa805b6718e0d2d66

		# start teaching
		while not finish:
			rospy.sleep(1)

		# change control mode to poisition control
<<<<<<< HEAD
		configure_control_mode(control_mode_srv, create_msg_position_control())

		# start playing
		init_play(gripper_srv)
=======
		change_control_mode(control_mode_srv, create_msg_position_control())

		# start playing
		init_play()
>>>>>>> 3247ae8d06419c770416ca3aa805b6718e0d2d66
		play()

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt main...')
		configure_led(False, 1, False)
		rospy.signal_shutdown('')
