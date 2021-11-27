#! /usr/bin/env python


###
###  FOR OMNIWHEELED BOT MOVING BY PLANAR MOVE PLUGIN
###


#true and false instead of flags, using logerr,loginfo instead of print cz print is heavy

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math

class bot:
	def __init__(self):
		rospy.init_node('bot_mov')
		self.msg1=Twist()
		# self.sub = rospy.Subscriber ('/odom', Odometry, self.clbk_odom)
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	
	# def move(self):
	# 	# print("Velocity given")
	# 	self.msg1.linear.x=0.35
	# 	self.msg1.angular.z=0
	# 	self.pub.publish(self.msg1)

	def forward(self):
		# print("Velocity given")
		self.msg1.linear.y = -0.15
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)


	def back(self):
		# print("Velocity given")
		self.msg1.linear.y = 0.15
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)


	def right(self):
		# print("Velocity given")
		self.msg1.linear.x = -0.15
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)


	def left(self):
		# print("Velocity given")
		self.msg1.linear.x = 0.15
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)

	
	def slow_forward(self):
		# print("Velocity given")
		self.msg1.linear.y = -0.05
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)

	def stop(self):
		self.msg1.linear.x = 0
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)

	
	def pid(self,l,c,r):
		# pid
		pass
		
if __name__ == '__main__':
	obj=bot()
	while(1):
		obj.forward()

  # FYI, move() has to be called continuously for the bot to move 
	# obj.rotate(90)
	
