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
dir= 0  #by default internal direction is towards north, direction is chosen from the below list
dirs=['F', 'R', 'B', 'L']  # correspond to the north, west, south & east, OR forward, right, back, left
pub = None 
regions=[]
prev_c = 0
first_clbk = True

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions, first_clbk
    
    regions = [  
        round(100*min(max(max(msg.ranges[345:359]), max(msg.ranges[0:14])), 100)),   
        round(100*min(max(msg.ranges[75:104]), 100)), 
        round(100*min(max(msg.ranges[165:194]), 100)),
        round(100*min(max(msg.ranges[255:284]), 100))
    ]
   
    # if sensor_l != regions[2] and sensor_c != regions[1] and sensor_r != regions[0] and sensor_b != regions[3]:
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(regions[3], regions[2], regions[1], regions[0]))
    
    sensor_l = regions[3]
    sensor_c = regions[2]
    sensor_r = regions[1]
    sensor_b = regions[0]

    # if first_clbk :
    #     leftfollow()
    #     first_clbk = False

# def change_dir(n) : #changes direction as per turn to be taken
#     global dir, dirs
#     # dir = obj.getDir() #current
#     print("Dir is: ", dir)
#     if n==1:    # +1 is for clockwise, ie, right turn
#         if dir<3:
#             dir=dir+n
#         elif dir==3: 
#             dir=0
#     elif n==-1: # -1 is for anti clockwise, ie, left turn
#         if dir>0:
#             dir=dir+n
#         elif dir==0:
#             dir=3 
#     elif n==2:
#         if dir<=1:
#             dir=dir+2
#         else:
#             dir=dir-2
#     # return dirs[dir]

def left_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, temp_l, temp_c, temp_r, temp_b
    sensor_l, sensor_c, sensor_r, sensor_b = sensor_b, sensor_l, sensor_c, sensor_r
    #prev_c = [0]

def right_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_l, sensor_c, sensor_r, sensor_b = sensor_c, sensor_r, sensor_b, sensor_l

def deadend_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_l, sensor_c, sensor_r, sensor_b = sensor_r, sensor_b, sensor_l, sensor_c

def check_left(): # Checking for left wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
    # print("Checking left wall...")
    # if sensor_l > 2 and sensor_l <= 9:
    if sensor_l <= 9:
        # print("Left not possi")
        return False
    else:
        print("Left possi")
        return True

def check_right(): # Checking for right wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    # print("Checking right wall...")
    if sensor_r > 2 and sensor_r <= 9:
        print("Right not possi")
        return False
    else:
        # print("Right possi")
        return True

def check_center(): # Checking for center wall
    # global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    # print("Checking center wall...")
    if sensor_c > 2 and sensor_c <= 9 :
        # print("Straight not possi")
        return False
    else:
        # print("Straight possi")
        return True

def check_back(): # Checking for back wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    print("Checking back wall...")
    if sensor_b <= 12:
        print("Center wall found")
        return False
    else:
        print("Center wall not found")
        return True

def delay(t) : #to give a certain time period delay after every turn
    print("Delaying............")
    t0 = rospy.Time.now().to_sec()
    t1=0
    while ((t1-t0)<t) :
        t1 = rospy.Time.now().to_sec()
        # obj.move()
        # obj.slow_forward()
        obj.stop()


def leftfollow():
    # obj.forward()
    global sensor_l, sensor_c, sensor_r, dir, prev_c
    
    # while not rospy.is_shutdown():
    while(1) :
        obj.forward()
        if check_left():  #left turn possible
            
            prev_c = sensor_c
            print("Prev_c :", prev_c)
            print("Sensor_c outside while:", sensor_c)
            print("Difference outside while: ", prev_c - sensor_c)
            
            # obj.stop()
            # delay(100)
            # while ((prev_c - sensor_c) <= 10) and (prev_c - sensor_c) > 0 :
            while ((prev_c - sensor_c) <= 7) > 0 :
                print("Sensor_c inside while:", sensor_c)
                print("Difference inside while: ", prev_c - sensor_c)
                obj.forward()

            obj.stop()
            delay(10)
        
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            # print("Moving right")

            # else :
            #     print("Sensor_c(1st time) : ", sensor_c)
            left_exchange()
            print("Exchanged left")
            while sensor_c >= 9:
                print("Turning left")
                obj.left()
            obj.stop()

        elif check_center():
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            # obj.forward()
            pass
            # print("Moving forward")
            

        elif check_right():
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            obj.right()
            print("Moving right")
            right_exchange()

        else:
            # Dead End
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            obj.back()
            print("Moving back")
            deadend_exchange()

    rospy.spin()

if __name__ == '__main__':
    obj = bot()
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)
    leftfollow()
    rospy.spin()
    # leftfollow()

# def delay(t) : #to give a certain time period delay after every turn
#     print("Delaying............")
#     t0 = rospy.Time.now().to_sec()
#     t1=0
#     while ((t1-t0)<t) :
#         t1 = rospy.Time.now().to_sec()
#         # obj.move()
#         obj.slow_forward()
