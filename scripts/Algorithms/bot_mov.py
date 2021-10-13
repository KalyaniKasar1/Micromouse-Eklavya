#! /usr/bin/env python

# bot class, yaw coordinate system, importing classes in python, managing movements, straight wall func me pid, data structures to implement bfs ds etc

import rospy
from geometry_msgs.msg import Twist
import math

msg1 = Twist()
pub=None
linx=0.0
kp=0.3

def move():
    global msg1, pub, linx, angz
    target=0.4
    linx= linx + kp * (target - linx) 
    msg1.linear.x= linx
    #if (linx <= (target-0.009)) :
    if linx <= target-0.001 :
        pub.publish(msg1)
        print("Speed x: ", linx)

def main():
    global msg1, pub, linx
    
    #linx=0.35
    msg1.angular.z=0.0
    rospy.init_node('bot_mov')
    
    #sub = rospy.Subscriber ('/cmd_vel', Twist, get d)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():
        move()
        rate.sleep()

if __name__ == '__main__':
    main()
