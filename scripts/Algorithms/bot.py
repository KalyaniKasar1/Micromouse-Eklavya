#! /usr/bin/env python

#true and false instead of flags, bot class, directly call rotate, using logerr,loginfo instead of print cz print is heavy

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math

class Bot:
	def __init__(self):
		self.yaw=0.0
		self.flag=0
		self.pub=None
		self.msg1=Twist()
		self.sub = rospy.Subscriber ('/odom', Odometry, self.get_rotation)
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	
	def move(self):
		#pid
		print("Velocity given")
		self.msg1.linear.x=0.35
		self.msg1.angular.z=0
		self.pub.publish(self.msg1)
		
	def get_rotation(self,msg):
		print("Yaw value: ", self.yaw ,"& flag=", self.flag)
		self.flag = 1
		orientation_q = msg.pose.pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(_, _, self.yaw) = euler_from_quaternion (orientation_list)  #yaw=0.0 is north direction
    
	def rotate(self,targ):  
		#global msg1, yaw, flag, pub
		kp=0.95
		#target=-90
		print("Rotating to yaw %5.2f..." %targ)
		print("Flag=",self.flag)
		if self.flag==1 :
			rotate(targ) 
		#rate = rospy.Rate(20)
		#rospy.spin()
		while True :
			self.flag=0
			target_rad = targ * math.pi/180
			self.msg1.angular.z = kp * (target_rad-self.yaw)
			yaw_deg = (self.yaw*180/math.pi)
    
    		#if (((yaw_deg<= (targ-0.09)) and targ>=0) or ((yaw_deg>= (targ-0.09)) and targ<=0)) : #or (math.fabs(yaw_deg-targ) :
			if (round(yaw_deg) != targ) :
				self.pub.publish(self.msg1)
				print("target=%5.2f current:%5.2f" %(targ,yaw_deg))
        	
			else :    
				print("Robot successfully turned!")
				print("Final yaw:", yaw_deg)
				self.msg1.linear.x = 0
				self.msg1.angular.z = 0
				self.pub.publish(self.msg1)
				rospy.signal_shutdown("Shutting down....done!")
				break 

if __name__ == '__main__':
	rospy.init_node('bot_rot')
	obj=Bot()
	#obj.rotate(0)
	obj.move()
	rospy.spin()
