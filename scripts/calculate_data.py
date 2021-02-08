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


# for every user_x.csv file save only waypoints for simplify the count
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

# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':

	'''
	# reading single csv_file
	single_file = pd.read_csv(filename_wrench_csv, squeeze=True)
	print('\n = Calculating data of {' + name + '} performing {' + task + '} at {' + rep + '} with {' + mode + '} \n')
	calculate_time_single_user(single_file)
	
	'''
	for m in range(len(modes)):
		for t in range(len(tasks)):
			calculate_time(mode=modes[m], task=tasks[t])
			print('= Calculating data of {' + tasks[t] + '} with {' + modes[m] + '}')


	# ==== PLOT DI TEMPI SU TRE RIPETIZIONI ====

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

	#save_waypoints()
