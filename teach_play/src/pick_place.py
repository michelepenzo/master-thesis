#!/usr/bin/env python

from std_msgs.msg import Bool
import actionlib
import actionlib_msgs.msg

from functions import *
from services import *
from create_msgs import *


# place one lego over another
def place():
	rospy.logwarn('Start placing ...')
	client = actionlib.SimpleActionClient('/iiwa/action/move_to_cartesian_pose', msg.MoveToCartesianPoseAction)

	client.cancel_all_goals()
	client.wait_for_server()


	# GET LEGO FROM PALLET, POSE 1
	pose = [0.67899, -0.181, 0.2, 0.0, 1.0, 0.0, 0.0, 2, 0.72490485201]
	move_goal = create_movement_cartesian_pose(pose)
	action_goal = msg.MoveToCartesianPoseGoal(move_goal)
	client.send_goal_and_wait(action_goal)
	client.wait_for_result()
	configure_gripper(gripper_srv, 0)

	
	# MOVE UP
	pose =[ 0.437848779582, -0.20973445676, 0.468888963643, 0.0, 1.0, 0.0, 0.0, 2, 0.952986043894]
	move_goal = create_movement_cartesian_pose(pose)
	action_goal = msg.MoveToCartesianPoseGoal(move_goal)
	client.send_goal_and_wait(action_goal)
	client.wait_for_result()


	# POSE BIG LEGO
	pose = [0.443239041669, -0.297993827852, 0.164502074751, 0.0, 1.0, 0.0, 0.0, 2, 0.72490485201]
	move_goal = create_movement_cartesian_pose(pose)
	action_goal = msg.MoveToCartesianPoseGoal(move_goal)
	client.send_goal_and_wait(action_goal)
	client.wait_for_result()

	configure_gripper(gripper_srv, 1)


	# MOVE UP
	pose =[ 0.437848779582, -0.200973445676, 0.468888963643, 0.0, 1.0, 0.0, 0.0, 2, 0.952986043894]
	move_goal = create_movement_cartesian_pose(pose)
	action_goal = msg.MoveToCartesianPoseGoal(move_goal)
	client.send_goal_and_wait(action_goal)
	client.wait_for_result()


# pick up a lego
def pick():
	pass

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('assemble', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/openGripper')  # wait gripper service
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# startup operations
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	configure_gripper(gripper_srv, 1)


	try:
		# change to cartesian impedance
		#configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())

		place()
	except KeyboardInterrupt:
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt assemble...')
