#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from sensor_msgs.msg import Joy

from teach_play.create_msgs import create_msg_cartesian_impedance, create_msg_position_control
from teach_play.services import configure_control_mode


actual_pose = [0] * 7  # actual pose


# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = ['pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y,
				   data.poseStamped.pose.position.z,
				   data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
				   data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w,
				   data.redundancy.status, data.redundancy.e1]


# read joy buttons and parse
def read_joy_buttons(data):

	if data.buttons[2]:
		rospy.logwarn('2')

	if data.buttons[3]:
		rospy.logwarn('3')





# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('teach_controller', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# wait for services
	rospy.wait_for_service('/iiwa/configuration/configureLed')
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# service
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.ConfigureLed)
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)


	# listeners
	rospy.Subscriber("/joy", Joy, read_joy_buttons)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	try:

		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		pass
