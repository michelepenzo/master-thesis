#!/usr/bin/env python

import rospy
from iiwa_msgs import msg
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback

ON, OFF = 1.0, 0.0

# set feedback joypad
def set_feedback(value):
	msg, vib = JoyFeedbackArray(), JoyFeedback()
	# id = 0, 1, 2 per la tipologia di vibrazione
	vib.type, vib.id, vib.intensity = JoyFeedback.TYPE_RUMBLE, 2, value
	msg.array = [vib]

	pub.publish(msg)


# read external force on end effector
def read_cartesian_wrench(data):
	if abs(data.wrench.force.z) < 10 or abs(data.wrench.force.x) > 10 or abs(data.wrench.force.y) > 10:
		set_feedback(ON)
	else:
		set_feedback(OFF)


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller', disable_signals=True)
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)

	# external forces, pad buttons
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)

	try:
		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		set_feedback(OFF)
