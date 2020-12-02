#!/usr/bin/env python

from utils import *

#from iiwa_msgs import msg
#import actionlib_msgs.msg
import actionlib

with open(filename_csv) as outfile:
	reader = csv.reader(outfile)

	for line in reader:
		if line[0] == 'pose':
			print(get_cartesian_pose(line[1:8]))


def fibonacci_client():
	# Creates the SimpleActionClient, passing the type of the action
	# (FibonacciAction) to the constructor.
	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)
   	#client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose',msg.MoveToCartesianPoseActionGoal)


	# Waits until the action server has started up and started
	# listening for goals.
	client.wait_for_server()

	client.cancel_all_goals()
	
	#client.cancel_goals_at_and_before_time(rospy.Time.now())
	

	# Creates a goal to send to the action server.
	#goal = actionlib_tutorials.msg.FibonacciGoal(order=20)
	with open(filename_csv) as outfile:
		reader = csv.reader(outfile)

		for line in reader:
			if line[0] == 'pose':
				goal = msg.MoveToCartesianPoseGoal(
				 create_movement( (get_cartesian_pose(line[1:8])) ) )

				# Sends the goal to the action server.
				client.send_goal_and_wait(goal)
				
				# Waits for the server to finish performing the action.				
				rospy.logwarn('waiting ...')
				client.wait_for_result()
				rospy.logwarn('stop waiting')

				# Prints out the result of executing the action
				rospy.logwarn( client.get_result() ) # A FibonacciResult

	return

if __name__ == '__main__':
	try:
		# Initializes a rospy node so that the SimpleActionClient can
		# publish and subscribe over ROS.
		rospy.init_node('fibonacci_client_py')
		result = fibonacci_client()
		#print("Result:", ', '.join([str(n) for n in result.sequence]))
	except rospy.ROSInterruptException:
		#print("program interrupted before completion", file=sys.stderr)
		print('ros ex')