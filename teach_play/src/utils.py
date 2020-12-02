 #!/usr/bin/env python

import rospy, csv, Queue

# msgs pkg
from std_msgs.msg import String, Bool
from iiwa_msgs import msg, srv
#from iiwa_msgs import srv
import actionlib_msgs.msg
import actionlib

# macros
ON, OFF = True, False			# turn on/off led, turn on/off blinking
RED, GREEN, BLUE = 1, 2, 3		# rgb colors 

# TODO find package
filename_csv = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/teach_play/actions.csv'


# move gripper to selected configuration
def configure_gripper(action):
	gripper = rospy.ServiceProxy('/iiwa/configuration/openGripper',srv.OpenGripper)
	gripper_request = srv.OpenGripperRequest(action)		
	
	try:
		gripper_response = gripper(gripper_request) 
	except rospy.service.ServiceException as e:
		rospy.logerr('Gripper service Exception')


# configure led to selected configuration
def configure_led(on, color, blinking):
	led = rospy.ServiceProxy('/iiwa/configuration/configureLed',srv.ConfigureLed)	
	configure_led_request = srv.ConfigureLedRequest(on,color,blinking)
	
	try:
		led_response = led(configure_led_request)
	except rospy.service.ServiceException as e:
		rospy.logerr('Led service Exception')


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
		pass


# create movement in cartesian pose (for action)
def create_movement_cartesian_pose(move):
	
	movement=msg.CartesianPose()
	
	movement.poseStamped.header.seq = 1 
	movement.poseStamped.header.stamp = rospy.Time.now()
	movement.poseStamped.header.frame_id = 'iiwa_link_0'
	
	movement.poseStamped.pose.position.x = move[0]
	movement.poseStamped.pose.position.y = move[1]
	movement.poseStamped.pose.position.z = move[2]

	movement.poseStamped.pose.orientation.x = move[3]
	movement.poseStamped.pose.orientation.y = move[4]
	movement.poseStamped.pose.orientation.z = move[5]
	movement.poseStamped.pose.orientation.w = move[6]

	# TODO caricare redundancy da /iiwa/state/CartesianPose
	movement.redundancy.e1 = -1		
	movement.redundancy.status = -1	

	return movement

def create_movement_joint_position(move):
	pass


# wait until paying
def wait_playing():										
	rospy.sleep(2)
	configure_led(bool(ON), int(RED), bool(OFF))
	rospy.sleep(1)
	configure_led(bool(ON), int(BLUE), bool(OFF))
	rospy.sleep(1)
	configure_led(bool(ON), int(GREEN), bool(OFF))
	rospy.sleep(1)