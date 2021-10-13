#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *
from statistics import mean
import bot_rot
import bot_mov 
import math

# Global Variables
sensor_l, sensor_c, sensor_r = 0, 0, 0
pub = None 
flagl=flagf=flagr=0  #flags to check for walls in front or left or right
msg1 = Twist()

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r
    # 720 / 5 = 144
    regions = [
        round(100*min(mean(msg.ranges[0:71]), 100)),
        round(100*min(mean(msg.ranges[72:143]), 100)),
        round(100*min(mean(msg.ranges[144:215]), 100)),
        round(100*min(mean(msg.ranges[216:287]), 100)),
        round(100*min(mean(msg.ranges[288:359]), 100)),
    ]
    # rospy.loginfo(regions)
    

    print("Inside callback")
    #print("mean of range dists of leftex:", mean(msg.ranges[144:215]))
    print("l: {} \t c: {} \t r: {}".format(regions[4], regions[2], regions[0]))
    
    sensor_l = regions[4]
    sensor_c = regions[2]
    sensor_r = regions[0]

    # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r))

def check_left() : #checks if wall is present on the left
    global sensor_l, sensor_c, sensor_r, flagl, flagf, flagr, msg1
    print("Inside checkleft")
    if sensor_l >= 9 :
        flagl=1  #wall on left
    elif sensor_l>6 and sensor_l<8 : 
        print("Taking a turn")
        flagl=2
        msg1.linear.x=0
        pub_.publish(msg1)
        
        bot_rot.target=90.0
        bot_rot.main() #turn left
        
def check_right() : #checks if wall is present on the right
    global sensor_l, sensor_c, sensor_r, flagl, flagf, flagr, msg1
    print("Inside checkright")
    if sensor_r >= 9 :
        flagr=1  #wall on right
        msg1.linear.x=0
        pub_.publish(msg1)
        
        bot_rot.target=180.0
        bot_rot.main() #turn 180, dead end
        
    elif sensor_r>6 and sensor_r<8 : 
        print("Taking a turn")
        flagr=2
        msg1.linear.x=0
        pub_.publish(msg1)
        
        bot_rot.target=-90.0
        bot_rot.main() #turn right
        
def check_front() : #checks if wall is present in front
     global sensor_l, sensor_c, sensor_r, flagl, flagf, flagr, msg1
     print("Inside checkfront")
     if sensor_c <=8 :
         flagf=1 #wall in front
     elif sensor_c >=22 :
         flagf=0
         #pidtune
    
    
def main():
    global pub_, active_, flagl, flagf, flagr, msg1
    
    rospy.init_node('follow_wall')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=10)  #orig qs was 1
    
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    
    #srv = rospy.Service('wall_follower_switch', SetBool, wall_follower_switch)
    
    rate = rospy.Rate(50)   #orig rate for 20
    
    while not rospy.is_shutdown():

        check_left()
        if flagl== 1 : #if wall on left
            check_front()
            if flagf==1 : #if wall in front
                check_right()
                
        flagl=flagf=flagr=0 
        
        msg1.angular.z=0.0
        msg1.linear.x=0.35
        pub_.publish(msg1)
        
        rate.sleep()

if __name__ == '__main__':
    main()
    


