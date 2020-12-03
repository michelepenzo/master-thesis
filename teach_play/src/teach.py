#!/usr/bin/env python

from utils import *
from play import *

queue = Queue.Queue()				# msgs queue 
queue_m = Queue.Queue()				# movement queue

actual_pose = [0] * 7				# actual pose
action_gripper = 1					# open gripper

sleep_running = True

# read MFButton topic and publish action movement
def teach_and_play(data):
	# TODO sporco
	# TODO rimuovere service del gripper
	global actual_pose
	global action_gripper
	global sleep_running

	if data.data:
		queue.put('')
	else:

		if queue.qsize() > 20 and queue.qsize() <= 400:		# one click (POINT)
			
			print_on_csv(actual_pose)
			configure_led(True, 2, False)
			sleep(1)
			configure_led(False, 2, False)
			rospy.logwarn("Get pose")
			queue.queue.clear()

		elif queue.qsize() > 400 and queue.qsize() <= 1000:	# two seconds (INVERT GRIPPER)
			

			if action_gripper:
				action_gripper = 0
			else:
				action_gripper = 1
		
			print_on_csv(actual_pose)
			print_on_csv( ('action_gripper', action_gripper) )
			
			configure_led(True, 1, False)
			sleep(1)
			configure_led(False, 1, False)
			rospy.logwarn("Get pose and action gripper")		
			queue.queue.clear()

		elif queue.qsize() > 1000:							# 5 seconds 
			rospy.logwarn("Stop teaching")
			queue.queue.clear()								# STOP TEACHING


# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = [ 'pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y, data.poseStamped.pose.position.z,
					data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
					data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w,
					data.redundancy.status, data.redundancy.e1 ]

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
	rospy.init_node('teach', disable_signals=True)
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, teach_and_play)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)
	
	# actionclient
	try:
		
		while True:
			rospy.sleep(1)
		
		#play()

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt teach_and_play...')
		rospy.signal_shutdown('')
