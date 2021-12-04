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
l, c, r = 0, 0, 0
pub = None 
regions=[]
prev_b = 0
first_run = True

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions

    # 5 degrees
    regions = [  
        round(100*min(max(max(msg.ranges[358:359]), max(msg.ranges[0:2])), 100)),   
        round(100*min(max(msg.ranges[88:92]), 100)), 
        round(100*min(max(msg.ranges[178:182]), 100)),
        round(100*min(max(msg.ranges[268:272]), 100))
    ]

    sensor_l = regions[3]
    sensor_c = regions[2]
    sensor_r = regions[1]
    sensor_b = regions[0]

    if bot.dir==1 : #bot is internally facing east
        right_exchange()
    elif bot.dir==2 : #bot is internally facing south
        deadend_exchange()
    elif bot.dir==3 :  #bot is internally facing west
        left_exchange()
    

def change_dir(n) : #changes direction as per turn to be taken
    if n==1:    # +1 is for clockwise, ie, right turn
        if bot.dir<3:
            bot.dir=bot.dir+n
        elif bot.dir==3: 
            bot.dir=0
    elif n==-1: # -1 is for anti clockwise, ie, left turn
        if bot.dir>0:
            bot.dir=bot.dir+n
        elif bot.dir==0:
            bot.dir=3 
    elif n==2:
        if bot.dir<=1:
            bot.dir=bot.dir+2
        else:
            bot.dir=bot.dir-2

def left_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, temp_l, temp_c, temp_r, temp_b
    sensor_l, sensor_c, sensor_r, sensor_b = sensor_b, sensor_l, sensor_c, sensor_r

def right_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_l, sensor_c, sensor_r, sensor_b = sensor_c, sensor_r, sensor_b, sensor_l

def deadend_exchange():
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    sensor_l, sensor_c, sensor_r, sensor_b = sensor_r, sensor_b, sensor_l, sensor_c

def delay(t) : #to give a certain time period delay
    print("\nDelaying............\n")
    t0 = rospy.Time.now().to_sec()
    t1=0
    while ((t1-t0)<t) :
        t1 = rospy.Time.now().to_sec()
        obj.stop()

def check_left(): # Checking for left wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    if sensor_l >= 5 and sensor_l <= 11:
        return False
    elif (sensor_l+sensor_r)>18 :
        print("\nLeft possible!")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
        return True

def check_right(): # Checking for right wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    if sensor_r >= 5 and sensor_r <= 11:
        return False
    elif (sensor_l+sensor_r)>18 :
        print("\nRight possible!")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
        return True

def check_center(): # Checking for center wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    if sensor_c >= 5 and sensor_c <= 9 :
        print("\nWall Ahead!\n")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        return False
    else:
        return True

def recenter() :
    global sensor_l, sensor_r
    if sensor_l <= 7 :
        while sensor_l <= 7 :
            obj.slow_move('R')
    elif sensor_r <= 7 :
        while sensor_r <= 7 :
            obj.slow_move('L')        

def leftfollow():
    global sensor_l, sensor_c, sensor_r, prev_b, first_run, c
    delay(5)
    if first_run :
        prev_b = sensor_b
        first_run = False
    
    while(1) :
        while ((sensor_b - prev_b) <= 18) and sensor_c>=10 :
            if c >= 2 :
                if check_left() :
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 9) and sensor_c>=10 :
                        obj.slow_move('F')
                    break
                elif check_right() and (not check_center()) :    
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 9) and sensor_c>=10 :
                        obj.slow_move('F')
                    break
            obj.move('F')
        
        recenter()
        # delay(3)
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        print("Travelled one block\n")
        if check_left():  #Left turn possible
            # delay(5)
            change_dir(-1)
            left_exchange()
            print("Exchanged left")
            print("Turning left...")
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            # delay(5)

        elif check_center():  #Straight path
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            # obj.move('F')
            prev_b = sensor_b
            c = c + 1
            recenter()

        elif check_right():  #Right turn possible
            # delay(5)
            change_dir(1)
            right_exchange()
            print("Exchanged right")
            print("Turning right...")
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            # delay(1)

        else:  # Dead end
            # delay(5)
            change_dir(2)
            deadend_exchange()
            print("Exchanged deadend")
            print("U turning...\n")
            prev_b = sensor_b
            c = c + 1
            recenter()

if __name__ == '__main__':
    obj = bot()
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)
    leftfollow()
    # change_dir(1)
    rospy.spin()
