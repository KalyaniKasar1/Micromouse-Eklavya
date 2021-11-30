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
	dir = 0  #by default internal direction is towards north, direction is chosen from the below list
	dirs = ['N', 'E', 'S', 'W']  # correspond to the north, west, south & east, OR forward, right, back, left
	def __init__(self):
		rospy.init_node('bot_mov')
		self.msg1=Twist()
		# self.sub = rospy.Subscriber ('/odom', Odometry, self.clbk_odom)
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	
	def move(self):
		
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		# -1- Take another argument for speed with which movement is to be done                                                       #
		# -2- Take another argument which can have values :'slow' or 'fast' or 'medium', so we know how fast the bot has to be moved  #
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

		# if d=='R': 
		# 	if bot.dir<3:
		# 		d=bot.dirs[bot.dir+1]
		# 	elif bot.dir==3: 
		# 		d=bot.dirs[0]
		# elif d=='L': 
		# 	if bot.dir>0:
		# 		d=bot.dirs[bot.dir-1]
		# 	elif bot.dir==0:
		# 		d=bot.dirs[3] 
		# elif d=='S':
		# 	if bot.dir<=1:
		# 		d=bot.dirs[bot.dir+2]
		# 	else:
		# 		d=bot.dirs[bot.dir-2]
		# elif d=='F':
		# 	d=bot.dirs[bot.dir]

		d=bot.dirs[bot.dir]

		if d=='N':
			self.north()
		elif d=='S':
			self.south()
		elif d=='E':
			self.east()
		else :
			self.west()
		

	def north(self):
		# print("Velocity given")
		self.msg1.linear.y = -0.1
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)


	def south(self):
		# print("Velocity given")
		self.msg1.linear.y = 0.1
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)


	def east(self):
		# print("Velocity given")
		self.msg1.linear.x = -0.1
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)


	def west(self):
		# print("Velocity given")
		self.msg1.linear.x = 0.1
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)

	
	# def slow_forward(self):
	# 	# print("Velocity given")
	# 	self.msg1.linear.y = -0.05
	# 	self.msg1.linear.x = 0
	# 	self.pub.publish(self.msg1)

	def stop(self):
		self.msg1.linear.x = 0
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)

	
	# def pid(self,l,c,r):
	# 	# pid
	# 	pass
		
if __name__ == '__main__':
	obj=bot()
	while(1):
		obj.stop()

  # FYI, move() has to be called continuously for the bot to move 
	# obj.rotate(90)
	
