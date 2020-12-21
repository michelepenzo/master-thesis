#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback, Joy
from teach_play.functions import print_on_csv, clean_file, init_play
from teach_play.play import play
from teach_play.services import configure_gripper, configure_led

# IMPEDANCE = False

# global values
actual_pose = [0] * 7  # actual pose
last_events = [False] * 11
x_force, y_force, z_force = 10, 10, 10


# set feedback joypad
def set_feedback(value):
	msg_f, vib = JoyFeedbackArray(), JoyFeedback()

	# id = 0, 1, 2 per la tipologia di vibrazione
	vib.type, vib.id, vib.intensity = JoyFeedback.TYPE_RUMBLE, 0, value
	msg_f.array = [vib]

	pub.publish(msg_f)


# read external force on end effector
def read_cartesian_wrench(data):
	if data.wrench.force.z < z_force or abs(data.wrench.force.x) > x_force or abs(data.wrench.force.y) > y_force:
		set_feedback(1.0)
	else:
		set_feedback(0.0)


# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = ['pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y,
				   data.poseStamped.pose.position.z,
				   data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
				   data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w,
				   data.redundancy.status, data.redundancy.e1]


# read joy buttons and parse (0 -> 1 -> 0)
def read_joy_buttons(data):
	check_on_click(data, 2, 1)  # read pose
	# check_on_click(data, 3, 2)  # change controller	# TODO nuovo valore del pulsante
	check_on_click(data, 0, 3)  # action gripper
	check_on_click(data, 1, 4)  # action gripper
	check_on_click(data, 10, 5)  # start playing


# check onClick event
def check_on_click(data, pos, action):
	# TODO sistemare con passaggio a funzione

	if data.buttons[pos]:
		last_events[pos] = True
	elif last_events[pos] == True and data.buttons[pos] == False:

		if action == 1:  # read pose
			rospy.logwarn("Get pose")
			print_on_csv(actual_pose)

		# elif action == 2:  # change controller
		#	rospy.logwarn('change controller -> NOT DONE')

		elif action == 3:  # action gripper CLOSE
			rospy.logwarn("Get pose and action gripper")
			print_on_csv(actual_pose)
			print_on_csv(('action_gripper', 0))

		elif action == 4:  # action gripper OPEN
			print_on_csv(actual_pose)
			print_on_csv(('action_gripper', 1))

		elif action == 5:  # start playing
			init_play(led_srv)
			play(gripper_srv, led_srv)

		else:
			pass
		last_events[pos] = False


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions, need time ...
	rospy.init_node('controller', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')
	rospy.wait_for_service('/iiwa/configuration/configureLed')
	rospy.wait_for_service('/iiwa/configuration/openGripper')

	# topics
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)
	rospy.Subscriber("/joy", Joy, read_joy_buttons)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	# services
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)
	led_srv = rospy.ServiceProxy('/iiwa/configuration/configureLed', srv.ConfigureLed)
	gripper_srv = rospy.ServiceProxy('/iiwa/configuration/openGripper', srv.OpenGripper)

	# startup operations
	clean_file()
	configure_gripper(gripper_srv, 1)

	try:
		'''
		configure_control_mode(control_mode_srv, create_msg_position_control())
				
		# move in cartesian impedance if True, else in position control (by default)
		if IMPEDANCE:
			z_force = 5
			configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())
		'''

		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		configure_led(led_srv, False, 1, False)  # turn off led
		set_feedback(0.0)
