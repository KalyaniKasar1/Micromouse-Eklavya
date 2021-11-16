#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *
from statistics import mean
from bot import *
import math

sensor_l, sensor_c, sensor_r = 0, 0, 0
dir= 2  #by default direction is south facing (yaw=0), direction is chosen from the below list
dirs=[180,-90,0,90]  # correspond to the north, west, south & east directions
pub = None 
l=0  #Becomes 1 if left turn has been taken...used to avoid immediate left turn after one left turn 
regions=[]

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, regions
    regions = [  #Dividing into 3 regions - 0-45, 46-135 and 136-180
        round(100*min(mean(msg.ranges[0:89]), 100)),   
        round(100*min(mean(msg.ranges[90:269]), 100)), 
        round(100*min(mean(msg.ranges[270:359]), 100))
    ]
   

    if sensor_l != regions[2] and sensor_c != regions[1] and sensor_r != regions[0] :
        print("l: {} \t c: {} \t r: {}".format(regions[2], regions[1], regions[0],"\n\n\n\n\n"))
    
    sensor_l = regions[2]
    sensor_c = regions[1]
    sensor_r = regions[0]

def sensor_values():
    global sensor_l, sensor_c, sensor_r
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))


if __name__ == '__main__':
    obj = bot()
    sensor_values()