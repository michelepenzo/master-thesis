#!/usr/bin/env python

import actionlib

from create_msgs import *
from functions import *
from services import *


def play(gripper_srv, led_srv):
	configure_led(led_srv, True, 1, False)

	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)
	client.cancel_all_goals()  # clear all old goals
	client.wait_for_server()  # waiting starting server

	# alway start from HOME POSE
	pose = get_cartesian_pose(get_home_pose())  # array
	move_goal = create_movement_cartesian_pose(pose)  # 'movement' object
	action_goal = msg.MoveToCartesianPoseGoal(move_goal)  # action goal
	client.send_goal_and_wait(action_goal)  # send the action to action server and wait
	client.wait_for_result()  # waits for the server to finish performing the action
	rospy.logwarn('Move to home pose')

	# start reading from file
	while True:
		with open(filename_csv) as outfile:
			reader = csv.reader(outfile)

			for line in reader:
				if line[0] == 'pose':
					pose = get_cartesian_pose(line[1:10])  # array
					move_goal = create_movement_cartesian_pose(pose)  # 'movement' object

					action_goal = msg.MoveToCartesianPoseGoal(move_goal)  # action goal

					client.send_goal_and_wait(action_goal)  # send the action to action server and wait
					client.wait_for_result()  # waits for the server to finish performing the action

				elif line[0] == 'action_gripper':
					configure_gripper(gripper_srv, get_action_gripper(line[1]))

				else:
					rospy.logwarn('Anknown action')

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('play', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/configureLed')  # wait led service
	rospy.wait_for_service('/iiwa/configuration/openGripper')  # wait gripper service

	# startup operations
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.ConfigureLed)
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)

	configure_led(led_srv, True, 1, False)
	configure_gripper(gripper_srv, 1)

	try:
		init_play(led_srv)
		play(gripper_srv, led_srv)

	except KeyboardInterrupt:
		configure_led(led_srv, False, 1, False)  # turn off led
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt play...')
