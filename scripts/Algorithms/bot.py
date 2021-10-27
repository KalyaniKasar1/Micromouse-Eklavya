#! /usr/bin/env python

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
		self.yaw=1000.0
		self.msg1=Twist()
		self.sub = rospy.Subscriber ('/odom', Odometry, self.clbk_odom)
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	
	def move(self):
		# print("Velocity given")
		self.msg1.linear.x=0.35
		self.msg1.angular.z=0
		self.pub.publish(self.msg1)

	# def getDir(self):
	# 	if (-5<self.yaw) and (self.yaw<5): 
	# 		return 2
	# 	elif (85<self.yaw) and (self.yaw<95): 
	# 		return 3
	# 	elif (-85<self.yaw) and (self.yaw<-95): 
	# 		return 1
	# 	elif (-175<self.yaw) and (self.yaw<175): 
	# 		return 0

	def pid(self,l,c,r):
		# pid
		pass
		
	def clbk_odom(self,msg):
		#print("Yaw value: ", self.yaw)
		orientation_q = msg.pose.pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(_, _, self.yaw) = euler_from_quaternion (orientation_list)  #yaw=0.0 is north direction
    
	def rotate(self,targ):  
		kp=0.95
		print("Rotating to yaw %5.2f..." %targ)
		yaw_deg = (self.yaw*180/math.pi)
		#print("Yaw deg:", yaw_deg)
		while True :
			target_rad = targ * math.pi/180
			self.msg1.angular.z = kp * (target_rad-self.yaw)
			#print("Velocity: ", self.msg1.angular.z )
			self.msg1.linear.x = 0
			yaw_deg = (self.yaw*180/math.pi)
			if (round(yaw_deg) != targ) :
				self.pub.publish(self.msg1)
				#print("target=%5.2f current:%5.2f" %(targ,yaw_deg))
			else :    
				print("Robot successfully turned!")
				print("Final yaw:", yaw_deg)
				self.msg1.linear.x = 0
				self.msg1.angular.z = 0
				self.pub.publish(self.msg1)
				#rospy.signal_shutdown("Shutting down....done!")
				break
		pass

if __name__ == '__main__':
	obj=bot()
	# obj.move()
	obj.rotate(90)
	
