#!/usr/bin/env python

from utils import *

queue = Queue.Queue()				# msgs queue 
queue_m = Queue.Queue()				# movement queue

actual_pose = [0] * 7				# actual pose
action_gripper = 1					# open gripper

client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)

# read MFButton topic and publish action movement
def teach_and_play(data):
	# TODO sporco
	global actual_pose
	global action_gripper

	if data.data:
		queue.put('')
	else:

		if queue.qsize() > 20 and queue.qsize() <= 400:		# one click (POINT)
			#rospy.logwarn("Getting pose")
			print_on_csv(actual_pose)
			configure_led(True, 2, False)
			queue.queue.clear()

		elif queue.qsize() > 400 and queue.qsize() <= 1000:	# two seconds (INVERT GRIPPER)
			

			if action_gripper:
				action_gripper = 0
			else:
				action_gripper = 1
		
			print_on_csv(actual_pose)
			print_on_csv( ('action_gripper', action_gripper) )
			
			configure_led(True, 1, False)
			#rospy.logwarn("Action gripper")		
			queue.queue.clear()

		elif queue.qsize() > 1000:							# 5 seconds 
			rospy.logwarn("Start playing")
			queue.queue.clear()								# STOP TEACHING

			wait_playing()									# wait

			# TODO spostare TEACH tutto in una funzione			
			client.wait_for_server()
			client.cancel_all_goals()

			#while True:										# START PLAYING
			for _ in range(5):
				with open(filename_csv) as outfile:
					reader = csv.reader(outfile)

					for line in reader:
						if line[0] == 'pose':
							pose_goal = create_movement_cartesian_pose(
													get_cartesian_pose(line[1:8]) )		# pose goal # TODO forse ()

							goal_msg = msg.MoveToCartesianPoseGoal( pose_goal ) 			

							client.send_goal_and_wait(goal_msg)							# send goal to action server
							client.wait_for_result()									# wait for the result
							client.get_result()					 					# print the resutl of the execution

						elif line[0] == 'action_gripper':
								configure_gripper( get_action_gripper(line[1]) )


# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = [ 'pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y, data.poseStamped.pose.position.z,
					data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
					data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w ]


# read joint position and save actual position
def read_joint_position(data):
	pass

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':
	
	# init instructions
	rospy.wait_for_service('/iiwa/configuration/configureLed')	# wait led service
	rospy.wait_for_service('/iiwa/configuration/openGripper')	# wait gripper service

	# startup operations
	configure_led(False, 1, False)								# turn off led
	configure_gripper(1)										# open gripper
	clean_file()               									# clean file 

	# listeners
	rospy.init_node('tech_node', disable_signals=True)
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, teach_and_play)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)
	#rospy.Subscriber("/iiwa/state/CartesianPose", msg.JointPosition, read_cartesian_pose)		# TOOD joint pose
	
	# actionclient
	try:
		while not rospy.is_shutdown():
			rospy.sleep(1)
	except KeyboardInterrupt:
		client.cancel_all_goals()
		rospy.logwarn('KeyboardInterrupt ...')
		rospy.sleep(3)