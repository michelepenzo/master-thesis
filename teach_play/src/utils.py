 #!/usr/bin/env python

import rospy, csv, Queue

# msgs pkg
from std_msgs.msg import String, Bool
from iiwa_msgs import msg
from iiwa_msgs import srv

# macros
ON, OFF = True, False			# turn on/off led, turn on/off blinking
RED, GREEN, BLUE = 1, 2, 3		# rgb colors 

filename_csv = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/teach_play/csv/actions.csv'


# move gripper to selected configuration
def configure_gripper(action):
	gripper = rospy.ServiceProxy('/iiwa/configuration/openGripper',srv.OpenGripper)
	gripper_request = srv.OpenGripperRequest(action)		
	
	try:
		gripper_response = gripper(gripper_request) 
	except rospy.service.ServiceException as e:
		pass


# configure led to selected configuration
def configure_led(on, color, blinking):
	led = rospy.ServiceProxy('/iiwa/configuration/configureLed',srv.ConfigureLed)	
	configure_led_request = srv.ConfigureLedRequest(on,color,blinking)
	
	try:
		led_response = led(configure_led_request)
	except rospy.service.ServiceException as e:
		pass


# print on csv file
def print_on_csv(data):
	with open(filename_csv, 'ab') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
		wr.writerow(data)

	
# return an array [x, y, z, x, y, z, w] of cartesian pose
def get_cartesian_pose(data):
	return float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), float(data[6])

# return action gripper as boolean
def get_action_gripper(data):
	return bool( int(data) )


# clean file
def clean_file():
	with open(filename_csv, 'w') as outfile:
		outfile.write('')


# create movement
def create_movement(move):
	
	movement=msg.MoveToCartesianPoseActionGoal()
	movement.goal.cartesian_pose.poseStamped.header.frame_id = 'iiwa_link_0'

	movement.goal.cartesian_pose.poseStamped.pose.position.x = move[0]
	movement.goal.cartesian_pose.poseStamped.pose.position.y = move[1]
	movement.goal.cartesian_pose.poseStamped.pose.position.z = move[2]

	movement.goal.cartesian_pose.poseStamped.pose.orientation.x = move[3]
	movement.goal.cartesian_pose.poseStamped.pose.orientation.y = move[4]
	movement.goal.cartesian_pose.poseStamped.pose.orientation.z = move[5]
	movement.goal.cartesian_pose.poseStamped.pose.orientation.w = move[6]

	return movement

# wait until paying
def wait_playing():										
	configure_led(bool(ON), int(RED), bool(OFF))
	rospy.sleep(2)
	configure_led(bool(ON), int(BLUE), bool(OFF))
	rospy.sleep(2)
	configure_led(bool(ON), int(GREEN), bool(OFF))
	rospy.sleep(1)


# 'mutex'
def check_queue(queue_m):
	try:
		queue_m.get(block=True,timeout=10)
	except Queue.Empty:
		rospy.logerr("Timeout reached, exiting...")
		quit()
