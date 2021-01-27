#!/usr/bin/env python

import rospy

print('{ name }\t --> ' + rospy.get_param('name'))
print('{ task }\t --> ' + rospy.get_param('task'))
print('{ rep  }\t --> ' + rospy.get_param('rep'))
print('{ mode }\t --> ' + rospy.get_param('mode'))
