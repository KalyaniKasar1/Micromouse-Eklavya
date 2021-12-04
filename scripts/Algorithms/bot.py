#! /usr/bin/env python


###
###  FOR OMNIWHEELED BOT MOVING BY PLANAR MOVE PLUGIN
###


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
	
	def move(self, d):
		if d=='R': 
			if bot.dir<3:
				d=bot.dirs[bot.dir+1]
			elif bot.dir==3: 
				d=bot.dirs[0]
		elif d=='L': 
			if bot.dir>0:
				d=bot.dirs[bot.dir-1]
			elif bot.dir==0:
				d=bot.dirs[3] 
		elif d=='S':
			if bot.dir<=1:
				d=bot.dirs[bot.dir+2]
			else:
				d=bot.dirs[bot.dir-2]
		elif d=='F':
			d=bot.dirs[bot.dir]

		# d=bot.dirs[bot.dir]

		if d=='N':
			self.north(0.1)
		elif d=='S':
			self.south(0.1)
		elif d=='E':
			self.east(0.1)
		else :
			self.west(0.1)
		

	def slow_move(self, d):
		if d=='R': 
			if bot.dir<3:
				d=bot.dirs[bot.dir+1]
			elif bot.dir==3: 
				d=bot.dirs[0]
		elif d=='L': 
			if bot.dir>0:
				d=bot.dirs[bot.dir-1]
			elif bot.dir==0:
				d=bot.dirs[3] 
		elif d=='S':
			if bot.dir<=1:
				d=bot.dirs[bot.dir+2]
			else:
				d=bot.dirs[bot.dir-2]
		elif d=='F':
			d=bot.dirs[bot.dir]


		if d=='N':
			self.north(0.08)
		elif d=='S':
			self.south(0.08)
		elif d=='E':
			self.east(0.08)
		else :
			self.west(0.08)

	def north(self,v):  #v stands for velocity given
		# print("Velocity given")
		self.msg1.linear.y = (-1)*v
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)

	def south(self,v):
		# print("Velocity given")
		self.msg1.linear.y = v
		self.msg1.linear.x = 0
		self.pub.publish(self.msg1)

	def east(self,v):
		# print("Velocity given")
		self.msg1.linear.x = (-1)*v
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)

	def west(self,v):
		# print("Velocity given")
		self.msg1.linear.x = v
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)

	def stop(self):
		self.msg1.linear.x = 0
		self.msg1.linear.y = 0
		self.pub.publish(self.msg1)
		
if __name__ == '__main__':
	obj=bot()
	while(1):
		obj.stop()
	
