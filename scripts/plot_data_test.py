#!/usr/bin/python3
# coding=utf-8

import pandas as pd
import math
import matplotlib.pyplot as plt

# root_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
root_path = '/home/michele/Documents/robotica/csv_files/'
plt.rcParams.update({'font.size': 30})


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

		if x1 == 0.0 and y1 == 0.0:
			pass
		else:
			# distance from two points
			value = abs(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))) / (time) # TODO ora è velocità
			acceleration.append(value)

	return acceleration



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


filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
kt_michele = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
teleop_michele = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

filename = root_path + 'kt/test_user/eros_2_pose.csv'
kt_eros = calculate_acceleartion(pd.read_csv(filename, squeeze=True))

filename = root_path + 'teleop/test_user/eros_2_pose.csv'
teleop_eros = calculate_acceleartion(pd.read_csv(filename, squeeze=True))


# BOXPLOT VELOCITÀ
fig, ax = plt.subplots()
_labels = ('kt michele', 'teleop michele', 'kt eros', 'teleop eros')
plt.ylabel('velocita m/s')
plt.xlabel('2° trial in tutte le modalita')
ax.boxplot((kt_michele, teleop_michele, kt_eros, teleop_eros), showfliers=False, labels=_labels)
plt.show()


plt.subplot(211)
plt.ylim(0, 0.6)
plt.xlim(0, 1600)
plt.plot(teleop_michele)
plt.xlabel('teleop michele')
plt.ylabel('velocita in m/s')


plt.subplot(212)
plt.ylim(0, 0.6)
plt.xlim(0, 1600)
plt.plot(kt_michele)
plt.xlabel('kt michele')
plt.ylabel('velocita in m/s')

plt.show()

plt.axis('equal')
# altezza
#labels = ['171 - 180 cm', '181 - 190 cm']
#values = [8,2]

# peso
#labels = ['51-60 kg','61-70 kg','71-80 kg','81-90 kg', '>90']
#values = [2,4,2,1,1]

# età
#labels = ['23','24','25','26','27']
#values = [1,3,3,2,1]

# pad use
#labels = ['More than once a week', 'A few times a month', 'One a year', "I've never used it"]
#values = [1,4,4,1]

plt.pie(values, labels=labels, autopct='%0.f%%')
plt.legend()
plt.show()

'''
labels = ['t1-r1','t1-r2','t1-r3','t2-r1','t2-r2','t2-r3']
#values = [4, 4, 0, 1, 0, 3]
values = [3, 3, 1, 1, 1, 2]	# collision

# tutto
plt.bar(labels, values, width=0.8, align='center')
plt.xlim(-1, 6)
plt.xticks(range(6))
plt.yticks(range(4))

plt.show()
'''

mental_kt =     [2,6,3,4,8,1,3,3,2,1] #[1,1,2,3,3,4,6,8,8,9]
mental_teleop = [9,7,8,5,6,8,5,7,8,2] #[1,2,2,5,5,6,7,7,8,9]

physical_kt =     [6,6,3,6,5,3,5,2,7,7] #[1,2,3,3,5,5,6,6,7,7]
physical_teleop = [1,1,1,2,1,1,1,1,1,2] #[1,1,1,1,1,1,1,2,2,6]


plt.boxplot([physical_kt, physical_teleop], labels=['kinesthetic', 'teleoperation'])
# stress
# plt.boxplot([1,2,3,4,4,4,5,5,6,7], labels=[''])
plt.yticks(range(11))
plt.show()
'''
