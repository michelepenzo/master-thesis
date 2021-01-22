#!/usr/bin/python3
# coding=utf-8

import pandas as pd
import math
import matplotlib.pyplot as plt

# root_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
root_path = '/home/michele/Documents/robotica/csv_files/'

'''
# plot test wrench with position control
filename = root_path + 'calibration_tests/test_wrench_position.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.plot(infile['wrench_z'][2500:]/10 * -1)
plt.title('Position wrench on z')
#plt.grid(True)

# plot test wrench with impendance control
filename = root_path + 'calibration_tests/test_wrench_impedance.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.plot(infile['wrench_z'][2500:]/10 * -1)
plt.title('Impedance wrench on z')

# show first plot
plt.show()

# plot trajectory in teleop
scale = 100
filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.scatter(infile['pose_x'][2:]*scale, infile['pose_y'][2:]*scale)
plt.title('Cartesian pose - teleop')

# plot trajectory in kt
filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.scatter(infile['pose_x'][2:]*scale, infile['pose_y'][2:]*scale)
plt.title('Cartesian pose - kt')

# show second plot
plt.show()

x0, x1, y0, y1 = 0, 1400, -20, 20

# wrench on EE in teleop
filename = root_path + 'teleop/test_user/eros_2_wrench.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.plot(infile['wrench_z'][0:])
plt.axis([x0, x1, y0, y1])
plt.title('Wrench on EE - teleop')

# wrench on EE in kt
filename = root_path + 'kt/test_user/eros_2_wrench.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.plot(infile['wrench_z'][0:])
plt.axis([x0, x1, y0, y1])
plt.title('Wrench on EE - kt')

# show third plot
plt.show()


# waypoints michele in teleop
scale = 100
filename = root_path + 'teleop/test_user/michele_penzo_3_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(221)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Michele - teleop')

# waypoints michele in kt
filename = root_path + 'kt/test_user/michele_penzo_3_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(222)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Michele - kt')

# waypoints eros in teleop
scale = 100
filename = root_path + 'teleop/test_user/eros_2_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(223)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Eros - teleop')

# waypoints eros in kt
filename = root_path + 'kt/test_user/eros_2_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(224)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Eros - kt')

# show plot 4
plt.show()


# plot time for completing task in teleop
infile1 = pd.read_csv(root_path + 'teleop/test_user/eros_1_wrench.csv', squeeze=True)
infile2 = pd.read_csv(root_path + 'teleop/test_user/eros_2_wrench.csv', squeeze=True)
infile3 = pd.read_csv(root_path + 'teleop/test_user/eros_3_wrench.csv', squeeze=True)
infile4 = pd.read_csv(root_path + 'teleop/test_user/eros_4_wrench.csv', squeeze=True)
infile5 = pd.read_csv(root_path + 'teleop/test_user/eros_5_wrench.csv', squeeze=True)

names = ['eros_1', 'eros_2', 'eros_3', 'eros_4', 'eros_5']
values = [infile1['wrench_x'].count(), infile2['wrench_x'].count(), infile3['wrench_x'].count(), infile4['wrench_x'].count(), infile5['wrench_x'].count()]
plt.subplot(221)
plt.bar(names, values)
plt.title('Time Eros - teleop')

# plot time for completing task in kt
infile1 = pd.read_csv(root_path + 'kt/test_user/eros_1_wrench.csv', squeeze=True)
infile2 = pd.read_csv(root_path + 'kt/test_user/eros_2_wrench.csv', squeeze=True)
infile3 = pd.read_csv(root_path + 'kt/test_user/eros_3_wrench.csv', squeeze=True)
infile4 = pd.read_csv(root_path + 'kt/test_user/eros_4_wrench.csv', squeeze=True)
infile5 = pd.read_csv(root_path + 'kt/test_user/eros_5_wrench.csv', squeeze=True)

names = ['eros_1', 'eros_2', 'eros_3', 'eros_4', 'eros_5']
values = [infile1['wrench_x'].count(), infile2['wrench_x'].count(), infile3['wrench_x'].count(), infile4['wrench_x'].count(), infile5['wrench_x'].count()]
plt.subplot(222)
plt.bar(names, values)
plt.title('Time Eros - kt')

# plot time for completing task in teleop
infile1 = pd.read_csv(root_path + 'teleop/test_user/michele_penzo_1_wrench.csv', squeeze=True)
infile2 = pd.read_csv(root_path + 'teleop/test_user/michele_penzo_2_wrench.csv', squeeze=True)
infile3 = pd.read_csv(root_path + 'teleop/test_user/michele_penzo_3_wrench.csv', squeeze=True)
infile4 = pd.read_csv(root_path + 'teleop/test_user/michele_penzo_4_wrench.csv', squeeze=True)
infile5 = pd.read_csv(root_path + 'teleop/test_user/michele_penzo_5_wrench.csv', squeeze=True)

names = ['michele_penzo_1', 'michele_penzo_2', 'michele_penzo_3', 'michele_penzo_4', 'michele_penzo_5']
values = [infile1['wrench_x'].count(), infile2['wrench_x'].count(), infile3['wrench_x'].count(), infile4['wrench_x'].count(), infile5['wrench_x'].count()]
plt.subplot(223)
plt.bar(names, values)
plt.title('Time Michele - teleop')

# plot time for completing task in kt
infile1 = pd.read_csv(root_path + 'kt/test_user/michele_penzo_1_wrench.csv', squeeze=True)
infile2 = pd.read_csv(root_path + 'kt/test_user/michele_penzo_2_wrench.csv', squeeze=True)
infile3 = pd.read_csv(root_path + 'kt/test_user/michele_penzo_3_wrench.csv', squeeze=True)
infile4 = pd.read_csv(root_path + 'kt/test_user/michele_penzo_4_wrench.csv', squeeze=True)
infile5 = pd.read_csv(root_path + 'kt/test_user/michele_penzo_5_wrench.csv', squeeze=True)

names = ['michele_penzo_1', 'michele_penzo_2', 'michele_penzo_3', 'michele_penzo_4', 'michele_penzo_5']
values = [infile1['wrench_x'].count(), infile2['wrench_x'].count(), infile3['wrench_x'].count(), infile4['wrench_x'].count(), infile5['wrench_x'].count()]
plt.subplot(224)
plt.bar(names, values)
plt.title('Time Michele - kt')

# show plot 5
plt.show()


# calculate distance teleop
def calculate_distance(infile):
	x_values = infile['pose_x'][0:]
	y_values = infile['pose_y'][0:]
	distance = 0

	for i in range(infile['pose_z'].count()-1):

		x1 = x_values[i]
		y1 = y_values[i]
		x2 = x_values[i+1]
		y2 = y_values[i+1]

		distance = distance + abs(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))

	return distance


teleop_eros = list()
teleop_michele = list()
kt_michele = list()
kt_eros = list()

filename = root_path + 'teleop/test_user/michele_penzo_1_pose.csv'
teleop_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
teleop_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/michele_penzo_3_pose.csv'
teleop_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/michele_penzo_4_pose.csv'
teleop_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/michele_penzo_5_pose.csv'
teleop_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

########################
filename = root_path + 'kt/test_user/michele_penzo_1_pose.csv'
kt_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
kt_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/michele_penzo_3_pose.csv'
kt_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/michele_penzo_4_pose.csv'
kt_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/michele_penzo_5_pose.csv'
kt_michele.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

########################
filename = root_path + 'kt/test_user/eros_1_pose.csv'
kt_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/eros_2_pose.csv'
kt_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/eros_3_pose.csv'
kt_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/eros_4_pose.csv'
kt_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'kt/test_user/eros_5_pose.csv'
kt_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

########################
filename = root_path + 'teleop/test_user/eros_1_pose.csv'
teleop_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/eros_2_pose.csv'
teleop_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/eros_3_pose.csv'
teleop_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/eros_4_pose.csv'
teleop_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

filename = root_path + 'teleop/test_user/eros_5_pose.csv'
teleop_eros.append(calculate_distance(pd.read_csv(filename, squeeze=True)))

#########
names = ['#1', '#2', '#3', '#4', '#5']

plt.subplot(221)
plt.ylim(0, 5)
plt.ylabel('Distanza in metri')
plt.bar(names, teleop_eros)
plt.title('Distanza Michele - teleop')

plt.subplot(222)
plt.ylim(0, 5)
plt.ylabel('Distanza in metri')
plt.bar(names, teleop_michele)
plt.title('Distanza Eros - teleop')

plt.subplot(223)
plt.ylim(0, 5)
plt.ylabel('Distanza in metri')
plt.bar(names, kt_michele)
plt.title('Distanza Michele - kt')

plt.subplot(224)
plt.ylim(0, 5)
plt.ylabel('Distanza in metri')
plt.bar(names, kt_eros)
plt.title('Distanza Eros - kt')

plt.show()
'''

