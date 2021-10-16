! /usr/bin/env python

#true and false instead of flags, bot class, directly call rotate, using logerr,loginfo instead of print cz print is heavy

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math

class Bot:
	yaw=flag=0
	msg1=0
	pub=None
	'''def __init__(self):
		self.yaw=0.0
		self.flag=0.0
		self.msg1=Twist()'''
	
	def move():
		#pid
		global msg1, yaw, pub
		msg1.linear.x=0.35
		msg1.angular.z=0
		pub.publish(msg1)
		
	def get_rotation(msg):
		global yaw, flag
		print("Yaw value: ", yaw ,"& flag=", flag)
		flag = 1
		orientation_q = msg.pose.pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(_, _, yaw) = euler_from_quaternion (orientation_list)  #yaw=0.0 is north direction
    
	def rotate(targ):  
		global msg1, yaw, flag, pub
		rospy.init_node('bot_rot')
		sub = rospy.Subscriber ('/odom', Odometry, get_rotation)
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
		#target=-90
		print("Rotating to yaw %5.2f..." %targ)
		print("Flag=",flag)
		if flag==1 :
			rotate(target) 
		rate = rospy.Rate(20)
		rospy.spin()
    	while True :
			flag=0
			target_rad = targ * math.pi/180
			msg1.angular.z = kp * (target_rad-yaw)
			yaw_deg = (yaw*180/math.pi)
    
    		#if (((yaw_deg<= (targ-0.09)) and targ>=0) or ((yaw_deg>= (targ-0.09)) and targ<=0)) : #or (math.fabs(yaw_deg-targ) :
			if (round(yaw_deg) != targ) :
				pub.publish(msg1)
				print("target=%5.2f current:%5.2f" %(targ,yaw_deg))
        	
			else :    
				print("Robot successfully turned!")
				print("Final yaw:", yaw_deg)
				msg1.linear.x = 0
				msg1.angular.z = 0
				pub.publish(msg1)
				rospy.signal_shutdown("Shutting down....done!")
				break 

	if __name__ == '__main__':
		rotate(90)
