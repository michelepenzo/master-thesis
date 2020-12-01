#!/usr/bin/env python

from utils import *					# pars yaml file

queue = Queue.Queue()				# msgs queue 
actual_pose = [0] * 7				# actual pose

# read MFButton topic and publish action movement
def teach_and_play(data):
	if data.data:
		queue.put(' ')
	else:
		if queue.qsize() > 20 and queue.qsize() <= 500:			# one click (POINT)
			rospy.logwarn("Getting pose")
			global actual_pose
			print_on_csv(actual_pose)
			queue.queue.clear()

		elif queue.qsize() > 500 and queue.qsize() <= 1000:		# two seconds (CLOSE GRIPPER)
			rospy.logwarn("Closing gripper")
			print_on_csv( ('action_gripper', 0) )
			queue.queue.clear()

		elif queue.qsize() > 1000 and queue.qsize() <= 1500:	# three seconds (OPEN GRIPPER)
			print_on_csv( ('action_gripper', 1) )
			rospy.logwarn("Opening gripper")
			queue.queue.clear()

		elif queue.qsize() > 1500:								# 5 seconds 
			rospy.logwarn("Start playing")
			queue.queue.clear()									# STOP TEACHING

			rospy.sleep(2)										# wait
			configure_led(bool(ON), int(RED), bool(OFF))
			rospy.sleep(2)
			configure_led(bool(ON), int(BLUE), bool(OFF))
			rospy.sleep(2)
			configure_led(bool(ON), int(GREEN), bool(OFF))
			rospy.sleep(2)

			while not rospy.is_shutdown():

				with open(filename_csv) as outfile:
					reader = csv.reader(outfile)

					for line in reader:

						if line[0] == 'pose':
							rospy.logwarn('Move to pose')
							pub.publish( create_movement( get_cartesian_pose(line[1:8]) ) )
							rospy.sleep(2)

						elif line[0] == 'action_gripper':
							#rospy.logwarn('Activate gripper')
							configure_gripper( get_action_gripper(line[1]) )
							rospy.sleep(2)

						elif line[0] == 'action_led':
							#rospy.logwarn('action_led')
							configure_led( line[0], line[1], line[2] )
							rospy.sleep(2)

				#rospy.signal_shutdown('')



# read cartesian pose and put into a queue with only one element 
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
	configure_led(False, 1, False)								# turn off led on start
	clean_file()               									# clean file on open

	# start listener and talker on nodes
	rospy.init_node('tech_node', anonymous=True)
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, teach_and_play)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)
	#rospy.Subscriber('/iiwa/action/move_to_cartesian_pose_lin/result',msg.MoveToCartesianPoseActionResult, handler.sub_callback)
	pub = rospy.Publisher('/iiwa/action/move_to_cartesian_pose_lin/goal', msg.MoveToCartesianPoseActionGoal, queue_size=10)
	rospy.spin()	
