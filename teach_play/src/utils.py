 #!/usr/bin/env python

import yaml, rospy, csv
from iiwa_msgs import srv

# msgs pkg
from std_msgs.msg import String, Bool
from iiwa_msgs import msg

import Queue

# macros
OPEN, CLOSE = True, False 		# open/close grippers values
ON, OFF = True, False			# turn on/off led, turn on/off blinking
RED, GREEN, BLUE = 1, 2, 3		# rgb colors 

#filename = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/teach_play/yaml/actions.yaml'
filename_csv = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/teach_play/csv/actions.csv'


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


# ------------------------------------------------------------------------

'''
# open and read the complete file
def read_yaml_file(filename):
	with open(filename, 'r') as stream:
		try:
			data = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)

	return data

# return action led 
def get_action_led(data):
	return data['on'], data['color'], data['blinking']
	

# return action gripper as boolean
def get_action_gripper(data):
	return data


# print string in yaml files
def print_on_file(data):
	with open(filename, 'ab') as outfile:
		yaml.dump(data, outfile, default_flow_style=False)
'''