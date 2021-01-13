#!/usr/bin/env python

import rospy

print('{ name }\t --> ' + rospy.get_param('name'))
print('{ task }\t --> ' + rospy.get_param('task'))
print('{ mode }\t --> ' + rospy.get_param('mode'))
