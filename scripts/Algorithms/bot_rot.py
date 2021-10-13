#! /usr/bin/env python

# bot class, yaw coordinate system, importing classes in python, managing movements, straight wall func me pid, data structures to implement bfs ds etc

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math

roll = pitch = yaw = target = 0.0
flag = 0
#target = int(input("Enter degree of rotation:"))
kp=0.95
msg1 = Twist()
pub=None

def get_rotation(msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    #print("Yaw value", yaw)
    
def rotate():  
    global msg1, yaw, pub, target, flag
    target_rad = target * math.pi/180
    msg1.angular.z = kp * (target_rad-yaw)
    yaw_deg = (yaw*180/math.pi)
    
    if (yaw_deg<= (target-0.09)) :
        pub.publish(msg1)
        print("target=%5.2f current:%5.2f" %(target,yaw_deg))
    else :    
        print("Robot successfully turned!")
        print("Final yaw:", yaw_deg)
        msg1.angular.z = 0
        pub.publish(msg1)
        flag = 1
        
def main():
    global pub, target, flag
    
    rospy.init_node('bot_rot')
    
    target=90.0
    sub = rospy.Subscriber ('/odom', Odometry, get_rotation)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    print("Rotating by %5.2f..." %target)
    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():
        if flag == 0 :
            rotate()
        elif flag == 1 :
            print("Done")
            flag = -1
            
        rate.sleep()

if __name__ == '__main__':
    main()
