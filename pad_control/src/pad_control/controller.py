#!/usr/bin/env python

import rospy
from iiwa_msgs import msg, srv
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback

from teach_play.create_msgs import create_msg_cartesian_impedance, create_msg_position_control
from teach_play.services import configure_control_mode

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


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller', disable_signals=True)
	rospy.wait_for_service('/iiwa/configuration/ConfigureControlMode')

	# topics
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)

	# service
	control_mode_srv = rospy.ServiceProxy('/iiwa/configuration/ConfigureControlMode', srv.ConfigureControlMode)

	try:
		# move in cartesian impedance if True, else in position control (by default)
		if IMPEDANCE:
			x_force, y_force, z_force = 10, 10, 5
			configure_control_mode(control_mode_srv, create_msg_cartesian_impedance())
		else:
			x_force, y_force, z_force = 10, 10, 10
			configure_control_mode(control_mode_srv, create_msg_position_control())

		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		set_feedback(OFF)
