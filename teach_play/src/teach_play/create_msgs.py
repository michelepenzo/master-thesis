import rospy
from iiwa_msgs import msg


def create_movement_cartesian_pose(move):
	movement = msg.CartesianPose()

	movement.poseStamped.header.seq = 1
	movement.poseStamped.header.stamp = rospy.Time.now()
	movement.poseStamped.header.frame_id = 'iiwa_link_0'

	movement.poseStamped.pose.position.x = move[0]
	movement.poseStamped.pose.position.y = move[1]
	movement.poseStamped.pose.position.z = move[2]

	movement.poseStamped.pose.orientation.x = move[3]
	movement.poseStamped.pose.orientation.y = move[4]
	movement.poseStamped.pose.orientation.z = move[5]
	movement.poseStamped.pose.orientation.w = move[6]

	movement.redundancy.status = move[7]
	movement.redundancy.e1 = move[8]

	return movement


# create service msg (STANDARD)
def create_msg_control_mode(control_mode,
							joint_stiffness, joint_damping,
							cartesian_stiffness, cartesian_damping, nullspace_stiffness, nullspace_damping,
							df_cartesian_dof, desired_force, desired_stiffness,
							s_cartesian_dof, frequency, amplitude, stiffness,
							max_path_deviation, max_control_force, max_control_force_stop,
							max_cartesian_velocity):  # limits

	# TODO sistemare i parametri che non vengono utilizzati

	joint_impedance = msg.JointImpedanceControlMode()
	joint_impedance.joint_stiffness.a1 = joint_stiffness[0]
	joint_impedance.joint_stiffness.a2 = joint_stiffness[1]
	joint_impedance.joint_stiffness.a3 = joint_stiffness[2]
	joint_impedance.joint_stiffness.a4 = joint_stiffness[3]
	joint_impedance.joint_stiffness.a5 = joint_stiffness[4]
	joint_impedance.joint_stiffness.a6 = joint_stiffness[5]
	joint_impedance.joint_stiffness.a7 = joint_stiffness[6]

	joint_impedance.joint_damping.a1 = joint_damping[0]
	joint_impedance.joint_damping.a2 = joint_damping[1]
	joint_impedance.joint_damping.a3 = joint_damping[2]
	joint_impedance.joint_damping.a4 = joint_damping[3]
	joint_impedance.joint_damping.a5 = joint_damping[4]
	joint_impedance.joint_damping.a6 = joint_damping[5]
	joint_impedance.joint_damping.a7 = joint_damping[6]

	# --------------------------------------------------------------------------

	cartesian_impedance = msg.CartesianImpedanceControlMode()

	cartesian_impedance.cartesian_stiffness.x = cartesian_stiffness[0]
	cartesian_impedance.cartesian_stiffness.y = cartesian_stiffness[1]
	cartesian_impedance.cartesian_stiffness.z = cartesian_stiffness[2]
	cartesian_impedance.cartesian_stiffness.a = cartesian_stiffness[3]
	cartesian_impedance.cartesian_stiffness.b = cartesian_stiffness[4]
	cartesian_impedance.cartesian_stiffness.c = cartesian_stiffness[5]

	cartesian_impedance.cartesian_damping.x = cartesian_damping[0]
	cartesian_impedance.cartesian_damping.y = cartesian_damping[1]
	cartesian_impedance.cartesian_damping.z = cartesian_damping[2]
	cartesian_impedance.cartesian_damping.a = cartesian_damping[3]
	cartesian_impedance.cartesian_damping.b = cartesian_damping[4]
	cartesian_impedance.cartesian_damping.c = cartesian_damping[5]

	cartesian_impedance.nullspace_stiffness = nullspace_stiffness
	cartesian_impedance.nullspace_damping = nullspace_damping

	# --------------------------------------------------------------------------

	desired_force = msg.DesiredForceControlMode()
	sine_pattern = msg.SinePatternControlMode()
	limits = msg.CartesianControlModeLimits()

	return control_mode, joint_impedance, cartesian_impedance, desired_force, sine_pattern, limits


# create msg for position control
def create_msg_position_control():
	return create_msg_control_mode(
		control_mode=0,
		joint_stiffness=[0.0] * 7, joint_damping=[0.0] * 7,
		cartesian_stiffness=[0.0] * 6, cartesian_damping=[0.0] * 6, nullspace_stiffness=0.0, nullspace_damping=0.0,
		df_cartesian_dof=0, desired_force=0.0, desired_stiffness=0.0,
		s_cartesian_dof=0, frequency=0.0, amplitude=0.0, stiffness=0.0,
		max_path_deviation=[0.0] * 6, max_control_force=[0.0] * 6, max_control_force_stop=False,
		max_cartesian_velocity=[0.0] * 6)


# create msg for joint impendance (fake hand guide values)
def create_msg_joint_impedance():
	return create_msg_control_mode(
		control_mode=1,
		joint_stiffness=[2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0], joint_damping=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
		cartesian_stiffness=[0.0] * 6, cartesian_damping=[0.0] * 6, nullspace_stiffness=0.0, nullspace_damping=0.0,
		df_cartesian_dof=0, desired_force=0.0, desired_stiffness=0.0,
		s_cartesian_dof=0, frequency=0.0, amplitude=0.0, stiffness=0.0,
		max_path_deviation=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], max_control_force=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		max_control_force_stop=False, max_cartesian_velocity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


# create msg cartesian_impedance
def create_msg_cartesian_impedance():
	return create_msg_control_mode(
		control_mode=2,
		joint_stiffness=[0.0] * 7, joint_damping=[0.0] * 7,
		cartesian_stiffness=[1500, 700, 2500, 100, 100, 100], cartesian_damping=[0.0] * 6, nullspace_stiffness=0.0,
		nullspace_damping=0.0,
		df_cartesian_dof=0, desired_force=0.0, desired_stiffness=0.0,
		s_cartesian_dof=0, frequency=0.0, amplitude=0.0, stiffness=0.0,
		max_path_deviation=[0.0] * 6, max_control_force=[0.0] * 6, max_control_force_stop=False,
		max_cartesian_velocity=[0.0] * 6)
