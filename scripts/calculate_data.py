#!/usr/bin/env python3
# coding=utf-8

import math, csv
import matplotlib.pyplot as plt
import pandas as pd

sample_rate = 0.1

# LOCAL
path = '/home/michele/Documents/robotica/csv_files/'
users = ['user_1', 'user_2', 'user_3', 'user_4', 'user_5', 'user_6', 'user_7', 'user_8', 'user_9', 'user_10']
reps = ['rep_1', 'rep_2', 'rep_3']
tasks = ['task_2', 'task_3']
modes = ['kt', 'teleop']


def clean_file(filename):
	with open(filename, 'w') as _:
		pass


def print_on_csv(filename, data):
	with open(filename, 'a+') as outfile:
		wr = csv.writer(outfile, quoting=csv.QUOTE_NONE)
		wr.writerow(data)


def calculate_time_single_user(s):
	n_values = s['wrench_x'].count()

	# print(' = Number of sample: ' + str(n_values))

	m, sec = divmod(n_values * sample_rate, 60)
	h, m = divmod(m, 60)
	# print(' = Task time: ' + ('{:.0f} min {:.0f} sec'.format(m, sec)))

	# return min and secs
	# return '{:.0f} min {:.0f} sec\n'.format(m, sec)

	# return n_sample
	return n_values


def calculate_time(mode, task):
	times_csv = path + 'results/times/' + mode + '_' + task + '_' + 'times.csv'
	out = list()
	clean_file(times_csv)
	print_on_csv(times_csv, (users))

	for r in range(len(reps)):
		for u in range(len(users)):
			filename = path + mode + '/' + task + '/' + reps[r] + '/' + users[u]
			s = pd.read_csv(filename + '_wrench.csv', squeeze=True)

			out.append(calculate_time_single_user(s))

		out.insert(0, reps[r])
		print_on_csv(times_csv, out)
		out.clear()


def save_waypoints():
	n_file = 0

	for m in range(len(modes)):
		for t in range(len(tasks)):
			for r in range(len(reps)):
				for u in range(len(users)):

					filename = path + modes[m] + '/' + tasks[t] + '/' + reps[r] + '/' + users[u] + '.csv'
					filename_wp = path + modes[m] + '/' + tasks[t] + '/' + reps[r] + '/' + users[u] + '_waypoints.csv'
					with open(filename, 'r') as f:
						with open(filename_wp, 'w') as fwp:
							for line in f.readlines():
								if 'pose' in line:
									fwp.write(line)

					n_file += 1

	print(n_file)


def calculate_distance(infile):
	x_values = infile['position_x'][0:]
	y_values = infile['position_y'][0:]
	distance = 0

	for i in range(infile['position_z'].count()-1):

		x1 = x_values[i]
		y1 = y_values[i]
		x2 = x_values[i+1]
		y2 = y_values[i+1]

		distance = distance + abs(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))

	return distance

# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':
	plt.rcParams.update({'font.size': 30})

	'''
	for m in range(len(modes)):
		for t in range(len(tasks)):
			calculate_time(mode=modes[m], task=tasks[t])
			print('= Calculating data of {' + tasks[t] + '} with {' + modes[m] + '}')
	'''

	# test traiettoria
	'''
	scale = 100
	task = 'task_2'
	user = users[3]

	filename = path + 'teleop/' + task + '/' + reps[0] + '/' + user + '_pose.csv'
	infile = pd.read_csv(filename, squeeze=True)
	plt.subplot(221)
	plt.title('rep1')
	plt.scatter(infile['position_x'][2:] * scale, infile['position_y'][2:] * scale)

	filename = path + 'teleop/' + task  + '/' + reps[1] + '/' + user + '_pose.csv'
	infile = pd.read_csv(filename, squeeze=True)
	plt.subplot(222)
	plt.title('rep2')
	plt.scatter(infile['position_x'][2:] * scale, infile['position_y'][2:] * scale)

	filename = path + 'teleop/' + task + '/' + reps[2] + '/' + user + '_pose.csv'
	infile = pd.read_csv(filename, squeeze=True)
	plt.subplot(223)
	plt.title('rep3')
	plt.scatter(infile['position_x'][2:] * scale, infile['position_y'][2:] * scale)

	plt.show()
	'''


	# ==== PLOT DI TEMPI SU TRE RIPETIZIONI ====
	'''
	# task2, teleop
	times_csv = path + 'results/times/' + modes[1] + '_' + tasks[0] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)
	plt.subplot(221)
	plt.ylim(0, 3000)
	plt.plot(s['user_1']); plt.plot(s['user_2']); plt.plot(s['user_3']); plt.plot(s['user_4']); plt.plot(s['user_5'])
	plt.plot(s['user_6']); plt.plot(s['user_7']); plt.plot(s['user_8']); plt.plot(s['user_9']); plt.plot(s['user_10'])
	plt.title('task2, teleop')

	# task3, teleop
	times_csv = path + 'results/times/' + modes[1] + '_' + tasks[1] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	plt.subplot(222)
	plt.ylim(0, 3000)
	plt.plot(s['user_1']); plt.plot(s['user_2']); plt.plot(s['user_3']); plt.plot(s['user_4']); plt.plot(s['user_5'])
	plt.plot(s['user_6']); plt.plot(s['user_7']); plt.plot(s['user_8']);plt.plot(s['user_9']); plt.plot(s['user_10'])
	plt.title('task3, teleop')

	# task2, kt
	times_csv = path + 'results/times/' + modes[0] + '_' + tasks[0] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)
	plt.subplot(223)
	plt.ylim(0, 3000)
	plt.plot(s['user_1']); plt.plot(s['user_2']); plt.plot(s['user_3']); plt.plot(s['user_4']); plt.plot(s['user_5'])
	plt.plot(s['user_6']); plt.plot(s['user_7']); plt.plot(s['user_8']); plt.plot(s['user_9']); plt.plot(s['user_10'])
	plt.title('task2, kt')

	# task3, kt
	times_csv = path + 'results/times/' + modes[0] + '_' + tasks[1] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)
	plt.subplot(224)
	plt.ylim(0, 3000)
	plt.plot(s['user_1']); plt.plot(s['user_2']); plt.plot(s['user_3']); plt.plot(s['user_4']); plt.plot(s['user_5'])
	plt.plot(s['user_6']); plt.plot(s['user_7']); plt.plot(s['user_8']);plt.plot(s['user_9']); plt.plot(s['user_10'])
	plt.title('task3, kt')
	plt.show()
	'''


	# ==== PLOT TEMPO GRUPPO GIOCO in TELEOP ====
	'''
	times_gamer = list()
	times_gamer_ = list()
	times_non_gamer = list()
	times_non_gamer_ = list()
	
	# times teleop, task2
	
	times_csv = path + 'results/times/' + modes[1] + '_' + tasks[0] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	#times_gamer.append(s['user_10'][0]);
	times_gamer.append(s['user_10'][1]); times_gamer.append(s['user_10'][2])
	times_gamer.append(s['user_3'][0]); times_gamer.append(s['user_3'][1]); times_gamer.append(s['user_3'][2])
	times_gamer.append(s['user_5'][0]); times_gamer.append(s['user_5'][2])
	times_gamer.append(s['user_7'][0])
	times_gamer.append(s['user_9'][1]); times_gamer.append(s['user_9'][2])
	
	times_non_gamer.append(s['user_1'][0]); times_non_gamer.append(s['user_1'][1]); times_non_gamer.append(s['user_1'][2])
	times_non_gamer.append(s['user_2'][1]); times_non_gamer.append(s['user_2'][2])
	times_non_gamer.append(s['user_6'][0]); times_non_gamer.append(s['user_6'][1]); times_non_gamer.append(s['user_6'][2])
	times_non_gamer.append(s['user_4'][0]); times_non_gamer.append(s['user_4'][1]); times_non_gamer.append(s['user_4'][2]);
	times_non_gamer.append(s['user_8'][0]); times_non_gamer.append(s['user_8'][2])

	plt.boxplot([times_gamer, times_non_gamer], labels=['Group 1', 'Group 2'])
	plt.ylabel('Time in ms')
	plt.ylim(750, 3000)
	plt.show()


	# times teleop, task3
	
	times_csv = path + 'results/times/' + modes[1] + '_' + tasks[1] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	times_gamer.append(s['user_10'][0]); times_gamer.append(s['user_10'][1]); times_gamer.append(s['user_10'][2])
	times_gamer.append(s['user_3'][0]); times_gamer.append(s['user_3'][1]); times_gamer.append(s['user_3'][2])
	times_gamer.append(s['user_5'][0]); times_gamer.append(s['user_5'][1]); times_gamer.append(s['user_5'][2])
	times_gamer.append(s['user_7'][0]); times_gamer.append(s['user_7'][1]); times_gamer.append(s['user_7'][2])
	#times_gamer.append(s['user_9'][0]);
	times_gamer.append(s['user_9'][2])

	times_non_gamer.append(s['user_1'][0]); times_non_gamer.append(s['user_1'][1])
	times_non_gamer.append(s['user_2'][0]); times_non_gamer.append(s['user_2'][1])
	times_non_gamer.append(s['user_4'][1]); times_non_gamer.append(s['user_4'][2])
	times_non_gamer.append(s['user_6'][0]); times_non_gamer.append(s['user_6'][1]); times_non_gamer.append(s['user_6'][2])
	times_non_gamer.append(s['user_8'][0]); times_non_gamer_.append(s['user_8'][1]); times_non_gamer.append(s['user_8'][2])

	

	plt.boxplot([times_gamer, times_non_gamer], labels=['Group 1', 'Group 2'])
	plt.ylabel('Time in ms')
	plt.ylim(750, 3000)
	plt.show()
	

	print(times_gamer)
	print(sum(times_gamer) / len(times_gamer))
	print(times_non_gamer)
	print(sum(times_non_gamer) / len(times_non_gamer))
	'''


	# ==== PLOT DISTANZA GRUPPO GIOCO in TELOP ====
	'''
	# TODO occhio ai valori che vengono rimossi
	distance_gamer, distance_non_gamer = list(), list()

	# solo per il task 3
	for r in range(len(reps)):
		for u in range(len(users)):
			filename = path + 'teleop/' + tasks[1] + '/' + reps[r] + '/' + users[u] + '_pose.csv'
			distance = calculate_distance(pd.read_csv(filename, squeeze=True))

			#print(reps[r] + ' of ' + users[u] + ' : ' + str(distance))

			if users[u] == 'user_10' or users[u] == 'user_3' or users[u] == 'user_5' or users[u] == 'user_7' or users[u] == 'user_9':
				# gamer
				distance_gamer.append(distance)
			else:
				# non gamer
				distance_non_gamer.append(distance)

	# task2
	
	distance_non_gamer.remove(0.6844725893251613)# rep1 user2
	distance_gamer.remove(0.4380864179569224)# rep1 user7
	distance_gamer.remove(1.6924190995155661)# rep2 user5
	distance_non_gamer.remove(0.43319235494644426)# rep2 user8
	distance_gamer.remove(1.1301061640893995)# rep1 user9
	distance_gamer.remove(0.7426055344428442)# rep1 user7
	

	# task3
	distance_non_gamer.remove(0.48245662932542177)# rep3 user1
	distance_non_gamer.remove(1.2009031824808087)#rep3 user2
	distance_non_gamer.remove(0.7958873639893409)#rep1 user4
	distance_gamer.remove(0.5856682170874384)# rep2 user9



	#print(distance_gamer)
	print(sum(distance_gamer) / len(distance_gamer))

	#print(distance_non_gamer)
	print(sum(distance_non_gamer) / len(distance_non_gamer))

	plt.boxplot([distance_gamer, distance_non_gamer], labels=['Group 1', 'Group 2'])
	plt.ylabel('Distance in mt')
	plt.ylim(1.4, 2.8)
	plt.show()
	'''


	# ==== PLOT TEMPO GRUPPO GIOCO in KT ====
	'''
	times_gamer = list()
	times_gamer_ = list()
	times_non_gamer = list()
	times_non_gamer_ = list()


	# times kt, task3 e task3

	times_csv = path + 'results/times/' + modes[0] + '_' + tasks[0] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	times_gamer.append(s['user_10'][0]); times_gamer.append(s['user_10'][1]); times_gamer.append(s['user_10'][2])
	times_gamer.append(s['user_3'][0]); times_gamer.append(s['user_3'][1]); times_gamer.append(s['user_3'][2])
	times_gamer.append(s['user_5'][0]); times_gamer.append(s['user_5'][1]); times_gamer.append(s['user_5'][2])
	times_gamer.append(s['user_7'][0]); times_gamer.append(s['user_7'][1]); times_gamer.append(s['user_7'][2])
	times_gamer.append(s['user_9'][0]); times_gamer.append(s['user_9'][1]); times_gamer.append(s['user_9'][2])

	times_non_gamer.append(s['user_1'][0]); times_non_gamer.append(s['user_1'][1]); times_non_gamer.append(s['user_1'][2])
	times_non_gamer.append(s['user_2'][0]); times_non_gamer.append(s['user_2'][1]); times_non_gamer.append(s['user_2'][2])
	times_non_gamer.append(s['user_4'][1]);	times_non_gamer.append(s['user_4'][2]); times_non_gamer.append(s['user_4'][2])
	times_non_gamer.append(s['user_6'][0]); times_non_gamer.append(s['user_6'][1]);times_non_gamer.append(s['user_6'][2])
	times_non_gamer.append(s['user_8'][0]); times_non_gamer_.append(s['user_8'][1]);times_non_gamer.append(s['user_8'][2])

	plt.boxplot([times_gamer, times_non_gamer], labels=['Group 1', 'Group 2'])
	plt.ylabel('Time in ms')
	plt.ylim(300, 2000)
	plt.show()

	print(sum(times_gamer) / len(times_gamer))
	print(sum(times_non_gamer) / len(times_non_gamer))
	'''


	# ==== PLOT DISTANZA GRUPPO GIOCO in TELOP ====
	'''
	distance_gamer, distance_non_gamer = list(), list()

	# solo per il task 3
	for r in range(len(reps)):
		for u in range(len(users)):
			filename = path + 'kt/' + tasks[0] + '/' + reps[r] + '/' + users[u] + '_pose.csv'
			distance = calculate_distance(pd.read_csv(filename, squeeze=True))

			#print(reps[r] + ' of ' + users[u] + ' : ' + str(distance))

			if users[u] == 'user_10' or users[u] == 'user_3' or users[u] == 'user_5' or users[u] == 'user_7' or users[u] == 'user_9':
				# gamer
				distance_gamer.append(distance)
			else:
				# non gamer
				distance_non_gamer.append(distance)


	print(sum(distance_gamer) / len(distance_gamer))
	print(distance_gamer)
	print(sum(distance_non_gamer) / len(distance_non_gamer))
	print(distance_non_gamer)

	plt.boxplot([distance_gamer, distance_non_gamer], labels=['Group 1', 'Group 2'])
	plt.ylabel('Distance in mt')
	plt.ylim(1, 4)
	plt.show()
	'''

	times_kt = list()
	times_tt = list()

	# ==== PLOT TEMPO GRUPPO INIZIO in TELOP ====

	# times teleop, task2
	times_csv = path + 'results/times/' + modes[1] + '_' + tasks[0] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)


	times_kt.append(s['user_5'][0]); times_kt.append(s['user_5'][2])
	times_kt.append(s['user_3'][0]); times_kt.append(s['user_3'][1]); times_kt.append(s['user_3'][2])
	#times_kt.append(s['user_8'][0]); times_kt.append(s['user_8'][2])
	times_kt.append(s['user_9'][1]); times_kt.append(s['user_9'][2])
	times_kt.append(s['user_10'][1]); times_kt.append(s['user_10'][2]) # manca rep0

	times_tt.append(s['user_7'][0])
	times_tt.append(s['user_1'][0]); times_tt.append(s['user_1'][1]); times_tt.append(s['user_1'][2])
	times_tt.append(s['user_2'][1]); times_tt.append(s['user_2'][2])
	times_tt.append(s['user_6'][0]); times_tt.append(s['user_6'][1]); times_tt.append(s['user_6'][2])
	#times_tt.append(s['user_4'][0]); times_tt.append(s['user_4'][1]); times_tt.append(s['user_4'][2]);

	
	plt.boxplot([times_kt, times_tt], labels=['Group 1', 'Group 2'])

	plt.ylabel('Time in ms')
	plt.ylim(750, 3000)
	plt.show()

	'''
	# times teleop, task3
	
	times_csv = path + 'results/times/' + modes[1] + '_' + tasks[1] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	# AMEDEO
	times_kt.append(s['user_5'][0]); times_kt.append(s['user_5'][1]); times_kt.append(s['user_5'][2])
	times_kt.append(s['user_3'][0]); times_kt.append(s['user_3'][1]); times_kt.append(s['user_3'][2])
	times_kt.append(s['user_8'][0]); times_kt.append(s['user_8'][1]); times_kt.append(s['user_8'][2])
	#times_kt.append(s['user_9'][2]); times_kt.append(s['user_9'][0])
	times_kt.append(s['user_10'][0]); times_kt.append(s['user_10'][1]); times_kt.append(s['user_10'][2])

	# CARLO
	times_tt.append(s['user_1'][0]); times_tt.append(s['user_1'][1])
	times_tt.append(s['user_2'][0]); times_tt.append(s['user_2'][1])
	times_tt.append(s['user_7'][0]); times_tt.append(s['user_7'][1]); times_tt.append(s['user_7'][2])
	times_tt.append(s['user_4'][1]); times_tt.append(s['user_4'][2])
	#times_tt.append(s['user_6'][0]); times_tt.append(s['user_6'][1]); times_tt.append(s['user_6'][2])

	plt.boxplot([times_kt, times_tt], labels=['Group 1', 'Group 2'])
	plt.ylabel('Time in ms')
	plt.ylim(750, 3000)
	plt.show()
	'''


	# ==== PLOT TEMPO GRUPPO STAZZA in KT ====
	'''
	# times kt, task3 e task3
	
	times_csv = path + 'results/times/' + modes[0] + '_' + tasks[0] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	# gruppo di AMEDEO
	times_kt.append(s['user_5'][0]); times_kt.append(s['user_5'][1]); times_kt.append(s['user_5'][2])
	times_kt.append(s['user_3'][0]); times_kt.append(s['user_3'][1]); times_kt.append(s['user_3'][2])
	times_kt.append(s['user_8'][0]); times_kt.append(s['user_8'][1]); times_kt.append(s['user_8'][2])
	times_kt.append(s['user_9'][0]); times_kt.append(s['user_9'][1]); times_kt.append(s['user_9'][2])
	times_kt.append(s['user_10'][0]); times_kt.append(s['user_10'][1]); times_kt.append(s['user_10'][2])

	# gruppo di CARLO
	times_tt.append(s['user_1'][0]); times_tt.append(s['user_1'][1]); times_tt.append(s['user_1'][2])
	times_tt.append(s['user_2'][0]); times_tt.append(s['user_2'][1]); times_tt.append(s['user_2'][2])
	times_tt.append(s['user_7'][0]); times_tt.append(s['user_7'][1]); times_tt.append(s['user_7'][2])
	times_tt.append(s['user_4'][0]); times_tt.append(s['user_4'][2]); times_tt.append(s['user_4'][2])
	times_tt.append(s['user_6'][0]); times_tt.append(s['user_6'][2]) 
	times_tt.append(s['user_6'][1]) # TODO sbagliata la seconda rip


	plt.boxplot([times_kt, times_tt], labels=['Group 1', 'Group 2'])
	plt.ylabel('Time in ms')
	#plt.ylim(300, 2000)
	plt.show()
	'''


	try:
		print('piccoli - grandi')
		print(times_kt)
		print(times_tt)
		#print(sum(times_kt) / len(times_kt))
		#print(sum(times_tt) / len(times_tt))
	except ZeroDivisionError:
		pass

	# ==== PLOT FORZE ====
	'''
	x0, x1, y0, y1 = 0, 1400, -20, 20
	filename = path + 'kt/task_2/rep_3/user_10_wrench.csv'
	infile = pd.read_csv(filename, squeeze=True)
	#plt.subplot(211)
	plt.plot(infile['wrench_z'][0:])
	print('wrench x ' + str(sum(infile['wrench_x'][0:]) / len(infile['wrench_x'][0:])))
	print('wrench y ' + str(sum(infile['wrench_y'][0:]) / len(infile['wrench_y'][0:])))
	print('wrench z ' + str(sum(infile['wrench_z'][0:]) / len(infile['wrench_z'][0:])))
	#plt.axis([x0, x1, y0, y1])
	#plt.title('Amedeo')

	filename = path + 'kt/task_2/rep_3/user_6_wrench.csv'
	infile = pd.read_csv(filename, squeeze=True)
	#plt.subplot(212)
	plt.plot(infile['wrench_z'][0:])
	print('wrench x ' + str(sum(infile['wrench_x'][0:]) / len(infile['wrench_x'][0:])))
	print('wrench y ' + str(sum(infile['wrench_y'][0:]) / len(infile['wrench_y'][0:])))
	print('wrench z ' + str(sum(infile['wrench_z'][0:]) / len(infile['wrench_z'][0:])))
	plt.axis([x0, x1, y0, y1])
	plt.title('Carlo')

	# show third plot
	plt.show()
	'''


	# ==== CALCOLO STD ====
	'''
	times = list()
	import numpy as np

	# times teleop, task2
	times_csv = path + 'results/times/' + modes[0] + '_' + tasks[1] + '_' + 'times.csv'
	s = pd.read_csv(times_csv, squeeze=True)

	id = 'user_10'
	times.append(s[id][0])
	times.append(s[id][1])
	times.append(s[id][2])
	print(np.std(times))
	'''