def calculate_acceleartion(infile):
	x_values = infile['pose_x'][0:]
	y_values = infile['pose_y'][0:]
	acceleration = list()
	time = 0.1

	for i in range(infile['pose_z'].count()-1):

		x1 = x_values[i]
		y1 = y_values[i]
		x2 = x_values[i + 1]
		y2 = y_values[i + 1]

		# distance from two points
		value = abs(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))) / (time**2)
		acceleration.append(value)

	return acceleration


# return acceleration
'''
filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
plt.subplot(221)
plt.xlim(0, 1)
plt.boxplot(calculate_acceleartion(pd.read_csv(filename, squeeze=True)), showfliers=False,  vert=False)
plt.title('Accelerazione PTP Michele - kt')

filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
plt.subplot(222)
plt.xlim(0, 1)
plt.boxplot(calculate_acceleartion(pd.read_csv(filename, squeeze=True)), showfliers=False,  vert=False)
plt.title('Accelerazione PTP Michele - teleop')


filename = root_path + 'kt/test_user/eros_2_pose.csv'
plt.subplot(223)
plt.xlim(0, 1)
plt.boxplot(calculate_acceleartion(pd.read_csv(filename, squeeze=True)), showfliers=False,  vert=False)
plt.title('Accelerazione PTP Eros - kt')


filename = root_path + 'teleop/test_user/eros_2_pose.csv'
plt.subplot(224)
plt.xlim(0, 1)
plt.boxplot(calculate_acceleartion(pd.read_csv(filename, squeeze=True)), showfliers=False,  vert=False)
plt.title('Accelerazione PTP Eros - teleop')

plt.show()
'''
filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
kt_michele = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
teleop_michele = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

filename = root_path + 'kt/test_user/eros_2_pose.csv'
kt_eros = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

filename = root_path + 'teleop/test_user/eros_2_pose.csv'
teleop_eros = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

fig, ax = plt.subplots()
_labels = ('kt michele', 'teleop michele', 'kt eros', 'teleop eros')
plt.ylabel('accelerazione m/s^2')
plt.xlabel('2° trial in tutte le modalita')
ax.boxplot((kt_michele, teleop_michele, kt_eros, teleop_eros), showfliers=False, labels=_labels)
plt.show()
