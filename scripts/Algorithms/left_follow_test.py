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
        round(100*min(max(msg.ranges[0:89]), 100)),   
        round(100*min(max(msg.ranges[90:269]), 100)), 
        round(100*min(max(msg.ranges[270:359]), 100))
    ]
   

    if sensor_l != regions[2] and sensor_c != regions[1] and sensor_r != regions[0] :
        print("l: {} \t c: {} \t r: {}".format(regions[2], regions[1], regions[0],"\n\n\n\n\n"))
    
    sensor_l = regions[2]
    sensor_c = regions[1]
    sensor_r = regions[0]


def check_dir(n) : #checks which direction the turn should be taken to 
    global dir, dirs
    # dir = obj.getDir() #current
    print("Dir is: ", dir)
    if n==1:
        if dir<3:
            dir=dir+n
        elif dir==3: 
            dir=0
    elif n==-1:
        if dir>0:
            dir=dir+n
        elif dir==0:
            dir=3 
    elif n==2:
        if dir<=1:
            dir=dir+2
        else:
            dir=dir-2
        
    return dirs[dir]


def delay(t) : #to give a certain time period delay after every turn
    print("Delaying............")
    t0 = rospy.Time.now().to_sec()
    t1=0
    while ((t1-t0)<t) :
        t1 = rospy.Time.now().to_sec()
        obj.move()


def check_left():
    global sensor_l, sensor_c, sensor_r
    print("Checking left wall...")
    if sensor_l <= 12:
        return True
    else:
        return False
    

def check_right():
    global sensor_r
    print("Checking right wall...")
    if sensor_r <= 12:
        return True
    else:
        return False


def check_center():
    global sensor_c
    print("Checking tne front...")
    if sensor_c <= 12:
        return True
    else:
        False


def leftfollow():
    global sensor_l, sensor_c, sensor_r, l, dir
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        obj.move()
        if check_left:
            if check_center:
                if check_right:
                    #Reached dead end
                    target = check_dir(2)  # When dir = 2, it will make a 180 degree turn 
                    obj.rotate(target)
                    print("Making a U turn...")
                    obj.move()
                    print("Moving...")
                    print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))
                else:
                    target = check_dir(-1) # When dir = -1, it will make a right turn
                    obj.rotate(target)
                    print("Making a right turn...")
                    obj.move()
                    print("Moving...")
                    print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))
            else:
                obj.move()
                print("Moving...")
                print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))
        else:
            target = check_dir(1)  # When dir = 1, it will make a left turn
            obj.rotate(target)
            print("Making a left turn...")
            obj.move()
            print("Moving...")
            print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))

        


if __name__ == '__main__':
    obj = bot()
    leftfollow()

    

