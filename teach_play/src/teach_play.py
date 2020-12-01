#!/usr/bin/env python

from listener import *
from utils import *


# init instructions
rospy.wait_for_service('/iiwa/configuration/configureLed')
rospy.wait_for_service('/iiwa/configuration/openGripper')
configure_led(False, 1, False)								# turn off led on start

clean_file()               									# clean file on open
listener_teach()           									# listern: get actions from MFButton	

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


			elif line[0] == 'action_gripper':
				rospy.logwarn('action_gripper')
				configure_gripper( line[1] )
				rospy.sleep(2)

			'''	
			elif line[0] == 'action_led':		
				rospy.logwarn('action_led')
				configure_led( line[0], line[1], line[2] )
				rospy.sleep(2)
			'''