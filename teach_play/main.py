#!/usr/bin/env python

import rospy

from teach_play.src.play import *
from teach_play.src.teach import *
from teach_play.src.control_mode import *

from teach_play.src.teach import finish

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('main', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/configureLed')  # wait led service
	rospy.wait_for_service('/iiwa/configuration/openGripper')  # wait gripper service

	# service
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.configureLed)
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	# startup operations
	configure_led(led_srv, False, 1, False)
	configure_gripper(gripper_srv, 1)
	clean_file()

	# listeners
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, teach_and_play)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	try:
		pass
		# change contrl mode to joint impedance
		configure_led(True, 1, True)
		rospy.sleep(5)
		change_control_mode(control_mode_srv, create_msg_joint_impedance())

		# start teaching
		while not finish:
			rospy.sleep(1)

		# change control mode to poisition control
		change_control_mode(control_mode_srv, create_msg_position_control())

		# start playing
		play()

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt main...')
		configure_led(False, 1, False)
		rospy.signal_shutdown('')
