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
	if data.data:
		queue.put(' ')
	else:

		if queue.qsize() > 20 and queue.qsize() <= 400:		# one click (POINT)
			rospy.logwarn("Getting pose")
			global actual_pose
			print_on_csv(actual_pose)
			queue.queue.clear()

		elif queue.qsize() > 400 and queue.qsize() <= 1000:	# two seconds (INVERT GRIPPER)
			global action_gripper
			if action_gripper:
				action_gripper = 0
			else:
				action_gripper = 1
			
			print_on_csv( ('action_gripper', action_gripper) )
			rospy.logwarn("Action gripper")
			
			queue.queue.clear()

		elif queue.qsize() > 1000:							# 5 seconds 
			rospy.logwarn("Start playing")
			queue.queue.clear()								# STOP TEACHING

			wait_playing()									# wait

			while not rospy.is_shutdown():					# START PLAYING

				with open(filename_csv) as outfile:
					reader = csv.reader(outfile)

					for line in reader:
						if line[0] == 'pose':
							pub.publish( create_movement( get_cartesian_pose(line[1:8]) ) )
							check_queue(queue_m)

						elif line[0] == 'action_gripper':
							configure_gripper( get_action_gripper(line[1]) )

				#rospy.signal_shutdown('')



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
	clean_file()               									# clean file 

	handler = MyHandler(queue_m)

	# listeners
	rospy.init_node('tech_node', anonymous=True)
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, teach_and_play)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)
	rospy.Subscriber('/iiwa/action/move_to_cartesian_pose_lin/result',msg.MoveToCartesianPoseActionResult, handler.sub_callback)

	# publisher
	pub = rospy.Publisher('/iiwa/action/move_to_cartesian_pose_lin/goal', msg.MoveToCartesianPoseActionGoal, queue_size=10)

	rospy.spin()	
