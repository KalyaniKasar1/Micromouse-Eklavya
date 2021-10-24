#! /usr/bin/env python

import rospy
from statistics import mean
from bot import *
from sensor_msgs.msg import LaserScan

sensor_l, sensor_c, sensor_r = 0, 0, 0
regions=[]

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, regions
    # 720 / 5 = 144
    regions = [
        round(100*min(mean(msg.ranges[0:71]), 100)),
        round(100*min(mean(msg.ranges[72:143]), 100)),
        round(100*min(mean(msg.ranges[144:215]), 100)),
        round(100*min(mean(msg.ranges[216:287]), 100)),
        round(100*min(mean(msg.ranges[288:359]), 100)),
    ]
    # rospy.loginfo(regions)
    
    #print("Inside callback......")
    #print("mean of range dists of leftex:", mean(msg.ranges[144:215]))

    if sensor_l != regions[4] and sensor_c != regions[2] and sensor_r != regions[0] :
        print("l: {} \t c: {} \t r: {}".format(regions[4], regions[2], regions[0],"\n\n\n\n\n"))
    
    sensor_l = regions[4]
    sensor_c = regions[2]
    sensor_r = regions[0]


def main():
    rospy.init_node('reading_laser')
    
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    main()
