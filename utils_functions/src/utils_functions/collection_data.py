#!/usr/bin/env python

import rospy
from iiwa_msgs import msg
from functions import print_on_csv_datas, clean_file_datas

dir_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
path = dir_path + rospy.get_param('mode') + '/' + rospy.get_param('task') + '/' + rospy.get_param('rep') + '/' + rospy.get_param('name')
sample_rate = 0.1

actual_wrench = msg.CartesianWrench().wrench.force
actual_cartesian_pose = msg.CartesianPose().poseStamped.pose
'''
actual_external_joint_torque = msg.JointTorque().torque
actual_joint_position = msg.JointPosition().position
actual_joint_velocity = msg.JointVelocity().velocity
actual_joint_torque = msg.JointTorque().torque
'''


filename_wrench_csv = path + '_wrench.csv'
filename_pose_csv = path + '_pose.csv'
'''
filename_ext_torque_csv = path + '_ext_torque.csv'
filename_torque_csv = path + '_torque.csv'
filename_position_csv = path + '_joint_pos.csv'
filename_vel_csv = path + '_velocity.csv'

def read_external_joint_torque(data):
	global actual_external_joint_torque
	actual_external_joint_torque = data.torque


def read_joint_position(data):
	global actual_joint_position
	actual_joint_position = data.position


def read_joint_velocity(data):
	global actual_joint_velocity
	actual_joint_velocity = data.velocity


def read_joint_torque(data):
	global actual_joint_torque
	actual_joint_torque = data.torque
'''


def read_cartesian_wrench(data):
	global actual_wrench
	actual_wrench = data.wrench.force


def read_cartesian_pose(data):
	global actual_cartesian_pose
	actual_cartesian_pose = data.poseStamped.pose

# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':

	# init instructions
	rospy.init_node('collection_data', disable_signals=True)
	rospy.Subscriber('/iiwa/state/CartesianWrench', msg.CartesianWrench, read_cartesian_wrench)
	rospy.Subscriber('/iiwa/state/CartesianPose', msg.CartesianPose, read_cartesian_pose)
	'''
	rospy.Subscriber('/iiwa/state/ExternalJointTorque', msg.JointTorque, read_external_joint_torque)
	rospy.Subscriber('/iiwa/state/JointTorque', msg.JointTorque, read_joint_torque)
	rospy.Subscriber('/iiwa/state/JointPosition', msg.JointPosition, read_joint_position)
	rospy.Subscriber('/iiwa/state/JointVelocity', msg.JointVelocity, read_joint_velocity)
	'''

	clean_file_datas(filename_wrench_csv)
	clean_file_datas(filename_pose_csv)
	'''
	clean_file_datas(filename_ext_torque_csv)
	clean_file_datas(filename_torque_csv)
	clean_file_datas(filename_position_csv)
	clean_file_datas(filename_vel_csv)
	'''

	try:
		print_on_csv_datas(('wrench_x', 'wrench_y', 'wrench_z'), filename_wrench_csv)
		print_on_csv_datas(('position_x', 'position_y', 'position_z', 'orientation_x',
							'orientation_y', 'orientation_z', 'orientation_w'), filename_pose_csv)
		'''
		print_on_csv_datas(('a1', 'a2', 'a3', 'a4', 'a5', 'a5', 'a7'), filename_ext_torque_csv)
		print_on_csv_datas(('a1', 'a2', 'a3', 'a4', 'a5', 'a5', 'a7'), filename_torque_csv)
		print_on_csv_datas(('a1', 'a2', 'a3', 'a4', 'a5', 'a5', 'a7'), filename_position_csv)
		print_on_csv_datas(('a1', 'a2', 'a3', 'a4', 'a5', 'a5', 'a7'), filename_vel_csv)
		'''

		while True:
			rospy.sleep(sample_rate)

			# wrench
			print_on_csv_datas((actual_wrench.x, actual_wrench.y, actual_wrench.z), filename_wrench_csv)

			# cartesian pose
			print_on_csv_datas((actual_cartesian_pose.position.x, actual_cartesian_pose.position.y, actual_cartesian_pose.position.z,
				 				actual_cartesian_pose.orientation.x, actual_cartesian_pose.orientation.y,
				 				actual_cartesian_pose.orientation.z, actual_cartesian_pose.orientation.w), filename_pose_csv)
			'''
			# external torque
			print_on_csv_datas((actual_external_joint_torque.a1, actual_external_joint_torque.a2, actual_external_joint_torque.a3,
								actual_external_joint_torque.a4, actual_external_joint_torque.a5, actual_external_joint_torque.a6,
								actual_external_joint_torque.a7), filename_ext_torque_csv)

			# position
			print_on_csv_datas((actual_joint_position.a1, actual_joint_position.a2, actual_joint_position.a3,
								actual_joint_position.a4, actual_joint_position.a5, actual_joint_position.a6,
								actual_joint_position.a7), filename_position_csv)

			# velocity
			print_on_csv_datas((actual_joint_velocity.a1, actual_joint_velocity.a2, actual_joint_velocity.a3,
								actual_joint_velocity.a4, actual_joint_velocity.a5, actual_joint_velocity.a6,
								actual_joint_velocity.a7), filename_vel_csv)

			# joint torque
			print_on_csv_datas((actual_joint_torque.a1, actual_joint_torque.a2, actual_joint_torque.a3,
								actual_joint_torque.a4, actual_joint_torque.a5, actual_joint_torque.a6,
								actual_joint_torque.a7), filename_torque_csv)
			'''

	except KeyboardInterrupt:

		rospy.signal_shutdown('')
		rospy.logwarn('KeyboardInterrupt collection data...')
