#!/usr/bin/env python

import rospy
from iiwa_msgs import msg
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback, Joy

from teach_play.functions import print_on_csv, get_cartesian_pose

# macros
ON, OFF = 1.0, 0.0
actual_pose = [0] * 7  # actual pose


# set feedback joypad
def set_feedback(value):
	msg, vib = JoyFeedbackArray(), JoyFeedback()
	vib.type, vib.id, vib.intensity = JoyFeedback.TYPE_RUMBLE, 2, value
	msg.array = [vib]

	pub.publish(msg)


# read external force on end effector
def read_cartesian_wrench(data):
	if abs(data.wrench.force.z) < 10 or abs(data.wrench.force.x) > 10 or abs(data.wrench.force.y) > 10:
		set_feedback(ON)
	else:
		set_feedback(OFF)


# read button state and make actions
def read_joy_buttons(data):
	global actual_pose

	if bool(data.buttons[0]):
		rospy.logwarn("close gripper")
		#print_on_csv(('action_gripper', 0)) # close gripper

	elif bool(data.buttons[1]):
		rospy.logwarn("open gripper")
		#print_on_csv(('action_gripper', 1)) # open gripper

	elif bool(data.buttons[2]):
		rospy.logwarn("get pose")
		#print_on_csv(actual_pose)

	elif bool(data.buttons[10]):
		rospy.logwarn("start play")

	else:
		pass

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
	rospy.init_node('controller', disable_signals=True)
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)

	# external forces, pad buttons, cartesian pose
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)
	rospy.Subscriber('/joy', Joy, read_joy_buttons)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	try:
		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		set_feedback(OFF)
