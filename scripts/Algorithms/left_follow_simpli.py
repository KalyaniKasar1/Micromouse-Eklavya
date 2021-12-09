#! /usr/bin/env python
# Speed is 0.1
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
final_dir = 0

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
    if sensor_c >= 5 and sensor_c <= 11 :  # <=11 for speed=0.1, <=12 for speed=0.15
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

def calibrate():
    global sensor_c, sensor_b, sensor_l, sensor_r
    # if
    # initial_dir= 
    pass

def check_end():
    # delay(3)
    end = False
    global sensor_l, sensor_c, sensor_r, sensor_b, dists, final_dir
    le=0    
    re=0
    print(dists[0],dists[180],dists[270])
    print(round(min(dists[114:117])*100) >=26)
    print(round(min(dists[154:157])*100) >=26)
    print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    

    if (sensor_c <= 29) and (sensor_c >= 24):
        if (sensor_c <= sensor_r+2 and sensor_c >= sensor_r-2) and sensor_l <= 11 :  
            le=1  #means bot entered centre from left side
        elif (sensor_c <= sensor_l+2 and sensor_c >= sensor_l-2) and sensor_r <= 11 :
            re=1  #means bot entered centre from right side
        
        if bot.dir==0:  # for speed=0.1, >=27 & for speed=0.15, >=26 
            if le==1 and (round(min(dists[114:117])*100) >=26) and (round(min(dists[154:157])*100) >=26) :
                # print("\n\nDetected.")
                # print(round(min(dists[114:117])*100) >=26)
                # print(round(min(dists[154:157])*100) >=26)
                end = True
            elif re==1 and (round(min(dists[244:247])*100) >=26) and (round(min(dists[204:207])*100) >=26) : 
                # print("\n\nDetected.")
                # print(round(min(dists[244:247])*100) >=26)
                # print(round(min(dists[204:207])*100) >=26)
                end = True
        elif bot.dir==1:
            if le==1 and (round(min(dists[24:27])*100) >=26) and (round(min(dists[64:67])*100) >=26) :
                # print("\n\nDetected.")
                # print(round(min(dists[24:27])*100) >=26)
                # print(round(min(dists[64:67])*100) >=26)
                end = True
            elif le==1 and (round(min(dists[154:157])*100) >=26) and (round(min(dists[114:117])*100) >=26) :
                # print("\n\nDetected.")
                # print(round(min(dists[154:157])*100) >=26)
                # print(round(min(dists[114:117])*100) >=26)
                end = True
        elif bot.dir==2:
            if le==1 and (round(min(dists[294:297])*100) >=26) and (round(min(dists[334:337])*100) >=26) :
                # print("\n\nDetected.")
                # print(round(min(dists[294:297])*100) >=26)
                # print(round(min(dists[334:337])*100) >=26)
                end = True
            elif re==1 and (round(min(dists[64:67])*100) >=26) and (round(min(dists[24:27])*100) >=26) : 
                # print("\n\nDetected.")
                # print(round(min(dists[64:67])*100) >=26)
                # print(round(min(dists[24:27])*100) >=26)
                end = True
        elif bot.dir==3:
            if le==1 and (round(min(dists[204:207])*100) >=26) and (round(min(dists[244:247])*100) >=26) :
                # print("Detected.")
                # print(round(min(dists[204:207])*100) >=26)
                # print(round(min(dists[244:247])*100) >=26)
                end = True
            elif re==1 and (round(min(dists[334:337])*100) >=26) and (round(min(dists[294:297])*100) >=26) : 
                # print("Detected.")
                # print(round(min(dists[334:337])*100) >=26)
                # print(round(min(dists[294:297])*100) >=26)
                end = True

        if end :
            print("Hurrayyy!")
            print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            delay(2)
            print("Required path: ", de)
            print("Path length : ", path)
            path_list=list(collections.deque(de))
            path_list="".join(path_list)
            pathf = open("path.txt","w")
            # pathf = open("path.txt","w+")
            pathf.write(path_list)
            pathf.close()
            print("\n\n")
            final_dir=bot.dir

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
    
