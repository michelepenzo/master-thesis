#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback
from iiwa_msgs import msg
from geometry_msgs.msg import Wrench

ON, OFF = 1.0, 0.0

# set feedback joypad
def set_feedback(value):
	msg, vib = JoyFeedbackArray(), JoyFeedback()
	vib.type, vib.id, vib.intensity = JoyFeedback.TYPE_RUMBLE, 1, value
	msg.array = [vib]

	pub.publish(msg)


# read external force on end effector
def read_cartesian_wrench(data):

	if abs(data.wrench.force.z) < 10 or abs(data.wrench.force.x) > 5 or abs(data.wrench.force.y) > 10:
		set_feedback(ON)
	else:
		set_feedback(OFF)

# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller', disable_signals=True)
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)

	try:
		while True:
			rospy.sleep(1)
	except KeyboardInterrupt:
		pass

	'''
	scrive nel file csv la posa quando premo pulsante
	stessa cosa viene fatta per apertura e chiusura gripper
	tasto play e chiama nodo di play
	'''
