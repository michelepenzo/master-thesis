#!/usr/bin/env python

import sys, rospy
from getopt import GetoptError, getopt


def main(argv):
	try:
		opts, args = getopt(argv, "n:t:m:")
	except GetoptError:
		print('set_param.py -n <user_name> -t <task_number> -m <kt/teleop>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('set_param.py -n <user_name> -t <task_number> -m <kt/teleop>')
			sys.exit()
		elif opt in "-name":
			rospy.set_param('/name', str(arg))
			print('{ name } \t--> ' + arg)

		elif opt in "-task":
			rospy.set_param('/task', str(arg))
			print('{ task_x } \t--> ' + arg)

		elif opt in "-mode":
			rospy.set_param('/mode', str(arg))
			print('{ mode }\t--> ' + arg)


if __name__ == "__main__":
	main(sys.argv[1:])
