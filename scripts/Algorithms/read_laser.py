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
pub = None 
regions=[]

def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r, sensor_b, regions
    
    # 30 degrees
    # regions = [  
    #     round(100*min(max(max(msg.ranges[345:359]), max(msg.ranges[0:14])), 100)),   
    #     round(100*min(max(msg.ranges[75:104]), 100)), 
    #     round(100*min(max(msg.ranges[165:194]), 100)),
    #     round(100*min(max(msg.ranges[255:284]), 100))
    # ]

    # 19 degrees
    # regions = [  
    #     round(100*min(max(max(msg.ranges[351:359]), max(msg.ranges[0:8])), 100)),   
    #     round(100*min(max(msg.ranges[81:98]), 100)), 
    #     round(100*min(max(msg.ranges[171:188]), 100)),
    #     round(100*min(max(msg.ranges[261:278]), 100))
    # ]

    # 15 degrees
    # regions = [  
    #     round(100*min(max(max(msg.ranges[353:359]), max(msg.ranges[0:6])), 100)),   
    #     round(100*min(max(msg.ranges[83:97]), 100)), 
    #     round(100*min(max(msg.ranges[173:187]), 100)),
    #     round(100*min(max(msg.ranges[263:277]), 100))
    # ]

    # 10 degrees
    # regions = [  
    #     round(100*min(max(max(msg.ranges[356:359]), max(msg.ranges[0:5])), 100)),   
    #     round(100*min(max(msg.ranges[86:95]), 100)), 
    #     round(100*min(max(msg.ranges[176:185]), 100)),
    #     round(100*min(max(msg.ranges[266:275]), 100))
    # ]

    # 5 degrees
    regions = [  
        round(100*min(max(max(msg.ranges[358:359]), max(msg.ranges[0:2])), 100)),   
        round(100*min(max(msg.ranges[88:92]), 100)), 
        round(100*min(max(msg.ranges[178:182]), 100)),
        round(100*min(max(msg.ranges[268:272]), 100))
    ]

    if sensor_l != regions[3] or sensor_c != regions[2] or sensor_r != regions[1] or sensor_b != regions[0]:
        print("l: {} \t c: {} \t r: {} \t b: {}".format(regions[3], regions[2], regions[1], regions[0]))
        # print(msg.ranges[90:180])
        # print(msg.ranges[90:270])
        # print(msg.ranges[0:90], msg.ranges[270:360])
        # print(msg.ranges[0:90])
        # print(msg.ranges[270:360])

    
    sensor_l = regions[3]
    sensor_c = regions[2]
    sensor_r = regions[1]
    sensor_b = regions[0]

    # if bot.dir==1 : #bot is internally facing east
    #     right_exchange()
    # elif bot.dir==2 : #bot is internally facing south
    #     deadend_exchange()
    # elif bot.dir==3 :  #bot is internally facing west
    #     left_exchange()


def sensor_values():
    global sensor_l, sensor_c, sensor_r, sensor_b
    rospy.init_node('reading_laser')
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        # print("l: {} \t c: {} \t r: {} \t b: {}".format(sensor_l, sensor_c, sensor_r, sensor_b))
        pass


if __name__ == '__main__':
    # obj=bot()
    sensor_values()
