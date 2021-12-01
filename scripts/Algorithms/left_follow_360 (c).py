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
# dir= 0  #by default internal direction is towards north, direction is chosen from the below list
# dirs=['N', 'E', 'S', 'W']  # correspond to the north, west, south & east, OR forward, right, back, left
pub = None 
regions=[]
prev_c = 0
first_clbk = True

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    
    regions = [  
        round(100*min(max(max(msg.ranges[345:359]), max(msg.ranges[0:14])), 100)),   
        round(100*min(max(msg.ranges[75:104]), 100)), 
        round(100*min(max(msg.ranges[165:194]), 100)),
        round(100*min(max(msg.ranges[255:284]), 100))
    ]
    # print(msg.ranges[0:359])

    # if sensor_l != regions[3] or sensor_c != regions[2] or sensor_r != regions[1] or sensor_b != regions[0]:
    #     print("l: {} \t c: {} \t r: {} \t b: {}".format(regions[3], regions[2], regions[1], regions[0]))
    
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
    # global dir, dirs
    # print("Old Dir is: ", bot.dirs[bot.dir])
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

    # print("New Dir is: ", bot.dirs[bot.dir])
    # return dirs[dir]

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

def delay(t) : #to give a certain time period delay after every turn
    print("\nDelaying............\n")
    t0 = rospy.Time.now().to_sec()
    t1=0
    while ((t1-t0)<t) :
        t1 = rospy.Time.now().to_sec()
        # obj.move()
        # obj.slow_forward()
        obj.stop()

def check_left(): # Checking for left wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
    # print("Checking left wall...")
    if sensor_l >= 5 and sensor_l <= 11 :
    # if sensor_l <= 9:
        # print("Left not possi")
        return False
    elif (sensor_l+sensor_r)>18 :
        print("\nLeft possible!\n")
        return True

def check_right(): # Checking for right wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    # print("Checking right wall...")
    if sensor_r >= 5 and sensor_r <= 11 :
    # if sensor_l <= 9:
        # print("Right not possi")
        return False
    elif (sensor_l+sensor_r)>18 :
        print("\nRight possible!\n")
        return True

def check_center(): # Checking for center wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    # print("Checking center wall...")
    if sensor_c >= 5 and sensor_c <= 11 :
    # if sensor_c <= 9 :
        # print("Straight not possi")
        return False
    else:
        # print("Straight possi")
        return True

def leftfollow():
    delay(5)
    global sensor_l, sensor_c, sensor_r, prev_c, l, c, r
    
    # while not rospy.is_shutdown():
    while(1) :
        obj.move()
        if check_left():  #left turn possible
            # delay(5)
            if l==0 :
                prev_c = sensor_c
                while ((prev_c - sensor_c) <= 10) and (prev_c - sensor_c) >= 0 and sensor_c>=8 :
                    # print("Sensor_c inside while:", sensor_c)
                    # print("Difference inside while: ", prev_c - sensor_c)
                    obj.move()

            # delay(5)
            else :
                prev_c = sensor_c
                while ((prev_c - sensor_c) <= 5) and (prev_c - sensor_c) >= 0 and sensor_c>=8 :
                    print("Sensor_c", sensor_c)
                    obj.move()
            change_dir(-1)
            left_exchange()
            # print("\nExchanged left")
            print("Turning left...done")
            
            delay(5)
         
            prev_c = sensor_c
            while ((prev_c - sensor_c) <= 10) and (prev_c - sensor_c) >= 0 and sensor_c>=8 :
                obj.move()
            print("Now, next........")
            
            delay(5)

            # delay(1)
            l = 1
            r = 0

        elif check_center():
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            obj.move()
            l = 0
            r = 0

        elif check_right():
            # delay(5)
            if r==0 :
                prev_c = sensor_c
                while ((prev_c - sensor_c) <= 10) and (prev_c - sensor_c) >= 0 and sensor_c>=8 :
                    obj.move()

            # delay(5)
            else :
                prev_c = sensor_c
                while ((prev_c - sensor_c) <= 5) and (prev_c - sensor_c) >= 0 and sensor_c>=8 :
                    print("Sensor_c", sensor_c)
                    obj.move()
            change_dir(1)
            right_exchange()
            # print("\nExchanged right")
            print("Turning right...done\n")
         
            prev_c = sensor_c
            while ((prev_c - sensor_c) <= 10) and (prev_c - sensor_c) >= 0 and sensor_c>=8 :
                obj.move()
            
            # obj.stop()
            # delay(1)
            l = 0
            r = 1

        else:
            # Dead End
            # prev_c = sensor_c
            # while ((prev_c - sensor_c) <= 9) and (prev_c - sensor_c) >= 0 and sensor_c>=10 :
            #     # print("Sensor_c inside while:", sensor_c)
            #     # print("Difference inside while: ", prev_c - sensor_c)
            #     obj.move()

            # delay(5)
            change_dir(2)
            deadend_exchange()
            print("\nExchanged deadend")
            print("U turning...\n")
         
            # prev_c = sensor_c
            # while ((prev_c - sensor_c) <= 12) and (prev_c - sensor_c) >= 0 and sensor_c>=10 :
                # print("Sensor_c inside while:", sensor_c)
                # print("Difference inside while: ", prev_c - sensor_c)
                # obj.move()
            
            # obj.stop()
            # delay(5)
            l = 0
            r = 0


    rospy.spin()

if __name__ == '__main__':
    obj = bot()
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)
    leftfollow()
    # change_dir(1)
    rospy.spin()

# def delay(t) : #to give a certain time period delay after every turn
#     print("Delaying............")
#     t0 = rospy.Time.now().to_sec()
#     t1=0
#     while ((t1-t0)<t) :
#         t1 = rospy.Time.now().to_sec()
#         # obj.move()
#         obj.slow_forward()

# def check_back(): # Checking for back wall
#     global sensor_l, sensor_c, sensor_r, sensor_b
#     print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
#     print("Checking back wall...")
#     if sensor_b <= 12:
#         print("Center wall found")
#         return False
#     else:
#         print("Center wall not found")
#         return True
