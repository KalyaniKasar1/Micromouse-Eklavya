#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

x_dist = 0
y_dist = 0

def clbk_odom(msg):
    global x_dist
    global y_dist
    global yaw_
    # position
    position_ = msg.pose.pose.position
    # gives x and y distance of the bot
    x_dist = position_.x
    y_dist = position_.y
    
    # yaw
    # convert quaternions to euler angles, only extracting yaw angle for the robot
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    
    yaw_ = euler[2]
    print(x_dist, y_dist)

def clbk_laser(msg):
    region = {
        'p' : msg.ranges[:],
    }
    # region['p'][0] represents the 0 degree and 0the value start from back and continues in anti-clockwise direction
    for i in range(360):
        print (region['p'][i])

def main():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom) 
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)  
    rospy.init_node('cmd_robot', anonymous=True)
    rate = rospy.Rate(50) # 40hz

    while not rospy.is_shutdown():
        msg1 = Twist()
	#positive speed_z value represents clockwise angular velocity of the bot and positive speed_x value represents forward linear velocity of the robot
        speed_z = 0
        speed_x = 0.1
        msg1.linear.x = speed_x
        msg1.angular.z = speed_z
        pub.publish(msg1)
        rate.sleep()


if __name__ == '__main__':
    main()
