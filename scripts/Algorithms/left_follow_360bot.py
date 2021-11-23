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
dir= 2  #by default direction is south facing (yaw=0), direction is chosen from the below list
dirs=[180,-90,0,90]  # correspond to the north, west, south & east directions
pub = None 
l=0  #Becomes 1 if left turn has been taken...used to avoid immediate left turn after one left turn 
regions=[]

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    
    regions = [  
        round(100*min(max(max(msg.ranges[345:359]), max(msg.ranges[0:14])), 100)),   
        round(100*min(max(msg.ranges[75:104]), 100)), 
        round(100*min(max(msg.ranges[165:194]), 100)),
        round(100*min(max(msg.ranges[255:284]), 100))
    ]
   

    if sensor_l != regions[2] and sensor_c != regions[1] and sensor_r != regions[0] and sensor_b != regions[3]:
        print("l: {} \t c: {} \t r: {} \t b: {}".format(regions[3], regions[2], regions[1], regions[0]))
    
    sensor_l = regions[3]
    sensor_c = regions[2]
    sensor_r = regions[1]
    sensor_b = regions[0]


# def check_dir(n) : #checks which direction the turn should be taken to 
#     global dir, dirs
#     # dir = obj.getDir() #current
#     print("Dir is: ", dir)
#     if n==1:
#         if dir<3:
#             dir=dir+n
#         elif dir==3: 
#             dir=0
#     elif n==-1:
#         if dir>0:
#             dir=dir+n
#         elif dir==0:
#             dir=3 
#     elif n==2:
#         if dir<=1:
#             dir=dir+2
#         else:
#             dir=dir-2
        
#     return dirs[dir]


# def delay(t) : #to give a certain time period delay after every turn
#     print("Delaying............")
#     t0 = rospy.Time.now().to_sec()
#     t1=0
#     while ((t1-t0)<t) :
#         t1 = rospy.Time.now().to_sec()
#         obj.move()


def left_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_c = sensor_r
    sensor_l = sensor_c
    sensor_b = sensor_l
    sensor_r = sensor_b


def right_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_l = sensor_b
    sensor_c = sensor_l
    sensor_r = sensor_c
    sensor_b = sensor_r
    

def deadend_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_l = sensor_r
    sensor_r = sensor_l
    sensor_c = sensor_b
    sensor_b = sensor_c


# Checking for left wall
def check_left():     
    global sensor_l, sensor_c, sensor_r, sensor_b
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
    print("Checking left wall...")
    if sensor_l <= 12:
        print("Left wall found")
        return False
    else:
        print("Left wall not found")
        return True
    

# Checking for right wall
def check_right():
    global sensor_l, sensor_c, sensor_r, sensor_b
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    print("Checking right wall...")
    if sensor_r <= 12:
        print("Right wall found")
        return False
    else:
        print("Right wall not found")
        return True


# Checking for center wall
def check_center():
    global sensor_l, sensor_c, sensor_r, sensor_b
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    print("Checking center wall...")
    if sensor_c <= 12:
        print("Center wall found")
        return False
    else:
        print("Center wall not found")
        return True


# Checking for back wall
def check_back():
    global sensor_l, sensor_c, sensor_r, sensor_b
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    print("Checking back wall...")
    if sensor_b <= 12:
        print("Center wall found")
        return False
    else:
        print("Center wall not found")
        return True


def leftfollow():
    global sensor_l, sensor_c, sensor_r, l, dir
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        
        # obj.forward()
        if check_left:
            # if l == 0:
            prev_c = sensor_c
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            if abs(prev_c - sensor_c) >= 4:
                obj.left()
                print("Moving left")
                left_exchange()
                l = 1
            else:
                obj.slow_forward()
            

        elif check_center:
            print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            obj.forward()
            print("Moving forward")
            l = 0

        elif check_right:
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            obj.right()
            print("Moving right")
            right_exchange()
            l = 0

        else:
            # Dead End
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            obj.back()
            print("Moving back")
            deadend_exchange()
            l = 0
        

    



if __name__ == '__main__':

    obj = bot()
    leftfollow()