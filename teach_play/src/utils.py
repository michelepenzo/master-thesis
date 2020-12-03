 #!/usr/bin/env python

import rospy, csv, Queue, rospkg, actionlib

# msgs pkg
from std_msgs.msg import String, Bool
from iiwa_msgs import msg, srv
import actionlib_msgs.msg

# macros
ON, OFF = True, False			# turn on/off led, turn on/off blinking
RED, GREEN, BLUE = 1, 2, 3		# rgb colors 
filename_csv = rospkg.RosPack().get_path('teach_play') + '/actions.csv'


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

	
# return an array [x, y, z, x, y, z, w, status, redundancy]
def get_cartesian_pose(data):
	return float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), float(data[6]), int(data[7]), float(data[8])


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

	movement.redundancy.status = move[7]	
	movement.redundancy.e1 = move[8]
	
	return movement

# wait until paying
def init_play():										
	rospy.sleep(1)
	configure_led(bool(ON), int(RED), bool(OFF))
	rospy.sleep(1)
	configure_led(bool(ON), int(GREEN), bool(OFF))
	rospy.sleep(1)