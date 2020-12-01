#!/usr/bin/env python

from utils import *					# pars yaml file

queue = Queue.Queue()				# msgs queue 
queue_p = Queue.Queue(maxsize=1)	# pose queue


# read MFButton topic and publish action movement
def teach_and_play(data):
	if data.data:
		queue.put(' ')		
	else:
		if queue.qsize() > 20 and queue.qsize() <= 500:			# one click (POINT)
			rospy.logwarn("Getting pose")
			pose = queue_p.get()
			print_on_csv(pose)
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

			rospy.sleep(2)										# wait 8 seconds
			configure_led(bool(ON), int(GREEN), bool(OFF))			
			rospy.sleep(2)									
			configure_led(bool(ON), int(BLUE), bool(OFF))						
			rospy.sleep(2)									
			configure_led(bool(ON), int(RED), bool(OFF))
			rospy.sleep(2)	
			#rospy.signal_shutdown('')	
			
			play()												# START PLAYING 
				

# read cartesian pose and put into a queue with only one element 
def read_cartesian_pose(data):
	queue_p.put([ 'pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y, data.poseStamped.pose.position.z,
					data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
					data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w ])



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
	rospy.Publisher('/iiwa/action/move_to_cartesian_pose_lin/goal', msg.MoveToCartesianPoseActionGoal, queue_size=10)
	rospy.spin()	
