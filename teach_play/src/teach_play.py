#!/usr/bin/env python

from utils import *

queue = Queue.Queue()				# msgs queue 
queue_m = Queue.Queue()				# movement queue

actual_pose = [0] * 7				# actual pose
action_gripper = 1					# open gripper

# handler for queue
class MyHandler(object):

	def __init__(self, q):
		self._q = q

	def sub_callback(self, result):
		self._q.put(1)


# read MFButton topic and publish action movement
def teach_and_play(data):
	global actual_pose
	
	if data.data:
		queue.put('')
	else:

		if queue.qsize() > 20 and queue.qsize() <= 400:		# one click (POINT)
			rospy.logwarn("Getting pose")

			print_on_csv(actual_pose)
			queue.queue.clear()

		elif queue.qsize() > 400 and queue.qsize() <= 1000:	# two seconds (INVERT GRIPPER)
			global action_gripper

			if action_gripper:
				action_gripper = 0
			else:
				action_gripper = 1
		
			print_on_csv(actual_pose)
			print_on_csv( ('action_gripper', action_gripper) )
			
			rospy.logwarn("Action gripper")		
			queue.queue.clear()

		elif queue.qsize() > 1000:							# 5 seconds 
			rospy.logwarn("Start playing")
			queue.queue.clear()								# STOP TEACHING

			wait_playing()									# wait

			client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)

			client.wait_for_server()
			client.cancel_all_goals()

			while not rospy.is_shutdown():		# START PLAYING
		
				with open(filename_csv) as outfile:
					reader = csv.reader(outfile)

					for line in reader:
						if line[0] == 'pose':

							goal = msg.MoveToCartesianPoseGoal( create_movement((get_cartesian_pose(line[1:8]))) )
							client.send_goal_and_wait(goal)							# Sends the goal to the action server.
							client.wait_for_result()								# Waits for the server to finish performing the action.				
							rospy.logwarn( client.get_result() ) 					# Prints out the result of executing the action

						elif line[0] == 'action_gripper':
								configure_gripper( get_action_gripper(line[1]) )

# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = [ 'pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y, data.poseStamped.pose.position.z,
					data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
					data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w ]


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':
	
	# init instructions
	rospy.wait_for_service('/iiwa/configuration/configureLed')	# wait led service
	rospy.wait_for_service('/iiwa/configuration/openGripper')	# wait gripper service

	# startup operations
	configure_led(False, 1, False)								# turn off led
	configure_gripper(1)										# open gripper
	#clean_file()               									# clean file 

	handler = MyHandler(queue_m)

	# listeners
	rospy.init_node('tech_node', disable_signals=True)
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, teach_and_play)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)
	rospy.Subscriber('/iiwa/action/move_to_cartesian_pose_lin/result',msg.MoveToCartesianPoseActionResult, handler.sub_callback)
	
	# actionclient
	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)
	try:
		while not rospy.is_shutdown():
			rospy.sleep(1)
	except:
		client.cancel_all_goals()
		sleep(3)
	