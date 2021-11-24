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

sensor_l, sensor_c, sensor_r, sensor_b = 0, 0, 0, 0
pub = None 
regions=[]

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    
    regions = [  
        round(100*min(max(max(msg.ranges[345:359]), max(msg.ranges[0:14])), 100)),   
        round(100*min(max(msg.ranges[75:104]), 100)), 
        round(100*min(max(msg.ranges[165:194]), 100)),
        round(100*min(max(msg.ranges[255:284]), 100))
    ]
    # print(msg.ranges[0:359])

    if sensor_l != regions[3] or sensor_c != regions[2] or sensor_r != regions[1] or sensor_b != regions[0]:
        print("l: {} \t c: {} \t r: {} \t b: {}".format(regions[3], regions[2], regions[1], regions[0]))
    
    sensor_l = regions[3]
    sensor_c = regions[2]
    sensor_r = regions[1]
    sensor_b = regions[0]


def sensor_values():
    global sensor_l, sensor_c, sensor_r, sensor_b
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        pass


if __name__ == '__main__':
    obj = bot()
    sensor_values()
