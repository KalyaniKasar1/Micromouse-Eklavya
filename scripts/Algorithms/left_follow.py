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
prev_b = 0
first_run = True

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions

    # 30 degrees    
    # regions = [  
    #     round(100*min(max(max(msg.ranges[345:359]), max(msg.ranges[0:14])), 100)),   
    #     round(100*min(max(msg.ranges[75:104]), 100)), 
    #     round(100*min(max(msg.ranges[165:194]), 100)),
    #     round(100*min(max(msg.ranges[255:284]), 100))
    # ]

    # 5 degrees
    regions = [  
        round(100*min(max(max(msg.ranges[358:359]), max(msg.ranges[0:2])), 100)),   
        round(100*min(max(msg.ranges[88:92]), 100)), 
        round(100*min(max(msg.ranges[178:182]), 100)),
        round(100*min(max(msg.ranges[268:272]), 100))
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
    #prev_b = [0]

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
        # obj.move('F')
        # obj.slow_forward()
        obj.stop()

def check_left(): # Checking for left wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("Checking left wall...")
    if sensor_l >= 5 and sensor_l <= 10:
    # if sensor_l <= 9:
        # print("Left not possi")
        return False
    elif (sensor_l+sensor_r)>18 :
        print("\nLeft possible!")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
        return True

def check_right(): # Checking for right wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    # print("Checking right wall...")
    if sensor_r >= 5 and sensor_r <= 10:
    # if sensor_l <= 9:
        # print("Right not possi")
        return False
    elif (sensor_l+sensor_r)>18 :
        print("\nRight possible!")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
        return True

def check_center(): # Checking for center wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
    # print("Checking center wall...")
    if sensor_c >= 5 and sensor_c <= 9 :
    # if sensor_c <= 9 :
        print("\nWall Ahead!\n")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        return False
    else:
        # print("Straight possi")
        return True

def recenter() :
    global sensor_l, sensor_r
    if sensor_l <= 7 :
        while sensor_l <= 7 :
            obj.move('R')
    elif sensor_r <= 7 :
        while sensor_r <= 7 :
            obj.move('L')        

def leftfollow():
    global sensor_l, sensor_c, sensor_r, prev_b, first_run, c
    # obj.forward()
    delay(5)
    if first_run :
        prev_b = sensor_b
        first_run = False
    
    # while not rospy.is_shutdown():
    while(1) :
        # obj.forward()
        while ((sensor_b - prev_b) <= 18) and sensor_c>=10 :
            if c >= 2 :
                if check_left() :
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 9) and sensor_c>=10 :
                        obj.move('F')
                    break
                elif check_right() and (not check_center()) :    
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 9) and sensor_c>=10 :
                        obj.move('F')
                    break
            obj.move('F')
        
        recenter()
        # delay(3)
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        print("Travelled one block\n")
        if check_left():  #left turn possible
            # delay(5)
            change_dir(-1)
            left_exchange()
            print("Exchanged left")
            print("Turning left...")
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            # delay(5)

            # else :
            #     prev_b = sensor_b
            #     while ((sensor_b - prev_b) <= 9) and (sensor_b - prev_b) >= 0 and sensor_c>=10 :
            #         # print("Sensor_c inside while:", sensor_c)
            #         # print("Difference inside while: ", sensor_b - prev_b)
            #         obj.move('F')

            #     delay(5)
            #     change_dir(-1)
            #     left_exchange()
            #     print("\nExchanged left")
            #     print("Turning left...\n")
        
            # prev_b = sensor_b
            # l = 1
            # r = 0
            # while ((sensor_b - prev_b) <= 9) and (sensor_b - prev_b) >= 0 and sensor_c>=10 :
            #     # print("Sensor_c inside while:", sensor_c)
            #     # print("Difference inside while: ", sensor_b - prev_b)
            #     obj.move('F')
            
            # obj.stop()
            # delay(1)


        elif check_center():
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            # obj.move('F')
            prev_b = sensor_b
            c = c + 1
            recenter()
            # l=0
            # r=0
            # pass
            # print("Moving forward")
            

        elif check_right():
            # delay(5)
            change_dir(1)
            right_exchange()
            print("Exchanged right")
            print("Turning right...")
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            # delay(5)
            # while ((sensor_b - prev_b) <= 9) and (sensor_b - prev_b) >= 0 and sensor_c>=10 :
                # print("Sensor_c inside while:", sensor_c)
                # print("Difference inside while: ", sensor_b - prev_b)
                # obj.move('F')

            # delay(5)
            # change_dir(1)
            # right_exchange()
            # print("\nExchanged right")
            # print("Turning right...\n")
        
            # prev_b = sensor_b
            # l = 0
            # r = 1

            # while ((sensor_b - prev_b) <= 9) and (sensor_b - prev_b) >= 0 and sensor_c>=10 :
            #     # print("Sensor_c inside while:", sensor_c)
            #     # print("Difference inside while: ", sensor_b - prev_b)
            #     obj.move('F')
            
            # # obj.stop()
            # delay(1)

        else:
            # Dead End
            # delay(5)
            change_dir(2)
            deadend_exchange()
            print("Exchanged deadend")
            print("U turning...\n")
            prev_b = sensor_b
            c = c + 1
            recenter()
            
            # delay(5)

            # while ((sensor_b - prev_b) <= 9) and (sensor_b - prev_b) >= 0 and sensor_c>=10 :
            #     # print("Sensor_c inside while:", sensor_c)
            #     # print("Difference inside while: ", sensor_b - prev_b)
            #     obj.move('F')

            # delay(5)
            # change_dir(2)
            # deadend_exchange()
            # print("\nExchanged deadend")
            # print("U turning...\n")
        
            # prev_b = sensor_b
            # while ((sensor_b - prev_b) <= 9) and (sensor_b - prev_b) >= 0 and sensor_c>=10 :
                # print("Sensor_c inside while:", sensor_c)
                # print("Difference inside while: ", sensor_b - prev_b)
                # obj.move('F')
            
            # obj.stop()
            # delay(5)
    # delay(5)
    # print("Travelled one block")
    
# rospy.spin()

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
#         # obj.move('F')
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
