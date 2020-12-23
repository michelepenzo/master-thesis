#!/usr/bin/env python

import Queue

from std_msgs.msg import Bool

from create_msgs import *
from functions import *
from services import *
from play import play

# global variables
queue = Queue.Queue()  # msgs queue
actual_pose = [0] * 7  # actual pose
action_gripper = 1  # open gripper

finish = False


# read MFButton topic and publish action movement
def read_MF_button(data):
	# TODO sporco
	global actual_pose
	global action_gripper
	global finish

	if not data.data:
		if 20 < queue.qsize() <= 400:  # one click (POINT)

			# print on csv, turn on and off LED, print on terminal, clear queue
			print_on_csv(actual_pose)
			configure_led(led_srv, True, 2, False)
			rospy.sleep(1)
			configure_led(led_srv, False, 2, False)
			rospy.logwarn("Get pose")
			queue.queue.clear()

		elif 400 < queue.qsize() <= 1000:  # two seconds (INVERT GRIPPER and GET POINT)

			# invert gripper values, print pose and action on csv, turn on and off led, clear queue
			if action_gripper:
				action_gripper = 0
			else:
				action_gripper = 1

			print_on_csv(actual_pose)
			print_on_csv(('action_gripper', action_gripper))

			configure_led(led_srv, True, 1, False)
			rospy.sleep(1)
			configure_led(led_srv, False, 1, False)
			rospy.logwarn("Get pose and action gripper")
			queue.queue.clear()

		elif queue.qsize() > 1000:  # 5 seconds (STOP TEACHING)

			# clear queue, turn on led, set position control mode, set 'finish' flag true
			rospy.logwarn("Stop teaching")
			queue.queue.clear()
			configure_led(led_srv, True, 3, False)
			configure_control_mode(control_mode_srv, create_msg_position_control())
			finish = True
	else:
		# fill the queue
		queue.put('')


# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = ['pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y,
				   data.poseStamped.pose.position.z,
				   data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
				   data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w,
				   data.redundancy.status, data.redundancy.e1]


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('teach', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/configureLed')  # wait led service
	rospy.wait_for_service('/iiwa/configuration/openGripper')  # wait gripper service
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# service
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.ConfigureLed)
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	# startup operations
	configure_led(led_srv, False, 1, False)
	configure_gripper(gripper_srv, 1)
	clean_file()

	# listeners
	rospy.Subscriber("/iiwa/state/MFButtonState", Bool, read_MF_button)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	try:
		# move to joint impedance
		configure_led(led_srv, True, 3, False)
		rospy.sleep(1)
		configure_control_mode(control_mode_srv, create_msg_joint_impedance())

		while not finish:
			rospy.sleep(1)

		init_play(led_srv)
		play(gripper_srv, led_srv)

	except KeyboardInterrupt:
		rospy.logwarn('KeyboardInterrupt teach...')
		configure_led(led_srv, False, 1, False)
		rospy.signal_shutdown('')
