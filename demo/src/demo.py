#!/usr/bin/env python

import rospy
import moveit_commander
import os
from parser import *
from iiwa_msgs import srv

def configureGripper(action):
	gripper = rospy.ServiceProxy('/iiwa/configuration/openGripper',srv.OpenGripper)
	gripper_request = srv.OpenGripperRequest(action)		
	gripper_response = gripper(gripper_request) 

def configureLed(on, color, blinking):
	configure_led = rospy.ServiceProxy('/iiwa/configuration/configureLed',srv.ConfigureLed)	
	configure_led_request = srv.ConfigureLedRequest(on,color,blinking)
	configure_led_response = configure_led(configure_led_request)

def make_motion(position):
	move_group.set_joint_value_target(position)
	plan = move_group.plan()
	result = move_group.execute(plan, wait=True)
	rospy.sleep(1)


pick_data  = read_yaml_file('/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/demo/config/pick.yaml')
place_data = read_yaml_file('/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/demo/config/place.yaml')

os.environ["ROS_NAMESPACE"] = "/iiwa"

OPEN, CLOSE = True, False
RED, GREEN, BLUE = 1, 2, 3
x, y, z, w = 0, 1, 2, 3

# init instructions
rospy.init_node('demo')
rospy.Rate(1000)
rospy.wait_for_service('/iiwa/configuration/configureLed')
rospy.wait_for_service('/iiwa/configuration/openGripper')
configureLed(False, RED, False)

# starting operations
configureGripper(OPEN)
configureLed(True, RED, False)

# motion planner configurations
move_group = moveit_commander.MoveGroupCommander('manipulator')
move_group.set_planning_time(10)
move_group.set_planner_id("RRTConnect")
move_group.set_end_effector_link("tool_link_center")
move_group.set_start_state_to_current_state()   
move_group.set_pose_reference_frame("world")
move_group.set_goal_tolerance(0.0001)

# first point with joint position
joints = get_joit_position(pick_data)
make_motion(joints)

# get lego in cartesian pose
position = move_group.get_current_pose()
position.pose.position.y = get_cartesian_pose_position(pick_data)[y]
position.pose.position.z = get_cartesian_pose_position(pick_data)[z]

orientation = get_cartesian_pose_orientation(pick_data)
position.pose.orientation.x = orientation[x]
position.pose.orientation.y = orientation[y]
position.pose.orientation.z = orientation[z] 
position.pose.orientation.w = orientation[w]

make_motion(position)
configureGripper(CLOSE)

# move up
position.pose.position.z += 0.2
make_motion(position)

# second point with joint position
joints = get_joit_position(place_data)
make_motion(joints)

# move down and pose lego (cartesian pose)
position = move_group.get_current_pose()
position.pose.position.y = get_cartesian_pose_position(place_data)[y]
position.pose.position.z = get_cartesian_pose_position(place_data)[z]

make_motion(position)

configureGripper(OPEN)

# move up
position.pose.position.z += 0.2
make_motion(position)

# finish
configureLed(True, GREEN, False)

#print(move_group.get_goal_tolerance())

print('------- COMPLETE -------')
