#!/usr/bin/env python

import actionlib

from utils_functions.create_msgs import *
from utils_functions.functions import *
from utils_functions.services import *


def play(gripper_srv, led_srv):
	is_position_control = True
	configure_led(led_srv, True, 1, False)

	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)
	client.cancel_all_goals()  # clear all old goals
	client.wait_for_server()  # waiting starting server

	if not is_empty():

		init_play(led_srv)

		# TODO partenza dalla home


		# alway start from HOME POSE
		pose = get_cartesian_pose(get_home_pose())
		move_goal = create_movement_cartesian_pose(pose)
		action_goal = msg.MoveToCartesianPoseGoal(move_goal)
		client.send_goal_and_wait(action_goal)
		client.wait_for_result()
		rospy.logwarn('Move to home pose')


		# start reading from file
		#while True:
		for _ in range(2):
			with open(filename_actions_csv) as outfile:
				reader = csv.reader(outfile)

				for line in reader:
					if line[0] == 'pose':

						pose = get_cartesian_pose(line[1:10])  # array
						move_goal = create_movement_cartesian_pose(pose)  # 'movement' object

						if is_position_control:
							rospy.logwarn('eseguo in position')
							action_goal = msg.MoveToCartesianPoseGoal(move_goal)  # action goal
							client.send_goal_and_wait(action_goal)  # send the action to action server and wait
							client.wait_for_result()  # waits for the server to finish performing the action

						else:
							rospy.logwarn('eseguo in impedance')
							pub.publish(move_goal)
							rospy.sleep(1.5)


					elif line[0] == 'action_gripper':
						configure_gripper(gripper_srv, get_action_gripper(line[1]))

					elif line[0] == 'position_control':
						configure_control_mode(control_mode_srv, create_msg_position_control())
						is_position_control = True

					elif line[0] == 'impedance_control':
						configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())
						is_position_control = False

					else:
						rospy.logwarn('Unknown action')

	else:
		rospy.logwarn('Empty action file!')


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('play', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/configureLed')  # wait led service
	rospy.wait_for_service('/iiwa/configuration/openGripper')  # wait gripper service
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# startup operations
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.ConfigureLed)
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	# publisher in impendance
	pub = rospy.Publisher('/iiwa/command/CartesianPose', msg.CartesianPose, queue_size=1)

	configure_led(led_srv, True, 1, False)
	configure_gripper(gripper_srv, 1)

	try:
		configure_control_mode(control_mode_srv, create_msg_position_control())
		play(gripper_srv, led_srv)

	except KeyboardInterrupt:
		configure_led(led_srv, False, 1, False)  # turn off led
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt play...')
