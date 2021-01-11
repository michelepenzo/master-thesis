#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from create_msgs import create_msg_cartesian_impedance, create_msg_position_control, create_movement_cartesian_pose
from services import configure_control_mode

from geometry_msgs.msg import PoseStamped
from functions import *

def move_in_impedance():

	configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())
	#configure_control_mode(control_mode_srv, create_msg_position_control())


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('move_in_impedance', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	pub = rospy.Publisher('/iiwa/command/CartesianPose', msg.CartesianPose, queue_size=1)


	try:
		move_in_impedance()

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt play...')
