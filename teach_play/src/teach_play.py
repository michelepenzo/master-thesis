#!/usr/bin/env python

from listener import *
from utils import *

# init instructions
rospy.wait_for_service('/iiwa/configuration/configureLed')
rospy.wait_for_service('/iiwa/configuration/openGripper')
configure_led(False, 1, False)								# turn off led on start

#clean_file()               									# clean file on open
#listener_teach()           								# listern: get actions from MFButton	

#data = read_yaml_file(filename)								# read complete yaml file


pub = rospy.Publisher('/iiwa/action/move_to_cartesian_pose_lin/goal', msg.MoveToCartesianPoseActionGoal, queue_size=10)
rospy.init_node('talker_node', anonymous=True)
rate = rospy.Rate(100)


while not rospy.is_shutdown():

	with open(filename_csv) as outfile:
		reader = csv.reader(outfile)
   
		for line in reader:
			
			if line[0] == 'pose':
				rospy.logwarn('pose')
				pub.publish( create_movement( get_cartesian_pose(line[1:8]) ) )
				rospy.sleep(2)

			elif line[0] == 'action_led':		
				rospy.logwarn('action_led')
				configure_led( line[0], line[1], line[2] )
				rospy.sleep(2)

			elif line[0] == 'action_gripper':
				rospy.logwarn('action_gripper')
				#configure_gripper( line[1] )
				print(int(line[1]))
				rospy.sleep(2)
			
'''
while not rospy.is_shutdown():

	for i in range(len(data)):
		action = (data.items()[i])

		if 'pose' in action[0]:
			rospy.logwarn('pose')
			#pub.publish( create_movement( get_cartesian_pose(action[1]) ) )
			rospy.sleep(2)

		elif action[0] == 'action_led':		
			rospy.logwarn('action_led')
			x = get_action_led(action[1])
			#configure_led( x[0], x[1], x[2] )
			rospy.sleep(2)

		elif action[0] == 'action_gripper':
			rospy.logwarn('action_gripper')
			#configure_gripper( get_action_gripper(action[1]) )
			rospy.sleep(2)
'''
