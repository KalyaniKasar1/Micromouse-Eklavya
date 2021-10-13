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
flagl=flagf=flagr=0
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
        flagl=1  #wall
    elif sensor_l>6 and sensor_l<8 : 
        print("Taking a turn")
        flagl=2
        msg1.linear.x=0
        pub_.publish(msg1)
        
        bot_rot.target=90.0
        bot_rot.main() #turn left
        
    
    
def main():
    global pub_, active_, flagl, flagf, flagr, msg1
    
    rospy.init_node('follow_wall')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=10)  #orig qs was 1
    
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    
    #srv = rospy.Service('wall_follower_switch', SetBool, wall_follower_switch)
    
    rate = rospy.Rate(50)   #orig rate for 20
    
    while not rospy.is_shutdown():

        check_left()
        
        '''if flagl== 1 :
            pidtune()
            if (cond for checking wall in front) :
            #if (cond for checking wall in front) :
                flagf=1
                if (cond for checking if wall on right) :
                    flagr=1
                    turn(180) #dead end
                else
                    turn(-90) #right turn
            else :
                continue/keep moving & PIDDDD 
        elif flagl==2 :
            bot_rot.target=90.0
            bot_rot.main() #turn left
            
        flagl=flagf=flagr=0 '''
        
        ''''if state_ == 0:
            print("Inside rospy not shutdown find_wall()")
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
        elif state_ == 2:
            msg = follow_the_wall()
            pass
        else:
            rospy.logerr('Unknown state!') '''
        
        msg1.linear.x=0.35
        pub_.publish(msg1)
        
        rate.sleep()

if __name__ == '__main__':
    main()
    


