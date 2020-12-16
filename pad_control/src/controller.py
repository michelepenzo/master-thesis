#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback
from iiwa_msgs import msg

ON, OFF = 1.0, 0.0

# set feedback joypad
def set_feedback(value):
	rum = JoyFeedback()
	msg = JoyFeedbackArray()

	rum.type, rum.id, rum.intensity = JoyFeedback.TYPE_RUMBLE, 1, value
	msg.array = [rum]

	pub.publish(msg)
	rospy.logwarn(msg)


# read external force on robot joints
def read_external_force(data):
	#rospy.logwarn(data.torque)
	pass


'''
scrive nel file csv la posa quando premo pulsante
stessa cosa viene fatta per apertura e chiusura gripper
tasto play e chiama nodo di play
'''


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':

	# init instructions
	rospy.init_node('controller', disable_signals=True)
	pub = rospy.Publisher('/joy/set_feedback', JoyFeedbackArray, queue_size=1)
	sub = rospy.Subscriber('/iiwa/state/ExternalJointTorque', msg.JointTorque, read_external_force)

	try:

		set_feedback(ON)

		while True:
			rospy.sleep(1)

	except KeyboardInterrupt:
		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt controller...')
