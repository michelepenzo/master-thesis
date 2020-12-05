#!/usr/bin/env python

from std_msgs.msg import Bool
import actionlib
import actionlib_msgs.msg

from teach_play.utils.functions import *
from teach_play.utils.services import *
from teach_play.utils.create_msgs import *

def play():
	rospy.logwarn('Start playing ...')
	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)

	client.wait_for_server()  												# waiting starting server
	client.cancel_all_goals()  												# clear all old goals

	while True:
		with open(filename_csv) as outfile:
			reader = csv.reader(outfile)

			for line in reader:
				if line[0] == 'pose':

					pose = get_cartesian_pose(line[1:10])					# array
					move_goal = create_movement_cartesian_pose(pose)  		# 'movement' object
					action_goal = msg.MoveToCartesianPoseGoal(move_goal)  	# action goal

					client.send_goal_and_wait(action_goal)  				# send the action to action server and wait
					client.wait_for_result()  								# waits for the server to finish performing the action

				elif line[0] == 'action_gripper':
					configure_gripper(gripper_srv, get_action_gripper(line[1]))


# ---------------------------------------------------------------------------------------------			

if __name__ == '__main__':
	try:
		# init instructions
		rospy.init_node('play', disable_signals=True)
		rospy.wait_for_service('/iiwa/configuration/configureLed')  # wait led service
		rospy.wait_for_service('/iiwa/configuration/openGripper')  # wait gripper service

		# startup operations
		configure_led(True, 1, False)
		configure_gripper(1)
		gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)

		play()

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt play...')
		configure_led(False, 1, False)  # turn off led
		rospy.signal_shutdown('')
