#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
 
import math
import time

pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
regions = None

state_ = 0
error = None
now_time = 10000000
state_dict_ = {
	0: 'follow the wall',
    1: 'turn left',
    2: 'turn right',
    3: 'slow research',
    4: 'stop',
}

distance = 1
distance_turn = 0.9
distance_l = 0.5


def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 100),
        
        'front':  min(min(msg.ranges[288:431]), 100),
       
        'left':   min(min(msg.ranges[576:719]), 100),
    }

    choose_action()


def change_state(state):
    global state_, state_dict_
    if state is not state_:
        state_ = state

def choose_action():
	global regions_, regions, distance_l, distance
	
	if regions:
		prev_regions = regions

	regions = regions_
	msg = Twist()
	linear_x = 0
	angular_z = 0
   

	if regions['front'] > distance:
		if distance < 9.9:
			change_state(0)
		else:
			change_state(4)

	elif abs(regions['left'] - regions['right']) < 0.3 and (abs(regions['right'] - distance_turn) < 0.2 or abs(regions['left'] - distance_turn) < 0.2):
		if regions['front'] > distance_l:
			change_state(3)
		else:
			change_state(4)

	elif regions['left'] > regions['right']:
		change_state(1)
		rospy.loginfo(regions)
	else:
		change_state(2)

	
def follow_wall():
	global regions_, distance_l, error, now_time
	k_p = 2
	k_d = 0.8
	prev_time = 0
	prev_err = 0
	if error:
		prev_err = error
		prev_time = now_time

	time.sleep(0.02)
	error = regions_['left'] - distance_l
	now_time = rospy.Time.now().to_sec()
	delta_time = now_time - prev_time
	print(delta_time)
	msg = Twist()
	msg.linear.x = 0.6
	if delta_time == 0:
		msg.angular.z = k_p * error
	else:
		msg.angular.z = k_p * error + k_d * (error - prev_err)/delta_time
	return msg

def turn_left():
	msg = Twist()
	msg.angular.z = 0.6
	return msg

def turn_right():
	msg = Twist()
	msg.angular.z = -0.6
	return msg

def slow_mo():  
	msg = Twist()
	msg.angular.z = 0
	msg.linear.x = 0.1
	return msg

def stop():
	msg = Twist()
	msg.angular.z = 0
	msg.linear.x = 0
	return msg

def main():
	global pub_
	rospy.init_node('reading_laser')
	
	time.sleep(0.5)

	pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	
	sub = rospy.Subscriber('/base_scan', LaserScan, clbk_laser)


	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		msg = Twist()
		if state_ == 0:
			msg = follow_wall()
		elif state_ == 1:
			msg = turn_left()
		elif state_ == 2:
			msg = turn_right()
		elif state_ == 3:
			msg = slow_mo()
		elif state_ == 4:
			msg = stop()
		else:
			rospy.logerr('Unknown state!')

		pub_.publish(msg)
		print (regions_, state_)

		rate.sleep()





main()