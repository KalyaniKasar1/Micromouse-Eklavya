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
import collections
de = collections.deque([],1000)
sensor_l, sensor_c, sensor_r, sensor_b = 0, 0, 0, 0
l, c, r = 0, 0, 0
pub = None 
regions=[]
dists=[]
prev_b = 0
angle=0
path=1
first_run = True

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions, dists
    dists=msg.ranges[:]
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
    # print("\nDelaying............\n")
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
        # print("\nLeft possible!")
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
        return True

def check_right(): # Checking for right wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    if sensor_r >= 5 and sensor_r <= 11:
        return False
    elif (sensor_l+sensor_r)>18 :
        # print("\nRight possible!")
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))    
        return True

def check_center(): # Checking for center wall
    global sensor_l, sensor_c, sensor_r, sensor_b
    if sensor_c >= 5 and sensor_c <= 11 :
        # print("\nWall Ahead!\n")
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        return False
    else:
        return True

def recenter():
    global sensor_l, sensor_r
    if sensor_l <= 7 :
        while sensor_l <= 7 :
            obj.slow_move('R')
    elif sensor_r <= 7 :
        while sensor_r <= 7 :
            obj.slow_move('L')   

def check_end():
    end = False
    global sensor_l, sensor_c, sensor_r, sensor_b, dists
    if (sensor_c <= 28) and (sensor_c >= 24):
        if ((sensor_c == sensor_l or sensor_c == sensor_l+1 or sensor_c == sensor_l-1) and sensor_r <= 11) or ((sensor_c == sensor_r or sensor_c == sensor_r+1 or sensor_c == sensor_r-1)  and sensor_l <= 11):
            if bot.dir==0 and (round(min(dists[224:226])*100) >=31 or round(min(dists[134:136])*100) >=31)  :  #when dir is N
                end = True 
            elif bot.dir==1 and (round(min(dists[134:136])*100) >=31 or round(min(dists[44:46])*100) >=31)  :  #when dir is E
                end = True
            elif bot.dir==2 and (round(min(dists[44:46])*100) >=31 or round(min(dists[314:316])*100) >=31)  :  #when dir is S
                end = True
            elif bot.dir==3 and (round(min(dists[224:226])*100) >=31 or round(min(dists[314:316])*100) >=31)  :  #when dir is W
                end = True
        # if (sensor_c == sensor_l or sensor_c == sensor_l+1 or sensor_c == sensor_l-1) and sensor_r <= 11 :
        #     if round(min(dists[220:230])*100) >=33 or round(min(dists[310:320])*100) >=33 or round(min(dists[130:140])*100) >=33 or round(min(dists[40:50])*100) >=33 :
        #         end = True 
        # elif (sensor_c == sensor_r or sensor_c == sensor_r+1 or sensor_c == sensor_r-1)  and sensor_l <= 11 : 
        #     if round(max(dists[220:230])*100) >=33 or round(max(dists[310:320])*100) >=33 or round(max(dists[130:140])*100) >=33 or round(max(dists[40:50])*100) >=33 :
        #         end = True
    if end :
        print("Hurrayyy!")
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        delay(1)
        print("Required path: ", de)
        print("Path length : ", path)
    return end


def simplifypath(de):#L S B L ~ L R  :4~2
    global angle, path
    angle = 0
    print("Original Path : ", de)
    print("Original Path length : ", path)
    j = de.index('B') - 1
    while(j <= (path-4)):
        # if(de[j+1]=='B'):
        x=de[j]
        y=de[j+2]
        
        if(x=='L'):
            angle= angle+270
        elif(x=='R'):
            angle= angle+90

        if(y=='L'):
            angle= angle+270
        elif(y=='R'):
            angle= angle+90
        
        angle = (angle+180) % 360
        
        if(angle==0):
            for i in range(3):
                del de[j] 
            de.insert(j,'S')
            path=path-2
        elif(angle==90):
            for i in range(3):
                del de[j] 
            de.insert(j,'R')
            path=path-2
        elif(angle==180):
            for i in range(3):
                del de[j] 
            de.insert(j,'B')
            path=path-2
        elif(angle==270):
            for i in range(3):
                del de[j] 
            de.insert(j,'L')
            path=path-2

        j=j+1            

        # else:
        #     de[j]=de[j]
        #     j=j+1
    print("Refined Path : ", de)
    print("Refined Path length : ", path)
    # delay(5)
    


def leftfollow():
    global sensor_l, sensor_c, sensor_r, prev_b, first_run, c, path
    delay(5)
    if first_run :
        prev_b = sensor_b
        first_run = False
    # path=1

    while(1) :
        if path>=4 and de[path-3]=='B':
            simplifypath(de)

        while ((sensor_b - prev_b) <= 17.5) and sensor_c>=10 :
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
        print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        print("Travelled one block\n")
        # delay(5)

        if check_end():  #checks for end of maze
            break

        if check_left():  #Left turn possible
            change_dir(-1)
            left_exchange()
            # print("Exchanged left")
            print("Turning left...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            de.append('L')
            print("Appended L")
            path = path+1

        elif check_center():  #Straight path
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            # obj.move('F')
            prev_b = sensor_b
            c = c + 1
            # straight=1
            if check_right():
                de.append('S')
                print("Appended S")
                print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
                # delay(8)
                path = path+1
            recenter()

        elif check_right():  #Right turn possible
            change_dir(1)
            right_exchange()
            # print("Exchanged right")
            print("Turning right...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            # right=1
            de.append('R')
            print("Appended R")
            path = path+1

        else:  # Dead end
            change_dir(2)
            deadend_exchange()
            # print("Exchanged deadend")
            print("U turning...\n")
            prev_b = sensor_b
            c = c + 1
            de.append('B')
            path= path+1  
            recenter()


    # if left == 1:
    #     # obj.left() # deque for storing the numbers
    #     de.append('L')
    #     path= path+1
    #     left=0
    # elif right == 1:
    #     # obj.right() 
    #     de.append('R')
    #     path= path+1
    #     right=0

    # elif straight == 1:
    #     #obj.forward() 
    #     de.append('S')
    #     path= path+1
    #     straight=0
    # else :
    #     #obj.back()
    #     de.append('B')
    #     path= path+1      
 
 
 
# while(i<path):
#        obj.move(de[i])
#        i=i+1 

# def turn(dir):
#     if dir == 'L':
#     obj.left()
#     elif dir == 'R':
#     obj.right()
#     elif dir == 'S':
#     obj.straight()
#     else:
#     obj.back()         

if __name__ == '__main__':
    obj = bot()
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)
    leftfollow()
    # simplifypath(de)   
    # change_dir(1)
    rospy.spin()

