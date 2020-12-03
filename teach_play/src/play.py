#!/usr/bin/env python

from utils import *

def play():
	
	rospy.logwarn('ACTION CLIENT: ' + str(rospy.get_name()))
	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)

	client.wait_for_server()		# waiting starting server
	client.cancel_all_goals()		# clear all old goals
	
	#while True:
	for _ in range(3):
		with open(filename_csv) as outfile:
			reader = csv.reader(outfile)

			for line in reader:
				if line[0] == 'pose':
					
					pose = get_cartesian_pose(line[1:10])					# array 
					move_goal = create_movement_cartesian_pose(pose)		# 'movement' object
					action_goal = msg.MoveToCartesianPoseGoal(move_goal)	# action goal

					client.send_goal_and_wait(action_goal)					# send the action to action server and wait
					client.wait_for_result()								# waits for the server to finish performing the action
				
				# TODO gestione del gripper
				elif line[0] == 'action_gripper':
					configure_gripper( get_action_gripper(line[1]) )
				

if __name__ == '__main__':
	try:
		rospy.init_node('play', disable_signals=True)
		init_play()
		play()
	
	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt play...')
		rospy.signal_shutdown('')
		quit()