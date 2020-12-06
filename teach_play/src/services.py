#!/usr/bin/env python

import rospy
from iiwa_msgs import srv

# move gripper to selected configuration
def configure_gripper(gripper_srv, action):
	gripper_request = srv.OpenGripperRequest(action)

	try:
		gripper_response = gripper_srv(gripper_request)
	except rospy.service.ServiceException as e:
		rospy.logerr('Gripper service Exception')


# configure led to selected configuration
def configure_led(led_srv, on, color, blinking):
	configure_led_request = srv.ConfigureLedRequest(on, color, blinking)

	try:
		led_response = led_srv(configure_led_request)
	except rospy.service.ServiceException as e:
		rospy.logerr('Led service Exception')

# change control mode in position control
def change_control_mode(control_mode_srv, control_mode, joint_impedance, cartesian_impedance, desired_force, sine_pattern, limits):
	control_mode_request = srv.ConfigureControlModeRequest(control_mode, joint_impedance, cartesian_impedance, desired_force, sine_pattern, limits)

	try:
		control_mode_response = control_mode_srv(control_mode_request)
	except rospy.service.ServiceException as e:
		rospy.logerr('Control mode service Exception' + str(control_mode_response))

