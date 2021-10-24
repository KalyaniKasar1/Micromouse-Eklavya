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

# Global Variables
sensor_l, sensor_c, sensor_r = 0, 0, 0
dir= 2  #by default direction is south facing (yaw=0), direction is chosen from the below list
dirs=[180,-90,0,90]  # correspond to the north, west, south & east directions
pub = None 
l=0  #Becomes 1 if left turn has been taken...used to avoid immediate left turn after one left turn 
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

    # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r))

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
            
def delay(t,vel) : #to give a certain time period delay after every turn
    print("Delaying............")
    t0 = rospy.Time.now().to_sec()
    t1=0
    while ((t1-t0)<t) :
        t1 = rospy.Time.now().to_sec()
        obj.move(vel)
    
def check_left() : #checks if wall is present on the left
    global sensor_l, sensor_r, sensor_c, l
    print("Inside checkleft....")
    
    if sensor_l>=2 and sensor_l <= 18 :
        #wall on left
        # check_front()
        return True
    elif sensor_l>18 :
        delayvar=0.8
        if (sensor_r<(sensor_l+1)) and (sensor_r>(sensor_l-1)) :
            delayvar= sensor_c*0.05
        delay(1.5+delayvar, 0.15)
        print("Taking a left turn\n...\n...\n...\n...\n...\n...\n...\n...\n...")
        target=check_dir(1)  # +1 passed means we want to take left turn, target means the target yaw value
        obj.rotate(target) #turn left
        delay(2.5,0.3) #1.5
    
        
def check_right() : #checks if wall is present on the right
    global sensor_r
    print("Inside checkright.....")
    if sensor_r>=2 and sensor_r <= 18 :
    #if sensor_r>= 9 and sensor_r<=18:
    # if sensor_r>=2 and sensor_r<=18 :
        #wall on right, so dead end
        print("Taking a U turn\n...\n...\n...\n...\n...\n...\n...\n...\n...")
        target=check_dir(2)
        obj.rotate(target) #turn 180
        delay(2.5,0.3) #1.5

    #elif sensor_r>6 and sensor_r<8 : 
    # elif sensor_r>20:
    elif sensor_r>18 :
        # no wall on right
        # print("Taking a right turn\n...\n...\n...\n...\n...\n...\n...\n...\n...")
        delay(1.5,0.2)
        print("Taking a right turn\n...\n...\n...")
        target=check_dir(-1)  # -1 passed means we want to take right turn, target means the target yaw value
        obj.rotate(target) #turn right
        delay(2.5,0.3) #1.5


def check_front() : #checks if wall is present in front
    global sensor_c
    l=0
    print("Inside checkfront......")
    if sensor_c>=2 and sensor_c <=9 :
        #wall in front
        # check_right()
        return True
    # elif sensor_c >=18 :
    elif sensor_c>9 :
        obj.move(0.38)
        pass #pidtune
        #obj.pid(regions)
    
def leftfollow():
    global sensor_l, sensor_c, sensor_r
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    #srv = rospy.Service('wall_follower_switch', SetBool, wall_follower_switch)
    rate = rospy.Rate(50)   #orig rate for 20
    while not rospy.is_shutdown():
        obj.move(0.38)
        #check_left()
        if (check_left()) : #if wall on left
            if (check_front()) : #if wall in front
                if (check_right()) : ##if wall on right
                    print("Dead End!\nDead End!\nDead End!\nDead End!")
                    print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))
                else :
                    print("Only right turn.\nOnly right turn.\nOnly right turn.\nOnly right turn.\n")
                    print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))
            else :
                print("Straight path.\nStraight path.\nStraight path.\nStraight path.\n")
                print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))
        else :
            print("Left turn detected.\nLeft turn detected.\nLeft turn detected.\nLeft turn detected.\n")
            print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r,"\n"))

        # flagl=flagf=flagr=0 
        #obj.pid(sensor_l, sensor_c, sensor_r)
        # msg1.angular.z=0.0
        # msg1.linear.x=0.32
        # pub_.publish(msg1)
        rate.sleep()

if __name__ == '__main__':
    obj=bot()
    leftfollow()
    