def left_follow():
    global sensor_l, sensor_c, sensor_r, prev_b, first_run, c, path
    delay(45)
    if first_run :
        prev_b = sensor_b
        first_run = False
    # path=1

    while(1) :
        if path>=4 and de[path-3]=='B':
            simplifypath(de)

        while ((sensor_b - prev_b) <= 16) and sensor_c>=10 : #for speed=0.1, 17.5 & for speed=0.15, 16
            if c >= 2 :
                if check_left() :
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 8) and sensor_c>=10 :  #for speed=0.1, 9 & for speed=0.15, 8
                        obj.slow_move('F')
                    break
                elif check_right() and (not check_center()) :    
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 8) and sensor_c>=10 :
                        obj.slow_move('F')
                    break
            obj.move('F')
        
        recenter()
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        print("Travelled one block\n")
        # delay(5)

        if check_end():  #checks for end of maze
            break

        if check_left():  #Left turn possible
            change_dir(-1)
            left_exchange()
            print("Turning left...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            de.append('L')
            print("Appended L")
            path = path+1

        elif check_center():  #Straight path
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            prev_b = sensor_b
            c = c + 1
            if check_right() and sensor_c>=20:
                de.append('S')
                print("Appended S")
                # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
                # delay(8)
                path = path+1
            recenter()

        elif check_right():  #Right turn possible
            change_dir(1)
            right_exchange()
            print("Turning right...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            de.append('R')
            print("Appended R")
            path = path+1

        else:  # Dead end
            change_dir(2)
            deadend_exchange()
            print("U turning...\n")
            prev_b = sensor_b
            c = c + 1
            de.append('B')
            print("Appended B")
            path= path+1  
            recenter()

# backtracking    
def backtrack():
    global sensor_l, sensor_c, sensor_r, prev_b, first_run, c, path, final_dir
    delay(5)

    bot.dir=0
    pathf = open(r"path.txt","r")
    path_list=pathf.readline()
    pathf.close()
    print(path_list)
    first_run = True
    print("Backtracking...\n..")
    # path_list='LRSLSRSRLSLLRLRRL'
    bot.dir=final_dir
    change_dir(2)
    
    if first_run :
        prev_b = sensor_b
        first_run = False
    # path=1
    x=len(path_list)-1
    # for i in path_list :
    while x>=0 :
        # print(path_list[x],end="-")
        while ((sensor_b - prev_b) <= 16) and sensor_c>=10 : #for speed=0.1, 17.5 & for speed=0.15, 16
            if c >= 2 :
                if check_left() :
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 8) and sensor_c>=10 :  #for speed=0.1, 9 & for speed=0.15, 8
                        obj.slow_move('F')
                    break
                elif check_right() and (not check_center()) :    
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 8) and sensor_c>=10 :
                        obj.slow_move('F')
                    break
            obj.move('F')
        
        recenter()
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        # print("Travelled one block\n")

        if path_list[x]=='R' and check_left():  #Left turn possible
            change_dir(-1)
            left_exchange()
            print("Turning left...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            x=x-1


        elif path_list[x]=='S' and sensor_c>=18 and (check_left or check_right):  #Straight path
            print("Going straight...")
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            prev_b = sensor_b
            c = c + 1
            recenter()
            x=x-1

        elif path_list[x]=='L' and check_right():  #Right turn possible
            change_dir(1)
            right_exchange()
            print("Turning right...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            x=x-1
        
        else :
            prev_b = sensor_b
    prev_b = sensor_b
    recenter()
    while ((sensor_b - prev_b) <= 16) and sensor_c>=10 : #for speed=0.1, 17.5 & for speed=0.15, 16
        obj.move('F')
    delay(1)
    print("Reached the start point")

# final run    
def final_run():
    global sensor_l, sensor_c, sensor_r, prev_b, first_run, c, path, final_dir
    delay(5)
    bot.dir=0
    path = open(r"path.txt","r")
    path_list=path.readline()
    path.close()
    print(path_list)
    # path_list='LRSLSRSRLSLLRLRRL'
    first_run = True
    if first_run :
        prev_b = sensor_b
        first_run = False
    # path=1
    x=0
    # for i in path_list :
    while x<len(path_list) :
        # print(path_list[x],end="-")
        while ((sensor_b - prev_b) <= 16) and sensor_c>=10 : #for speed=0.1, 17.5 & for speed=0.15, 16
            if c >= 2 :
                if check_left() :
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 8) and sensor_c>=10 :  #for speed=0.1, 9 & for speed=0.15, 8
                        obj.slow_move('F')
                    break
                elif check_right() and (not check_center()) :    
                    prev_b = sensor_b
                    while ((sensor_b - prev_b) <= 8) and sensor_c>=10 :
                        obj.slow_move('F')
                    break
            obj.move('F')
        
        recenter()
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        # print("Travelled one block\n")

        if path_list[x]=='L' and check_left():  #Left turn possible
            change_dir(-1)
            left_exchange()
            print("Turning left...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            x=x+1


        elif path_list[x]=='S' and sensor_c>=18 and (check_left or check_right):  #Straight path
            print("Going straight...")
            # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
            prev_b = sensor_b
            c = c + 1
            recenter()
            x=x+1

        elif path_list[x]=='R' and check_right():  #Right turn possible
            change_dir(1)
            right_exchange()
            print("Turning right...")
            # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b), "\n")    
            prev_b = sensor_b
            c = 0
            x=x+1
        
        else :
            # print("Errrrrrr")
            prev_b = sensor_b
    prev_b = sensor_b
    while ((sensor_b - prev_b) <= 16) and sensor_c>=10 : #for speed=0.1, 17.5 & for speed=0.15, 16
        obj.move('F')
    delay(1)
    print("\n\n")
    # final_dir=bot.dir


if __name__ == '__main__':
    obj = bot()
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)
    left_follow()
    backtrack()
    final_run()
    # while(1):
    #     obj.move('F')
    rospy.spin()

