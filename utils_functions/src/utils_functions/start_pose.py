#!/usr/bin/env python

import rospy, actionlib
from utils_functions.create_msgs import *
from utils_functions.functions import *
from iiwa_msgs import msg


def start_pose():
	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)
	client.cancel_all_goals()  # clear all old goals
	client.wait_for_server()  # waiting starting server

	# alway start from HOME POSE
	pose = get_cartesian_pose(get_start_pose())
	move_goal = create_movement_cartesian_pose(pose)
	action_goal = msg.MoveToCartesianPoseGoal(move_goal)
	client.send_goal_and_wait(action_goal)
	client.wait_for_result()

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('start_pose', disable_signals=True)

	try:
		start_pose()

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt start_pose ...')
