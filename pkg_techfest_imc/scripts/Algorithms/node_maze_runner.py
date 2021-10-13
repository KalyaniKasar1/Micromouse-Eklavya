#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

# Global Variables
sensor_l, sensor_c, sensor_r = 0, 0, 0
pub = 0 

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r
    # 720 / 5 = 144
    regions = [
        round(100*min(min(msg.ranges[0:71]), 100)),
        round(100*min(min(msg.ranges[72:143]), 100)),
        round(100*min(min(msg.ranges[144:215]), 100)),
        round(100*min(min(msg.ranges[216:287]), 100)),
        round(100*min(min(msg.ranges[288:359]), 100)),
    ]
    # rospy.loginfo(regions)
    
    print("Inside callback")
    print("l: {} \t c: {} \t r: {}".format(regions[4], regions[2], regions[0]))
    
    sensor_l = regions[4]
    sensor_c = regions[2]
    sensor_r = regions[0]

    # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r))

def motion_go_straight():
    global pub
    msg = Twist()
    msg.linear.x = 0.08
    print("Inside start motion")
    pub.publish(msg)

def motion_stop():
    global pub
    msg = Twist()
    msg.linear.x = 0.05
    print("Inside stop motion")
    pub.publish(msg)

def main():
    
    global sensor_l, sensor_c, sensor_r
    global pub

    msg = Twist()

    rospy.init_node('node_maze_runner')
    
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    # pub.publish(msg)
    
    # rospy.spin()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        print("Inside not shut")
        print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r))
  
        if(sensor_c > 15):
            motion_go_straight()
            print("motion strt called")
        else:
            motion_stop()
            print("motion stop called")

        rate.sleep()

if __name__ == '__main__':
    main()
