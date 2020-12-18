#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback, Joy

from teach_play.create_msgs import create_msg_cartesian_impedance, create_msg_position_control
from teach_play.services import configure_control_mode


actual_pose = [0] * 7  # actual pose
ON, OFF = 1.0, 0.0
IMPEDANCE = True


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
		set_feedback(ON)
	else:
		set_feedback(OFF)


# read cartesian pose and save as actual_pose
def read_cartesian_pose(data):
	global actual_pose
	actual_pose = ['pose', data.poseStamped.pose.position.x, data.poseStamped.pose.position.y,
				   data.poseStamped.pose.position.z,
				   data.poseStamped.pose.orientation.x, data.poseStamped.pose.orientation.y,
				   data.poseStamped.pose.orientation.z, data.poseStamped.pose.orientation.w,
				   data.redundancy.status, data.redundancy.e1]


# read joy buttons and parse
def read_joy_buttons(data):

	if data.buttons[2]:
		pass

	if data.buttons[3]:
		pass

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# values force
	x_force, y_force, z_force = 10, 10, 10

	# topics
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)
	rospy.Subscriber("/joy", Joy, read_joy_buttons)
	rospy.Subscriber("/iiwa/state/CartesianPose", msg.CartesianPose, read_cartesian_pose)

	# service
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	try:
		configure_control_mode(control_mode_srv, create_msg_position_control())

		# move in cartesian impedance if True, else in position control (by default)
		if IMPEDANCE:
			x_force, y_force, z_force = 10, 10, 5
			#configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())

		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		set_feedback(OFF)
