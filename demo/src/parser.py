#!/usr/bin/env python

import yaml

# open and read the complete file
def read_yaml_file(filename):
	with open(filename, 'r') as stream:
	    try:
	        data = yaml.safe_load(stream)
	    except yaml.YAMLError as exc:
	        print(exc)

	return data


# get joint position 
def get_joit_position(data):
	joints = data['joint_position'][0].values()
	joints += data['joint_position'][1].values()
	joints += data['joint_position'][2].values()
	joints += data['joint_position'][3].values()
	joints += data['joint_position'][4].values()
	joints += data['joint_position'][5].values()
	joints += data['joint_position'][6].values()

	return joints


# get x, y, z values of cartesian pose
def get_cartesian_pose_position(data):
	temp = data['cartesian_pose'][0]['position']

	pose =  temp[0].values()
	pose += temp[1].values()
	pose += temp[2].values()

	return pose

# get x, y, z, w of cartesian orientation
def get_cartesian_pose_orientation(data):
	temp = data['cartesian_pose'][1]['orientation']

	orientation =  temp[0].values()
	orientation += temp[1].values()
	orientation += temp[2].values()
	orientation += temp[3].values()

	return orientation